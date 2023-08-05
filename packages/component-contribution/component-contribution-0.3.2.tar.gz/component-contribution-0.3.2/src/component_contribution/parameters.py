"""module for component-contribution predictions."""
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
from collections import namedtuple
from typing import BinaryIO, Optional, Union

import numpy as np
import pandas as pd
import quilt
from requests.exceptions import ConnectionError

from . import DEFAULT_QUILT_PKG, DEFAULT_QUILT_VERSION


logger = logging.getLogger(__name__)

PARAMETER_NAMES = (
    "train_b train_S train_w train_G "
    "dimensions "
    "dG0_rc dG0_gc dG0_cc "
    "V_rc V_gc V_inf MSE "
    "P_R_rc P_R_gc P_N_rc P_N_gc "
    "inv_S inv_GS inv_SWS inv_GSWGS "
)


class CCModelParameters(namedtuple("CCModelParameters", PARAMETER_NAMES)):
    """Container class for all Component Contribution parameters."""

    @staticmethod
    def from_quilt(
        package: str = DEFAULT_QUILT_PKG,
        hash: Optional[str] = None,
        tag: Optional[str] = None,
        version: Optional[str] = DEFAULT_QUILT_VERSION,
        force: bool = True,
    ) -> "CCModelParameters":
        """Get the CC parameters from quilt.

        Parameters
        ----------
        package : str, optional
            The quilt package used to initialize the predictor
            (Default value = `equilibrator/component_contribution`)
        hash : str, optional
            quilt hash (Default value = None)
        version : str, optional
            quilt version (Default value = DEFAULT_QUILT_VERSION)
        tag : str, optional
            quilt tag (Default value = None)
        force : bool, optional
            Re-download the quilt data if a newer version exists
            (Default value = `True`).

        Returns
        -------
        CCModelParameters
            a collection of Component Contribution parameters.

        """
        try:
            logger.info("Fetching Component-Contribution parameters...")
            quilt.install(
                package=package,
                hash=hash,
                tag=tag,
                version=version,
                force=force,
            )
        except ConnectionError:
            logger.error(
                "No internet connection available. Attempting to use "
                "the existing component contribution model."
            )
        except PermissionError:
            logger.error(
                "You do not have the necessary filesystem permissions to "
                "download an update to the quilt data. Attempting to use the "
                "existing component contribution model."
            )
        pkg = quilt.load(package)

        param_dict = {k: v() for k, v in pkg.parameters._children.items()}
        return CCModelParameters(**param_dict)

    def to_npz(self, file: Union[str, BinaryIO]) -> None:
        """Save the parameters in NumPy uncompressed .npz format."""

        # convert the CCModelParameters object into a dictionary of NumPy
        # arrays. if one of the items is a pandas DataFrames, serialize it to 3
        # separate arrays (values, index, columns)
        param_dict = dict()
        for parameter_name in self._fields:
            parameter_value = self.__getattribute__(parameter_name)
            if type(parameter_value) == pd.DataFrame:
                param_dict[f"{parameter_name}_values"] = parameter_value.values
                param_dict[f"{parameter_name}_index"] = parameter_value.index
                param_dict[
                    f"{parameter_name}_columns"
                ] = parameter_value.columns
            else:
                param_dict[parameter_name] = parameter_value
        np.savez(file, **param_dict)

    @staticmethod
    def from_npz(file: Union[str, BinaryIO]) -> "CCModelParameters":
        """Load the parameters from a NumPy uncompressed .npz file."""

        npzfile = np.load(file, allow_pickle=True)
        param_dict = dict(npzfile)

        # translate the serializes DataFrames back to the original form
        for df_name in ["dimensions", "MSE", "train_G", "train_S"]:
            param_dict[df_name] = pd.DataFrame(
                data=param_dict[f"{df_name}_values"],
                index=param_dict[f"{df_name}_index"],
                columns=param_dict[f"{df_name}_columns"],
            )
            del param_dict[f"{df_name}_index"]
            del param_dict[f"{df_name}_columns"]
            del param_dict[f"{df_name}_values"]
        return CCModelParameters(**param_dict)
