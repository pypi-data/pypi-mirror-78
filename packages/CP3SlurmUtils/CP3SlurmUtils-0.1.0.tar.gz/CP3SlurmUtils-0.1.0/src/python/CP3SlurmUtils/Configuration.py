"""
Copyright (C) 2019  Universite catholique de Louvain, Belgium.

This file is part of CP3SlurmUtils.

CP3SlurmUtils is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CP3SlurmUtils is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CP3SlurmUtils.  If not, see <http://www.gnu.org/licenses/>.
"""

import imp
import os
import pickle

from CP3SlurmUtils.Exceptions import ConfigurationException
from CP3SlurmUtils.Exceptions import CP3SlurmUtilsException


class Configuration(object):
    def __init__(self):
        object.__init__(self)
        self._internal_config_attributes = []

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if not name.startswith('_internal_'):
            if name not in self._internal_config_attributes:
                self._internal_config_attributes.append(name)
        return

    def getConfigAttrs_(self):
        return self._internal_config_attributes


def loadConfiguration(filename):
    """_loadConfiguration_
    Load a configuration file and return its Configuration attribute.
    """
    confAttr = None
    if filename.endswith(".pkl"):
        try:
            with open(filename, 'rb') as fd:
                try:
                    confAttr = pickle.load(fd)
                except Exception as ex:
                    msg = "ERROR: Failed to unpickle file {file}"
                    msg += "\nError follows:\n{error}"
                    msg = msg.format(file=filename, error=str(ex))
                    raise CP3SlurmUtilsException(msg)
        except IOError as ex:
            msg = "ERROR: Failed to open file {file}"
            msg += "\nError follows:\n{error}"
            msg = msg.format(file=filename, error=str(ex))
            raise CP3SlurmUtilsException(msg)
    else:         
        cfgBaseName = os.path.basename(filename).replace(".py", "")
        cfgDirName = os.path.dirname(filename)
        if not cfgDirName:
            modPath = imp.find_module(cfgBaseName)
        else:
            modPath = imp.find_module(cfgBaseName, [cfgDirName])
        try:
            modRef = imp.load_module(cfgBaseName, modPath[0], modPath[1], modPath[2])
        except Exception as ex:
            msg = "ERROR: Unable to load configuration file {file}"
            msg += "\nError follows:\n{error}"
            msg = msg.format(file=filename, error=str(ex))
            raise CP3SlurmUtilsException(msg)
        for attr in modRef.__dict__.values():
            if isinstance(attr, Configuration):
                if confAttr is None:
                    confAttr = attr
                else:
                    msg = "ERROR: Configuration file contains more than one Configuration object."
                    raise ConfigurationException(msg)
    return confAttr
