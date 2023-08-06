#!/usr/bin/env python3
"""
________________________________________________________________________

:PROJECT: SiLA2_python

*${service_name}*

:details: ${service_name}:
${indent(4):wrap(116):trim(True,True):service_description}
           
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

import logging
import argparse

# Import the main SiLA library
from sila2lib.sila_server import SiLA2Server

${import_grpc_modules}

${import_servicer_modules}


class ${service_name}Server(SiLA2Server):
    """
${indent(4):trim(True,False):service_description}
    """

    def __init__(self, cmd_args, simulation_mode: bool = True):
        """Class initialiser"""
        super().__init__(
            name=cmd_args.server_name, description=cmd_args.description,
            server_type=cmd_args.server_type, server_uuid=None,
            version=__version__,
            vendor_url="${vendor_url}",
            ip="${IP_address}", port=${communication_port},
            key_file=cmd_args.encryption_key, cert_file=cmd_args.encryption_cert
        )

        logging.info(
            "Starting SiLA2 server with server name: {server_name}".format(
                server_name=cmd_args.server_name
            )
        )

        # registering features
${indent(8):feature_registration}

        self.simulation_mode = simulation_mode

        # starting and running the gRPC/SiLA2 server
        self.run()


def parse_command_line():
    """
    Just looking for commandline arguments
    """
    parser = argparse.ArgumentParser(description="A SiLA2 service: ${service_name}")

    # Simple arguments for the server identification
    parser.add_argument('-s', '--server-name', action='store',
                        default="${service_name}", help='start SiLA server with [server-name]')
    parser.add_argument('-t', '--server-type', action='store',
                        default="${service_type}", help='start SiLA server with [server-type]')
    parser.add_argument('-d', '--description', action='store',
                        default="${service_description}", help='SiLA server description')

    # Encryption
    parser.add_argument('-X', '--encryption', action='store', default=None,
                        help='The name of the private key and certificate file (without extension).')
    parser.add_argument('--encryption-key', action='store', default=None,
                        help='The name of the encryption key (*with* extension). Can be used if key and certificate '
                             'vary or non-standard file extensions are used.')
    parser.add_argument('--encryption-cert', action='store', default=None,
                        help='The name of the encryption certificate (*with* extension). Can be used if key and '
                             'certificate vary or non-standard file extensions are used.')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    parsed_args = parser.parse_args()

    # validate/update some settings
    #   encryption
    if parsed_args.encryption is not None:
        # only overwrite the separate keys if not given manually
        if parsed_args.encryption_key is None:
            parsed_args.encryption_key = parsed_args.encryption + '.key'
        if parsed_args.encryption_cert is None:
            parsed_args.encryption_cert = parsed_args.encryption + '.cert'

    return parsed_args
    
        
if __name__ == '__main__':
    # or use logging.ERROR for less output
    logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging.DEBUG)
    
    args = parse_command_line()

    # generate SiLA2Server
    sila_server = ${service_name}Server(cmd_args=args, simulation_mode=True)
