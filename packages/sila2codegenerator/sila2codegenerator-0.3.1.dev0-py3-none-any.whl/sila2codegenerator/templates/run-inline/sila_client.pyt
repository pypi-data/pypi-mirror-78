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

    def run(self):
        # type definition, just for convenience
        # noinspection PyUnusedLocal
        grpc_err: grpc.Call
        try:
            # Run the framework commands as a test
            logging.info("SiLA client ${service_name} - SiLA Framework commands:")

            logging.info(" " * 4 + "Retrieving the list of implemented features of the server:")
            response = self.SiLAService_stub.Get_ImplementedFeatures(SiLAService_feature_pb2.Get_ImplementedFeatures_Parameters())
            for feature_id in response.ImplementedFeatures:
                logging.info(" " * 8 + "Implemented feature: {feature_id}".format(
                    feature_id=feature_id.value)
                    )

            logging.info(" " * 4 + "Requesting feature definitions:")
            try:
                response = self.SiLAService_stub.GetFeatureDefinition(
                    SiLAService_feature_pb2.GetFeatureDefinition_Parameters(
                        QualifiedFeatureIdentifier=${sila_framework}.String(value="SiLAService")
                        )
                    )
                logging.info(" " * 8 + "Response of GetFeatureDefinition for SiLAService feature: {response}".format(
                        response=response)
                )
            except grpc.RpcError as grpc_err:
                logging.error(" " * 8 + "gRPC/SiLA error: {error}".format(error=grpc_err))

            logging.info(" " * 4 + "Requesting feature definitions:")
            try:
                logging.info('NOTE: The following call is supposed to produce an error:')
                response = self.SiLAService_stub.GetFeatureDefinition(
                    SiLAService_feature_pb2.GetFeatureDefinition_Parameters(
                        QualifiedFeatureIdentifier=${sila_framework}.String(value="NoFeature")
                        )
                    )
                logging.debug(" " * 8 + "Response of GetFeatureDefinition for NoFeature feature: {response}".format(
                        response=response)
                )
            except grpc.RpcError as grpc_err:
                logging.error(" " * 8 + "(Expected) gRPC/SiLA error: {error}".format(error=grpc_err))

            logging.info(" " * 4 + "Requesting meta information of the server:")
            response = self.SiLAService_stub.Get_ServerName(SiLAService_feature_pb2.Get_ServerName_Parameters())
            logging.info(" " * 8 + "Display name: {name}".format(name=response.ServerName.value))

            response = self.SiLAService_stub.Get_ServerDescription(SiLAService_feature_pb2.Get_ServerDescription_Parameters())
            logging.info(" " * 8 + "Description: {description}".format(description=response.ServerDescription.value))

            response = self.SiLAService_stub.Get_ServerVersion(SiLAService_feature_pb2.Get_ServerVersion_Parameters())
            logging.info(" " * 8 + "Version: {version}".format(version=response.ServerVersion.value))

            # Run all defined commands
${indent(12):command_calls}

            # Get all defined properties
${indent(12):property_calls}

        except grpc.RpcError as grpc_err:
            logging.exception(
                (
                    'Error during gRPC communication.' '\n'
                    '\t' 'Status code: {error_code}' '\n'
                    '\t' 'Details: {error_details}' '\n'

                ).format(error_code=grpc_err.code(), error_details=grpc_err.details())
            )

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
