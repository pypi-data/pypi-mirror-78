#!/usr/bin/env python3
"""
________________________________________________________________________

:PROJECT: SiLA2_python

*${service_name} client*

:details: ${service_name}:
${indent(4):wrap(116):trim(True,True):service_description}

:file:    ${output_filename}
:authors: ${authors}

:date: (creation)          ${creation_date}
:date: (last modification) ${creation_date}

.. note:: ${note}

_______________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""
__version__ = "${version}"

# import general packages
import logging
import argparse
import grpc
import time

# import meta packages
from typing import Union, Optional

# import SiLA2 library modules
from sila2lib.framework import SiLAFramework_pb2 as ${sila_framework}
from sila2lib.sila_client import SiLA2Client
from sila2lib.framework.std_features import SiLAService_pb2 as SiLAService_feature_pb2
from sila2lib.error_handling import client_err
#   Usually not needed, but - feel free to modify
# from sila2lib.framework.std_features import SimulationController_pb2 as SimController_feature_pb2

# import feature gRPC modules
${import_grpc_modules}


# noinspection PyPep8Naming, PyUnusedLocal
class ${service_name}Client(SiLA2Client):
    """
    ${indent(4):trim(True,False):service_description}

    .. note:: For an example on how to construct the parameter or read the response(s) for command calls and properties,
              compare the default dictionary that is stored in the directory of the corresponding feature.
    """
    # The following variables will be filled when run() is executed
    #: Storage for the connected servers version
    server_version: str = ''
    #: Storage for the display name of the connected server
    server_display_name: str = ''
    #: Storage for the description of the connected server
    server_description: str = ''

    def __init__(self,
                 name: str = "${service_name}Client", description: str = "${service_description}",
                 server_name: Optional[str] = None,
                 client_uuid: Optional[str] = None,
                 version: str = __version__,
                 vendor_url: str = "${vendor_url}",
                 server_hostname: str = "${hostname}", server_ip: str = "${IP_address}", server_port: int = ${communication_port},
                 cert_file: Optional[str] = None):
        """Class initialiser"""
        super().__init__(
            name=name, description=description,
            server_name=server_name,
            client_uuid=client_uuid,
            version=version,
            vendor_url=vendor_url,
            server_hostname=server_hostname, server_ip=server_ip, server_port=server_port,
            cert_file=cert_file
        )

        logging.info(
            "Starting SiLA2 service client for service ${service_name} with service name: {server_name}".format(
                server_name=name
            )
        )

        # Create stub objects used to communicate with the server
${indent(8):stub_creation}

        # initialise class variables for server information storage
        self.server_version = ''
        self.server_display_name = ''
        self.server_description = ''

    def Get_ImplementedFeatures(self):
        """Get a list of all implemented features."""
        # type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug("Retrieving the list of implemented features of the server:")
        try:
            response = self.SiLAService_stub.Get_ImplementedFeatures(
                SiLAService_feature_pb2.Get_ImplementedFeatures_Parameters()
            )
            for feature_id in response.ImplementedFeatures:
                logging.debug("Implemented feature: {feature_id}".format(
                    feature_id=feature_id.value)
                    )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return response.ImplementedFeatures

    def Get_FeatureDefinition(self, feature_identifier: str) -> Union[str, None]:
        """
        Returns the FDL/XML feature definition of the given feature.

        :param feature_identifier: The name of the feature for which the definition should be returned.
        """
        # type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug("Requesting feature definitions of feature {feature_identifier}:".format(
            feature_identifier=feature_identifier)
        )
        try:
            response = self.SiLAService_stub.GetFeatureDefinition(
                SiLAService_feature_pb2.GetFeatureDefinition_Parameters(
                    QualifiedFeatureIdentifier=${sila_framework}.String(value=feature_identifier)
                    )
                )
            logging.debug("Response of GetFeatureDefinition for {feature_identifier} feature: {response}".format(
                response=response,
                feature_identifier=feature_identifier)
            )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

    def run(self) -> bool:
        """
        Starts the actual client and retrieves the meta-information from the server.

        :returns: True or False whether the connection to the server is established.
        """
        # type definition, just for convenience
        grpc_err: grpc.Call

        try:
            # Retrieve the basic server information and store it in internal class variables
            #   Display name
            response = self.SiLAService_stub.Get_ServerName(SiLAService_feature_pb2.Get_ServerName_Parameters())
            self.server_display_name = response.ServerName.value
            logging.debug("Display name: {name}".format(name=response.ServerName.value))
            # Server description
            response = self.SiLAService_stub.Get_ServerDescription(
                SiLAService_feature_pb2.Get_ServerDescription_Parameters()
            )
            self.server_description = response.ServerDescription.value
            logging.debug("Description: {description}".format(description=response.ServerDescription.value))
            # Server version
            response = self.SiLAService_stub.Get_ServerVersion(SiLAService_feature_pb2.Get_ServerVersion_Parameters())
            self.server_version = response.ServerVersion.value
            logging.debug("Version: {version}".format(version=response.ServerVersion.value))
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return False

        return True

    def stop(self, force: bool = False) -> bool:
        """
        Stop SiLA client routine

        :param force: If set True, the client is supposed to disconnect and stop immediately. Otherwise it can first try
                      to finish what it is doing.

        :returns: Whether the client could be stopped successfully or not.
        """
        # TODO: Implement all routines that have to be executed when the client is stopped.
        #   Feel free to use the "force" parameter to abort any running processes. Or crash your machine. Your call!
        return True

${indent(4):command_calls}

${indent(4):property_calls}

    @staticmethod
    def grpc_error_handling(error_object: grpc.Call) -> None:
        """Handles exceptions of type grpc.RpcError"""
        # pass to the default error handling
        grpc_error =  client_err.grpc_error_handling(error_object=error_object)

        # Access more details using the return value fields
        # grpc_error.message
        # grpc_error.error_type


def parse_command_line():
    """
    Just looking for command line arguments
    """
    parser = argparse.ArgumentParser(description="A SiLA2 client: ${service_name}")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    return parser.parse_args()


if __name__ == '__main__':
    # or use logging.INFO (=20) or logging.ERROR (=30) for less output
    logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging.DEBUG)

    parsed_args = parse_command_line()

    # start the server
    sila_client = ${service_name}Client(server_ip='${IP_address}', server_port=${communication_port})
    sila_client.run()

    # Log connection info
    logging.info(
        (
            'Connected to SiLA Server {display_name} running in version {version}.' '\n'
            'Service description: {service_description}'
        ).format(
            display_name=sila_client.server_display_name,
            version=sila_client.server_version,
            service_description=sila_client.server_description
        )
    )

    # TODO:
    #   Write your further function calls here to run the client as a standalone application.
