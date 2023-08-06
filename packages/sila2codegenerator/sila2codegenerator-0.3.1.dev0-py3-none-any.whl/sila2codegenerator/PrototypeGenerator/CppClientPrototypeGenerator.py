"""
________________________________________________________________________

:PROJECT: SiLA2_python

*SiLA2 Code Generator for using Packages*

:details: Class to generate C++ client prototypes of a SiLA2 Client/Server

:file:    CppPrototypeGenerator.py
:authors: Florian Meinicke (florian.meinicke@cetoni.de)
          Timm Severin (timm.severin@tum.de)
          mark doerr  (mark.doerr@uni-greifswald.de)

:date: (creation)          2020-08-12
:date: (last modification) 2020-08-12

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

# import general modules
import os
from datetime import date

# import modules from this package
from ..service_descriptor_parser import ServiceDescriptorParser
from .PrototypeGenerator import PrototypeGenerator

# meta information packages
from typing import Union, Dict

# import helper
from .cpp_namespace_helper import generate_namespaces

class CppClientPrototypeGenerator(PrototypeGenerator):
    """TODO: Document"""

    def __init__(self,
                 service_description: Union[ServiceDescriptorParser, None] = None,
                 output_dir: Union[str, None] = None,
                 template_dir: Union[str, None] = None,
                 fdl_path: str = '.',
                 ignore_overwrite_warning: bool = False):
        """
        Class initialiser

        :param fdl_path: Path to where **all** FDL input files are stored

        .. note:: For parameter descriptions compare initialiser :meth:`.PrototypeGenerator.__init__`
        """

        super().__init__(
            service_description=service_description,
            output_dir=output_dir,
            template_dir=template_dir,
            fdl_path=fdl_path,
            ignore_overwrite_warning=ignore_overwrite_warning
        )

    def _generate_command_calls(self) -> str:
        """
        Generate the command calls to all features

        :return: The code to call all features
        """

        code_command_calls = ""

        for feature_id in self.service_dict['SiLA_feature_list']:
            for identifier, command in self.fdl_parsers[feature_id].commands.items():
                # distinguish between the different command variants
                if command.observable and command.intermediates:
                    # observable and defined intermediates
                    template_file = 'command_observable_intermediate_call'
                elif command.observable and not command.intermediates:
                    # observable without any intermediates defined
                    template_file = 'command_observable_no-intermediate_call'
                else:
                    # unobservable
                    template_file = 'command_unobservable_call'

                parameter_description, response_description = \
                    self._generate_parameters_responses_description(command)

                code_command_calls += self.generate_from_template({
                        'feature_identifier': feature_id,
                        'command_id': identifier,
                        'command_name': command.name,
                        'command_description': command.description,
                        'parameters_description': parameter_description,
                        'responses_description': response_description
                    },
                    input_template=template_file,
                    template_ext=self.CPP_TEMPLATE_EXTENSION
                ) + "\n\n"

        code_command_calls = code_command_calls[:-1]

        return code_command_calls

    def _generate_property_calls(self):
        """
        Generate the code to retrieve all properties

        :return: The code to send property requests to the server
        """

        code_property_calls = ""

        for feature_id in self.service_dict['SiLA_feature_list']:
            for identifier, property_object in self.fdl_parsers[feature_id].properties.items():
                # distinguish between the different command variants
                if property_object.observable:
                    # observable and defined intermediates
                    template_file = 'property_observable_call'
                else:
                    # unobservable
                    template_file = 'property_unobservable_call'

                code_property_calls += self.generate_from_template({
                        'feature_identifier': feature_id,
                        'property_id': identifier,
                        'property_name': property_object.name,
                        'property_description': property_object.description,
                    },
                    input_template=template_file,
                    template_ext=self.CPP_TEMPLATE_EXTENSION
                ) + "\n\n"

        code_property_calls = code_property_calls[:-2]

        if not code_property_calls:
            code_property_calls = "// No properties defined"

        return code_property_calls

    def _generate_stubs(self, form: str) -> str:
        """
        Creates the code to initialise the stub objects for the client

        :param form: Either 'creation' or 'declaration'

        :return: The stub code
        """

        code_stubs = ""

        for feature_id in self.service_dict['SiLA_feature_list']:
            code_stubs += self.generate_from_template({
                    'feature_identifier': feature_id
                },
                input_template="stub_" + form,
                template_ext=self.CPP_TEMPLATE_EXTENSION
            ) + "\n"

        # discard last newline and in case of `creation` also the last comma
        code_stubs = code_stubs[:-1] if form == 'declaration' else code_stubs[:-2]

        return code_stubs

    def _generate_grpc_includes(self) -> str:
        """
        Generate the code to include the gRPC header for each feature

        :return: The include code
        """

        code_import = "// include the gRPC classes for the SiLA Features"

        for feature_id in self.service_dict['SiLA_feature_list']:
            code_import += "\n" + self.generate_from_template({
                    'feature_identifier': feature_id
                },
                input_template='include_grpc',
                template_ext=self.CPP_TEMPLATE_EXTENSION
            )

        return code_import

    def _generate_using_namespaces(self) -> str:
        """
        Generate the code for using the feature namespaces

        :return: The code containing a `using namespace` for each feature
        """
        code_ns_aliases = ""
        for feature_id in self.service_dict['SiLA_feature_list']:
            namespace = '::'.join(generate_namespaces(self.fdl_parsers[feature_id]))
            code_ns_aliases += self.generate_from_template({
                'feature_namespace': namespace
            },
            input_template="using_feature_namespaces",
            template_ext=self.CPP_TEMPLATE_EXTENSION)
            code_ns_aliases += '\n'

        return code_ns_aliases

    def _generate_convenience_functions(self) -> str:
        """
        Generate the implementations for convenience functions that can construct complex
        gRPC types from C++ plain data types.

        :return: The code for the convenience functions implementations
        """
        return ""

    def write_client_code(self, output_filename: Union[str, None] = None):
        """
        This method builds a client class from a template.
            The resulting file can be run as SiLA client for the implemented features.

        :param output_filename: filename for server output file
        """

        # initialise variables
        template_vars = {
            'creation_date': date.today().isoformat()
        }

        # configuration options
        template_filename = "sila_client"
        if output_filename is None:
            output_filename = '{service_name}Client.cpp'.format(
                service_name=str(self.service_dict['service_name'])
            )

        self.write_from_template(template_vars,
                                 command_calls=self._generate_command_calls(),
                                 property_calls=self._generate_property_calls(),
                                 stub_creation=self._generate_stubs('creation'),
                                 stub_declaration=self._generate_stubs('declaration'),
                                 include_grpc=self._generate_grpc_includes(),
                                 using_feature_namespaces=self._generate_using_namespaces(),
                                 convenience_functions=self._generate_convenience_functions(),
                                 output_filename=output_filename,
                                 input_template=template_filename,
                                 template_ext=self.CPP_TEMPLATE_EXTENSION
        )
