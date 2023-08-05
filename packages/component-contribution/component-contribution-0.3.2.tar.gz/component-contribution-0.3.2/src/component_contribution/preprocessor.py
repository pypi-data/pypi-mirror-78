"""calculations needed for component-contribution predictions."""
# The MIT License (MIT)
#
# Copyright (c) 2013 The Weizmann Institute of Science.
# Copyright (c) 2018 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark.
# Copyright (c) 2018 Institute for Molecular Systems Biology,
# ETH Zurich, Switzerland.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import logging
from typing import Dict, Iterable, List, Optional, Tuple, Union

import numpy as np
from equilibrator_cache import Compound, Reaction

from . import CCModelParameters
from .linalg import LINALG


logger = logging.getLogger(__name__)


class Preprocessor(object):
    """A Component Contribution preprocessing class."""

    DEFAULT_RMSE_INF = 1e5

    def __init__(
        self, parameters: CCModelParameters, rmse_inf: float = DEFAULT_RMSE_INF
    ) -> None:
        """Create a GibbsEnergyPredictor object.

        Parameters
        ----------
        parameters : CCModelParameters
            all the parameters needed for running Component Contribution
            predictions.
        rmse_inf : float
            The MSE of the subspace that's not covered by Component Contribution
            which is set as an arbitrary high value. By default we set it to
            10^10 (kJ^2 / mol^2)

        """
        self._compound_ids = parameters.train_G.index.tolist()
        self.Nc = parameters.dimensions.at["Nc", "number"]

        # store the number of "real" groups, i.e. not including the "fake"
        # ones that are placeholders for non-decomposable compounds
        self.Ng = parameters.dimensions.at["Ng", "number"]

        self.S = parameters.train_S.values
        G = parameters.train_G.values

        self.RMSE_rc = np.sqrt(parameters.MSE.at["rc", "MSE"])
        self.RMSE_gc = np.sqrt(parameters.MSE.at["gc", "MSE"])
        self.RMSE_inf = rmse_inf

        self.mu = np.hstack([parameters.dG0_cc, parameters.dG0_gc[: self.Ng]])

        # pre-processing matrices
        self.L_rc = np.hstack(
            [
                parameters.inv_S @ parameters.P_R_rc,
                np.zeros((self.S.shape[1], self.Ng)),
            ]
        )
        self.L_gc = np.hstack(
            [
                parameters.inv_GS @ G.T @ parameters.P_N_rc,
                parameters.inv_GS[:, : self.Ng],
            ]
        )
        L_inf = np.hstack(
            [parameters.P_N_gc @ G.T, parameters.P_N_gc[:, : self.Ng]]
        )

        self.L_c = LINALG.qr_rank_deficient(
            np.vstack(
                [
                    self.RMSE_rc * self.L_rc,
                    self.RMSE_gc * self.L_gc,
                    self.RMSE_inf * L_inf,
                ]
            )
        )

    def get_compound_vector(self, compound: Compound) -> Union[np.array, None]:
        """Get the index of a compound in the original training data.

        Parameters
        ----------
        compound : Compound
            a Compound object


        Returns
        -------
        x
            the index of that compound, or -1 if it was not in the
            training list

        """

        try:
            # This compound is in the training set so we can use reactant
            # contributions for it
            i = self._compound_ids.index(compound.id)
            x = np.zeros(self.Nc + self.Ng, dtype=float)
            x[i] = 1
            return x
        except ValueError:
            if compound.group_vector:
                # This compound is not in the training set so must use group
                # contributions
                return np.hstack(
                    [np.zeros(self.Nc, dtype=float), compound.group_vector]
                )
            else:
                # This compound cannot be decomposed and therefore we cannot
                # have any estimate for it
                return None

    def get_compound_prediction(
        self, compound: Compound
    ) -> Tuple[Optional[float], Optional[np.ndarray]]:
        """Get the (mu, sigma) predictions of a compound's formation energy."""
        x = self.get_compound_vector(compound)
        if x is None:
            return None, None
        else:
            return self.mu @ x, self.L_c @ x

    def get_reaction_prediction(
        self, reaction: Reaction
    ) -> Tuple[float, np.ndarray, Dict[Compound, float]]:
        """Get the (mu, sigma) predictions of a reaction's energy.

        Parameters
        ----------
        reaction : Reaction
            the input Reaction object


        Returns
        -------
        mu : float
            the mean of the standard Gibbs energy estimate
        sigma : array
            a vector representing the square root of the covariance matrix
            (uncertainty)
        residual : dict
            the residual reaction in sparse notation (unknown and
            undecomposable reactants)

        """
        tot_mu = 0.0  # mean of the delta G estimate
        tot_sigma = np.zeros(self.L_c.shape[0])  # sqrt uncertainty vector
        residual = dict()

        for compound, coefficient in reaction.items(protons=False):
            mu, sigma = self.get_compound_prediction(compound)
            if mu is not None:
                tot_mu += coefficient * mu
                tot_sigma += coefficient * sigma
            else:
                residual[compound] = coefficient

        return tot_mu, tot_sigma, residual

    def get_reaction_prediction_multi(
        self, reactions: List[Reaction]
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Get the (mu, sigma) predictions of a reaction's energy.

        Parameters
        ----------
        reactions: List[Reaction] :
            a list of Reaction objects


        Returns
        -------
        mus : np.array
            the mean of the standard Gibbs energy estimates
        sigmas : np.array
            a matrix whose columns are the square root vectors (one for each
            reaction)
        residual : np.array
            another matrix with the square root of the covariance corresponding
            to the 'unknown' compounds (i.e. where the uncertainty is infinite)

        """
        Nr = len(reactions)
        mus = np.zeros(Nr)
        sigmas = np.zeros((Nr, self.L_c.shape[0]))

        residuals = []
        for i, reaction in enumerate(reactions):
            mu, sigma, residual = self.get_reaction_prediction(reaction)
            mus[i] = mu
            sigmas[i, :] = sigma
            residuals.append(residual)

        # make an ordered list of the unknown-undecomposable compounds
        residual_compounds = set()
        for sparse in residuals:
            residual_compounds.update(sparse.keys())
        residual_compounds = sorted(residual_compounds)

        # construct the residual stoichiometric matrix U
        U = np.zeros((len(residual_compounds), Nr))
        for i, sparse in enumerate(residuals):
            for cpd, coeff in sparse.items():
                j = residual_compounds.index(cpd)
                U[j, i] = coeff

        return mus, sigmas, self.RMSE_inf * U

    def decompose_reaction(
        self, reaction: Reaction
    ) -> Tuple[np.ndarray, Dict[Compound, float]]:
        """Decompose a reaction.

        Parameters
        ----------
        reaction : Reaction
            the input Reaction object


        Returns
        -------
        x : ndarray
            the reaction vector (describing both RC and GC changes)
        residual : dict
            the residual reaction in sparse notation

        """
        x = np.zeros(self.Nc + self.Ng, dtype=float)
        residual = dict()
        for compound, coefficient in reaction.items(protons=False):
            _x = self.get_compound_vector(compound)
            if _x is None:
                residual[compound] = coefficient
            else:
                x += coefficient * _x

        return x, residual

    def dg_analysis(self, reaction: Reaction) -> Iterable[Dict[str, object]]:
        r"""Analyse the weight of each observation to the :math:`\Delta G`.

        Parameters
        ----------
        reaction : Reaction
            the input Reaction object


        Returns
        -------
        list
            a list of reactions that contributed to the value of the
            :math:`\Delta G` estimation, with their weights and extra
            information

        """
        x, residual = self.decompose_reaction(reaction)
        if residual:
            return []

        # dG0_cc = (x*G1 + x*G2 + g*G3)*b
        weights_rc = (self.L_rc @ x).round(5)
        weights_gc = (self.L_gc @ x).round(5)
        weights = abs(weights_rc) + abs(weights_gc)

        for j in reversed(np.argsort(weights)):
            if abs(weights[j]) < 1e-5:
                continue
            r = {
                i: self.S[i, j]
                for i in range(self.S.shape[0])
                if self.S[i, j] != 0
            }
            yield {
                "index": j,
                "w_rc": weights_rc[j],
                "w_gc": weights_gc[j],
                "reaction": r,
            }

    def is_using_group_contribution(self, reaction: Reaction) -> bool:
        r"""Check if group contributions is needed for the :math:`\Delta G`.

        Parameters
        ----------
        reaction : Reaction
            the input Reaction object


        Returns
        -------
        bool
            True if the reaction require group contributions.

        """
        x, residual = self.decompose_reaction(reaction)
        if residual:
            return False

        sum_w_gc = np.linalg.norm(self.L_gc @ x, 1)
        logging.info("sum(w_gc) = %.2g" % sum_w_gc)
        return sum_w_gc > 1e-5
