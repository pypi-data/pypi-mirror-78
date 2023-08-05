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

class CP3SlurmUtilsException(Exception):
    """ General exception """
    pass


class ConfigurationException(CP3SlurmUtilsException):
    pass
