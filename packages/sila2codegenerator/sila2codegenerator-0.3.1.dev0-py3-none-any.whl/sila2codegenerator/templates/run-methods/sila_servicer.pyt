"""
________________________________________________________________________

:PROJECT: SiLA2_python

*${feature_name}*

:details: ${feature_identifier}:
${indent(4):wrap(116):trim(True,True):feature_description}
           
:file:    ${output_filename}
:authors: ${authors}

:date: (creation)          ${creation_date}
:date: (last modification) ${creation_date}

.. note:: ${note}

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

__version__ = "${version}"

# import general packages
import logging
import grpc

# meta packages
from typing import Union

# import SiLA2 library
import sila2lib.framework.SiLAFramework_pb2 as ${sila_framework}
from sila2lib.error_handling.server_err import SiLAError

# import gRPC modules for this feature
from .gRPC import ${feature_identifier}_pb2 as ${feature_identifier}_pb2
from .gRPC import ${feature_identifier}_pb2_grpc as ${feature_identifier}_pb2_grpc

# import simulation and real implementation
from .${feature_identifier}_simulation import ${feature_identifier}Simulation
from .${feature_identifier}_real import ${feature_identifier}Real


class ${feature_identifier}(${feature_identifier}_pb2_grpc.${feature_identifier}Servicer):
    """
${indent(4):trim(True,False):service_description}
    """
    implementation: Union[${feature_identifier}Simulation, ${feature_identifier}Real]
    simulation_mode: bool

    def __init__(self, simulation_mode: bool = True):
        """
        Class initialiser.

        :param simulation_mode: Sets whether at initialisation the simulation mode is active or the real mode.
        """

        self.simulation_mode = simulation_mode
        if simulation_mode:
            self._inject_implementation(${feature_identifier}Simulation())
        else:
            self._inject_implementation(${feature_identifier}Real())

    def _inject_implementation(self,
                               implementation: Union[${feature_identifier}Simulation,
                                                     ${feature_identifier}Real]
                               ) -> bool:
        """
        Dependency injection of the implementation used.
            Allows to set the class used for simulation/real mode.

        :param implementation: A valid implementation of the ${service_name}Servicer.
        """

        self.implementation = implementation
        return True

    def switch_to_simulation_mode(self):
        """Method that will automatically be called by the server when the simulation mode is requested."""
        self.simulation_mode = True
        self._inject_implementation(${feature_identifier}Simulation())

    def switch_to_real_mode(self):
        """Method that will automatically be called by the server when the real mode is requested."""
        self.simulation_mode = False
        self._inject_implementation(${feature_identifier}Real())

${indent(4):commands_servicer}

${indent(4):properties_servicer}
