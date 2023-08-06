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
import time         # used for observables
import uuid         # used for observables
import grpc         # used for type hinting only

# import SiLA2 library
import sila2lib.framework.SiLAFramework_pb2 as ${sila_framework}

# import gRPC modules for this feature
from .gRPC import ${feature_identifier}_pb2 as ${feature_identifier}_pb2
# from .gRPC import ${feature_identifier}_pb2_grpc as ${feature_identifier}_pb2_grpc

# import default arguments
from .${feature_identifier}_default_arguments import default_dict


# noinspection PyPep8Naming,PyUnusedLocal
class ${feature_identifier}${implementation_mode}:
    """
    Implementation of the *${feature_name}* in *${implementation_mode}* mode
    ${indent(4):trim(True,False):service_description}
    """

    def __init__(self):
        """Class initialiser"""

        logging.debug('Started server in mode: {mode}'.format(mode='${implementation_mode}'))

    def _get_command_state(self, command_uuid: str) -> ${sila_framework}.ExecutionInfo:
        """
        Method to fill an ExecutionInfo message from the SiLA server for observable commands

        :param command_uuid: The uuid of the command for which to return the current state

        :return: An execution info object with the current command state
        """

        #: Enumeration of ${sila_framework}.ExecutionInfo.CommandStatus
        command_status = ${sila_framework}.ExecutionInfo.CommandStatus.waiting
        #: Real ${sila_framework}.Real(0...1)
        command_progress = None
        #: Duration ${sila_framework}.Duration(seconds=<seconds>, nanos=<nanos>)
        command_estimated_remaining = None
        #: Duration ${sila_framework}.Duration(seconds=<seconds>, nanos=<nanos>)
        command_lifetime_of_execution = None

        # TODO: check the state of the command with the given uuid and return the correct information

        # just return a default in this example
        return ${sila_framework}.ExecutionInfo(
            commandStatus=command_status,
            progressInfo=(
                command_progress if command_progress is not None else None
            ),
            estimatedRemainingTime=(
                command_estimated_remaining if command_estimated_remaining is not None else None
            ),
            updatedLifetimeOfExecution=(
                command_lifetime_of_execution if command_lifetime_of_execution is not None else None
            )
        )

${indent(4):commands_implementation}

${indent(4):properties_implementation}
