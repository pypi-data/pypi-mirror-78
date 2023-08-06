#!/usr/bin/env python3
"""
________________________________________________________________________

:PROJECT: SiLA2_python

*SiLA2 code generator for packages*

:details: SiLA2 code generator that creates packages

:file:    sila2codegenerator.py
:authors: Timm Severin (timm.severin@tum.de)
          Mark Dörr (mark.doerr@uni-greifswald.de)

:date: (creation)          2018-05-22
:date: (last modification) 2019-11-04

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

# import general packages required
import os
import glob
import shutil
import argparse
import logging

# import meta packages
from typing import Union
from .__meta__ import __version__

# import sila2 packages specifically for the code generator
from sila2lib.fdl_parser.fdl_parser import FDLParser
from sila2lib.fdl_parser.fdl_validator import FDLValidator
from sila2lib.proto_builder.proto_builder import ProtoBuilder
from sila2lib.framework.utilities import copy_silastandard_proto
from sila2lib.proto_builder.proto_compiler import compile_proto_to_python, compile_proto_to_javascript

#   Function to build default arguments
from .PrototypeGenerator.generate_defaults import generate_default_dicts
#   Server/Client/Servicer Prototype generators
from .PrototypeGenerator.ServicerPrototypeGenerator import ServicerPrototypeGenerator
from .PrototypeGenerator.PyImplementationPrototypeGenerator import PyImplementationPrototypeGenerator
from .PrototypeGenerator.CppImplementationPrototypeGenerator import CppImplementationPrototypeGenerator
from .PrototypeGenerator.PyServerPrototypeGenerator import PyServerPrototypeGenerator
from .PrototypeGenerator.PyClientPrototypeGenerator import PyClientPrototypeGenerator
from .PrototypeGenerator.CppServerPrototypeGenerator import CppServerPrototypeGenerator
from .PrototypeGenerator.CppClientPrototypeGenerator import CppClientPrototypeGenerator
from .PrototypeGenerator.CppProjectPrototypeGenerator import CppProjectPrototypeGenerator
from .PrototypeGenerator.PrototypeGenerator import PrototypeGenerator

from .service_descriptor_parser import ServiceDescriptorParser


class SiLA2CodeGenerator:
    """SiLA2 CodeGenerator Class"""
    template_dir: str
    output_dir: str
    input_dir: str
    schema_file: str
    javascript: bool
    python: bool
    proto_generator: Union[ProtoBuilder, None]
    fdl_parser: Union[FDLParser, None]

    def __init__(self, parsed_args: Union[argparse.Namespace, None] = None):
        """Class constructor"""

        # Schema file, can be None, will be determined by the validator
        self.schema_file = parsed_args.fdl_schema

        self.ignore_overwrite_warning = parsed_args.ignore_overwrite_warning
        self.gen_javascript_stubs = parsed_args.gen_javascript_stubs
        self.gen_cpp = parsed_args.gen_cpp

        # input and output directory
        self.input_dir = parsed_args.project_dir
        self.output_dir = parsed_args.output_dir
        self.template_dir = parsed_args.template_dir

        # prepare fdl parser variable
        self.fdl_parser = None
        # prepare proto generator variable
        self.proto_generator = None
        # storage for a generated proto file
        self.proto_file = None

    def validate_fdl(self, input_file: str) -> bool:
        """Validation function used to evaluate XML/FDL files"""
        fdl_validator = FDLValidator(fdl_schema_file=self.schema_file)
        return fdl_validator.validate(input_file=input_file)

    def compile_fdl_to_proto(self, input_file: str, sub_dir: str = '.') -> str:
        self.fdl_parser = FDLParser(fdl_filename=input_file, fdl_schema_filename=self.schema_file)

        # create the proto builder
        self.proto_generator = ProtoBuilder(fdl_parser=self.fdl_parser)

        # return the generated filename
        self.proto_file = self.proto_generator.write_proto(proto_dir=os.path.join(self.output_dir, sub_dir))
        return self.proto_file

    def compile_proto_to_code(self, sub_dir: str = '.') -> bool:
        if self.proto_file is None:
            return False

        if self.gen_cpp:
            return True

        result = compile_proto_to_python(proto_file=os.path.basename(self.proto_file),
                               source_dir=os.path.dirname(self.proto_file),
                               target_dir=os.path.join(self.output_dir, sub_dir))
        if not result:
            # cancel if compilation failed
            return False

        if self.gen_javascript_stubs:
            logging.debug("now making javascript....")
            result = compile_proto_to_javascript(proto_file=os.path.basename(self.proto_file),
                                   source_dir=os.path.dirname(self.proto_file),
                                   target_dir=os.path.join(self.output_dir, sub_dir))
            if not result:
                # cancel if compilation failed
                return False

        # .. java / c# / ...

        # fix some imports in the generated files
        logging.debug('Fixing some import issues in the compiled python files.')
        # quite ugly - should be fixed by better solution - any suggestions?
        feature_id = os.path.basename(self.proto_file).split(os.extsep)[0]
        pb2_file = os.path.join(self.output_dir,
                                sub_dir,
                                str(feature_id) + '_pb2.py')
        pb2_grpc_file = os.path.join(self.output_dir,
                                     sub_dir,
                                     str(feature_id) + '_pb2_grpc.py')

        # # no correction necessary for this file
        # with open(pb2_file, 'r') as file_in:
        #     logging.debug('Correcting {file}'.format(file=pb2_file))
        #     logging.debug('\t' 'Correcting for import of SiLAFramework')
        #     replaced_text = file_in.read()
        # with open(pb2_file, 'w') as file_out:
        #     file_out.write(replaced_text)

        with open(pb2_grpc_file, 'r') as file_in:
            logging.debug('Correcting {file}'.format(file=pb2_grpc_file))
            logging.debug(
                (
                    '\t' 'Converting file imports to a package in file {file_name}: ' '\n'
                    '\t\t' '"import {feature_id}_pb2 -> from . import {feature_id}_pb2'
                ).format(file_name=pb2_grpc_file, feature_id=feature_id))
            replaced_text = file_in.read()
            replaced_text = replaced_text.replace(
                'import {feature_id}_pb2'.format(feature_id=feature_id),
                'from . import {feature_id}_pb2'.format(feature_id=feature_id)
            )
        with open(pb2_grpc_file, 'w') as file_out:
            file_out.write(replaced_text)

        return True

    def build_defaults(self, sub_dir: str = '.') -> bool:
        if self.gen_cpp:
            return True

        filename = '{feature_identifier}_default_arguments.py'.format(feature_identifier=self.fdl_parser.identifier)
        default_file = os.path.join(self.output_dir, sub_dir, filename)

        with open(default_file, 'w') as file_out:
            file_out.write((
                "# This file contains default values that are used for the implementations to supply them with " "\n"
                "#   working, albeit mostly useless arguments." "\n"
                "#   You can also use this file as an example to create your custom responses. Feel free to remove" "\n"
                "#   Once you have replaced every occurrence of the defaults with more reasonable values." "\n"
                "#   Or you continue using this file, supplying good defaults.." "\n"
                "\n"
                "# import the required packages" "\n"
                "import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2" "\n"
                "import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2" "\n"
                "from .gRPC import {feature_identifier}_pb2 as pb2" "\n"
                "\n"
                "# initialise the default dictionary so we can add keys. " "\n"
                "#   We need to do this separately/add keys separately, so we can access keys already defined e.g." "\n"
                "#   for the use in data type identifiers" "\n"
                "default_dict = dict()" "\n"
            ).format(feature_identifier=self.fdl_parser.identifier))
            file_out.write(generate_default_dicts(fdl_parser=self.fdl_parser))
            file_out.write('\n')

        return True

    def build_service(self, service_description: ServiceDescriptorParser, sub_dir: str = '.') -> bool:

        if not self.gen_cpp:
            # build the servicer
            sila_servicer_generator = ServicerPrototypeGenerator(
                fdl_input=self.fdl_parser,
                service_description=service_description,
                output_dir=os.path.join(self.output_dir, sub_dir),
                template_dir=self.template_dir,
                ignore_overwrite_warning=self.ignore_overwrite_warning
            )
            sila_servicer_generator.write_servicer_code(output_filename=None)

            # build the implementations
            for simulation_mode in [True, False]:
                sila_implementation_generator = PyImplementationPrototypeGenerator(
                    fdl_input=self.fdl_parser,
                    service_description=service_description,
                    output_dir=os.path.join(self.output_dir, sub_dir),
                    template_dir=self.template_dir,
                    simulation=simulation_mode,
                    ignore_overwrite_warning=self.ignore_overwrite_warning
                )
                sila_implementation_generator.write_implementation_code(output_filename=None)
        else:
            sila_implementation_generator = CppImplementationPrototypeGenerator(
                fdl_input=self.fdl_parser,
                service_description=service_description,
                output_dir=os.path.join(self.output_dir, sub_dir),
                template_dir=self.template_dir,
                ignore_overwrite_warning=self.ignore_overwrite_warning
            )
            sila_implementation_generator.write_implementation_code(output_filename=None)

        return True


def parse_command_line():
    """ Parse the command line arguments """

    # create the command line parser object
    parser = argparse.ArgumentParser(description="A SiLA2 code generator")

    # positional commandline arguments
    parser.add_argument('project_dir', action='store', default='.', metavar='PROJECT_DIR', nargs='?',
                        help='Project directory from which to read all input files for code generation. ' +
                             '(default: . [current directory])')

    # general optional arguments
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-o', '--output_dir', action='store', default=None,
                        help='Main output directory for the generated code. If not specified will be chosen '
                             'depending on the job at hand.')
    parser.add_argument('-s', '--fdl-schema', action='store', default=None,
                        help='XML/FDL validation schema, if not given the default SiLA2 schema will be used.')

    # conversion options
    parser.add_argument('-x', '--verify', action='store_true', dest="verify", help='Verify the XML/FDL input file.')
    parser.add_argument('-p', '--proto', action='store_true', dest="proto", help='Build proto files from XML/FDL.')
    parser.add_argument('-c', '--compile', action='store_true', dest="compile",
                        help='Compile the .proto files to language specific files. Implies --proto option.')
    parser.add_argument('-b', '--build', action='store_true', dest="build",
                        help='Build service prototype code (Python and C++ only). Implies --proto --compile option(s)')
    parser.add_argument('--ignore-overwrite-warning', action='store_true',
                        help='With this option you can ignore the overwrite warning during the build process.')
    parser.add_argument('--service-description', action='store', default='service_description',
                        help='Name of the .json file (without file ending) from which the service description is read. ' +
                             '(default: service_description).')
    # language choice arguments
    parser.add_argument('--javascript', action='store_true', dest='gen_javascript_stubs',
                        help='Compile proto also to JavaScript code/stubs ' + '(default: False).')
    parser.add_argument('--cpp', action='store_true', dest='gen_cpp',
                        help='Build service prototypes for C++ instead of Python (--compile option will be disregarded) ' + '(default: False).')
    # template related arguments
    parser.add_argument('--template', action='store', default='run-methods',
                        help='If --build option is given, this (package internal) template set is used to build the ' +
                             'servicer, implementations, server, and client. To get a list of all templates use the ' +
                             '--list-templates flag. Default: "run-methods" (or "cpp" when --cpp is used).')
    parser.add_argument('--template-dir', action='store', default="",
                        help="The path to a custom template directory. If given, will overwrite the --template flag.")
    parser.add_argument('--list-templates', action='store_true',
                        help='List all package internal template sets. Running this command will only print the ' +
                             'list and suppress all other actions.')

    parsed_args = parser.parse_args()

    # First parse all the arguments that end this script
    if parsed_args.list_templates:
        template_list = PrototypeGenerator.get_templates()
        print('Installed templates: ')
        for template in template_list:
            print('\t' + template)
        exit()

    # manually validate and/or update some inputs
    # --build implies --compile
    if parsed_args.build:
        parsed_args.compile = True

        if not os.path.isdir(parsed_args.project_dir) :
            logging.error(f"Build directory [{parsed_args.project_dir}] does not exist, please create it with a service descrition inside !")
            exit()

    # --compile implies --proto
    if parsed_args.compile:
        parsed_args.proto = True
    # --cpp uses 'cpp' template
    if parsed_args.gen_cpp:
        # no need to compile; C++ build system will take care of that
        parsed_args.compile = False
        parsed_args.template = "cpp"
    # template directory from template name if not given
    if not parsed_args.template_dir:
        template_dir = PrototypeGenerator.get_template_dir(parsed_args.template)
        if template_dir:
            parsed_args.template_dir = template_dir
            logging.debug('Set template dir to "{template_dir}"'.format(template_dir=template_dir))
        else:
            logging.error(
                (
                    'Given template name {template} does not exist inside the package.' '\n'
                    '    Use --list-templates argument to get a list of all valid templates'
                ).format(
                    template=parsed_args.template
                )
            )
            exit()

    return parsed_args


def main():
    """Main: """
    # set the logging
    #   consider logging.ERROR for less output
    logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging.INFO)

    # extract all arguments and create the code generator class fro it
    args = parse_command_line()

    # # Initialise variables
    # initialise the code_generator list variable for code generator objects
    code_generators = []

    # try to extract the data from the project_dir and there from the service description file
    logging.info('Using project directory and service description "{dir}/{service_description}.json" '
                 'as input source.'.format(dir=args.project_dir, service_description=args.service_description))
    # create a service descriptor
    service_descriptor = ServiceDescriptorParser(project_dir=args.project_dir, service_description=args.service_description)

    # extract all feature definitions that we want to work on, they never have a file ending
    fdl_input_files = [
        os.path.join(args.project_dir, item) + '.sila.xml'
        for item
        in service_descriptor.description_dictionary['SiLA_feature_list']
    ]

    # set the output dir automatically if none is given
    if args.output_dir is None:
        args.output_dir = service_descriptor.description_dictionary['service_name']

    logging.debug(f"in: {fdl_input_files} \n out:{args.output_dir}")

    # now we have prepared everything so we can actually parse the data
    # verification of xml input based on the service_description
    if args.verify:
        code_generator = SiLA2CodeGenerator(args)

        logging.info('Verifying input files.')
        # copy our input list and clear it, so we can re-add only the elements that actually validate
        list_iterator = fdl_input_files[:]
        fdl_input_files[:] = []
        for fdl_file in list_iterator:
            if code_generator.validate_fdl(fdl_file):
                fdl_input_files.append(fdl_file)
                logging.info('Input file {fdl_file} successfully validated.'.format(fdl_file=fdl_file))
            else:
                logging.error('Input file {fdl_file} failed to validate. It will not be processed further.'.format(
                    fdl_file=fdl_file))
        logging.info('Verification completed.')

    # generate proto files
    if args.proto:
        logging.info('Creating .proto files.')
        # prepare a list of code generator objects for each fdl-file
        code_generators = [SiLA2CodeGenerator(args) for _ in fdl_input_files]

        # we work with sub-directories
        target_dir = 'meta'
        # we must make sure the output directory exists
        os.makedirs(os.path.join(args.output_dir, target_dir), exist_ok=True)

        # generate the proto files
        for fdl_file, code_generator in zip(fdl_input_files, code_generators):
            logging.debug('Converting {fdl_file}'.format(fdl_file=fdl_file))
            code_generator.compile_fdl_to_proto(input_file=fdl_file, sub_dir=target_dir)

            # also copy the base file in that folder just for completeness
            shutil.copy(fdl_file, os.path.join(args.output_dir, target_dir))

        if not args.gen_cpp:
            # python also needs the base framework proto file
            copy_silastandard_proto(target_dir=os.path.join(args.output_dir, target_dir))

        logging.info('.proto file generation complete.')

    # compile the proto files
    if args.compile:
        logging.info('Compiling proto files to code.')
        for code_generator in code_generators:
            logging.debug('Compiling feature {proto_file}'.format(proto_file=code_generator.proto_file))
            # we work with sub-directories, these are - in this case - specific for the different files, so we can use
            # package options
            target_dir = os.path.join(str(os.path.basename(code_generator.proto_file).split(os.extsep)[0]), 'gRPC')
            # we must make sure the output directory exists
            os.makedirs(os.path.join(args.output_dir, target_dir), exist_ok=True)

            # generate the compiled gRPC files
            code_generator.compile_proto_to_code(sub_dir=target_dir)

            # prepare the folder for usage as a package (create a __init__.py)
            open(os.path.join(args.output_dir, target_dir, '__init__.py'), 'a').close()
        logging.info('Code generation completed.')

    # build the prototype client, server, servicer and implementations
    if args.build:
        logging.info('Building service prototype.')

        # each code generator has the context to one feature
        for fdl_file, code_generator in zip(fdl_input_files, code_generators):
            # use the correct sub-directory
            target_dir = str(os.path.basename(fdl_file).split(os.extsep)[0])
            # make sure the output directory exists
            os.makedirs(os.path.join(args.output_dir, target_dir), exist_ok=True)

            # first build the file with the default arguments that will be used in the servicer and implementations
            code_generator.build_defaults(sub_dir=target_dir)

            code_generator.build_service(service_description=service_descriptor, sub_dir=target_dir)

            if not args.gen_cpp:
                # prepare the folder for usage as a package (create a __init__.py)
                open(os.path.join(args.output_dir, target_dir, '__init__.py'), 'a').close()

        # build the server and the client
        meta_dir = 'meta'

        # parsed_args.ignore_overwrite_warning
        ServerPrototypeGenerator = PyServerPrototypeGenerator if not args.gen_cpp else CppServerPrototypeGenerator
        sila_server_generator = ServerPrototypeGenerator(
            service_description=service_descriptor,
            output_dir=args.output_dir,
            template_dir=args.template_dir,
            fdl_path=args.project_dir,
            ignore_overwrite_warning=args.ignore_overwrite_warning
        )
        # parsed_args.ignore_overwrite_warning
        sila_server_generator.write_server_code(output_filename=None, meta_path=meta_dir)

        # parsed_args.ignore_overwrite_warning
        ClientPrototypeGenerator = PyClientPrototypeGenerator if not args.gen_cpp else CppClientPrototypeGenerator
        sila_client_generator = ClientPrototypeGenerator(
            service_description=service_descriptor,
            output_dir=args.output_dir,
            template_dir=args.template_dir,
            fdl_path=args.project_dir,
            ignore_overwrite_warning=args.ignore_overwrite_warning
        )
        # parsed_args.ignore_overwrite_warning
        sila_client_generator.write_client_code(output_filename=None)

        if args.gen_cpp:
            # we also need project files
            project_generator = CppProjectPrototypeGenerator(
                service_description=service_descriptor,
                output_dir=args.output_dir,
                template_dir=args.template_dir,
                fdl_path=args.project_dir,
                meta_dir=meta_dir,
                ignore_overwrite_warning=args.ignore_overwrite_warning
            )
            project_generator.write_project_code()

        logging.info('Prototype finished.')


if __name__ == '__main__':
    main()
