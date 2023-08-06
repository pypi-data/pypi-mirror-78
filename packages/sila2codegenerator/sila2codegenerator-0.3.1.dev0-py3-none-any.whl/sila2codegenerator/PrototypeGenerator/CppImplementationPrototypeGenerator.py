"""
________________________________________________________________________

:PROJECT: SiLA2_python

*SiLA2 Code Generator for using Packages*

:details: Class to generate C++ implementation prototypes of a SiLA2 Client/Server

:file:    CppImplementationPrototypeGenerator.py
:authors: Florian Meinicke (florian.meinicke@cetoni.de)
          Timm Severin (timm.severin@tum.de)

:date: (creation)          2020-08-12
:date: (last modification) 2020-08-12

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

# import the general packages required
from datetime import date
import logging

# import modules from this package
from ..service_descriptor_parser import ServiceDescriptorParser
from .FDLPrototypeGenerator import FDLPrototypeGenerator

# import packages from the SiLA2 library
from sila2lib.fdl_parser.fdl_parser import FDLParser
from sila2lib.fdl_parser.data_type_intermediate import IntermediateDataType
from sila2lib.fdl_parser.data_type_response import ResponseDataType
from sila2lib.fdl_parser.type_basic import BasicType
from sila2lib.fdl_parser.type_list import ListType
from sila2lib.fdl_parser.type_base import DataType
from sila2lib.fdl_parser.command import Command
from sila2lib.fdl_parser.property import Property
from sila2lib.smart_template.hooks.code import indent

# meta information packages
from typing import Union
from typing import Dict

# import helper
from .cpp_namespace_helper import generate_namespaces


class CppImplementationPrototypeGenerator(FDLPrototypeGenerator):
    """TODO: Document"""

    simulation: bool

    def __init__(self,
                 fdl_input: Union[str, FDLParser],
                 service_description: Union[ServiceDescriptorParser, None] = None,
                 output_dir: Union[str, None] = None,
                 template_dir: Union[str, None] = None,
                 ignore_overwrite_warning: bool = False):
        """
        Class initialiser

        :param fdl_input: Either a reference to an FDLParser object (sila2lib.fdl_parser) or a string to an FDL
                          file. This is used to extract further information on methods and properties of the server

        .. note:: For further parameter descriptions compare initialiser :meth:`.PrototypeGenerator.__init__`
        """
        super().__init__(
            fdl_input=fdl_input,
            service_description=service_description,
            output_dir=output_dir,
            template_dir=template_dir,
            ignore_overwrite_warning=ignore_overwrite_warning
        )
        self.substitution_dict['feature_namespace'] = '::'.join(generate_namespaces(self.fdl_parser))
        self.substitution_dict['full_feature_identifier'] = \
            '::'.join([self.substitution_dict['feature_namespace'], self.fdl_parser.identifier])

    def _get_command_template_name(self, command: Command) -> str:
        """
        Helper to distinguish between the different command variants and choose
        the corresponding template file
        """
        if command.observable and command.intermediates:
            # observable and defined intermediates
            return 'command_observable_intermediate'
        elif command.observable and not command.intermediates:
            # observable without any intermediates defined
            return 'command_observable_no-intermediate'
        else:
            # unobservable
            return 'command_unobservable'

    def _get_property_template_name(self, prop: Property) -> str:
        """
        Helper to distinguish between the different property variants and choose
        the corresponding template file
        """
        if prop.observable:
            return 'property_observable'
        else:
            return 'property_unobservable'

    def _get_underlying_type(self, prop: Property) -> str:
        """
        Helper to get the underlying type of a property
        This will return the complete C++ type
        """
        # Go down the tree of sub_types to the very last type
        # (is always a SiLA Basic Type)
        underlying_type = prop.response
        underlying_type_str = "{underlying_type}"
        basic_type_str = "SiLA2::C{basic_type}"
        while not isinstance(underlying_type, BasicType):
            if isinstance(underlying_type, ListType):
                underlying_type_str = underlying_type_str.format(
                    underlying_type="std::vector<{underlying_type}>"
                )
            try:
                underlying_type = underlying_type.sub_type
            except AttributeError:
                logging.warning(
                    "sila_cpp does not yet support Properties with Structures or Custom Data Type Definitions"
                )
                return underlying_type

        return underlying_type_str.format(underlying_type=basic_type_str.format(
            basic_type=underlying_type.sub_type
        ))

    def _generate_commands_include(self) -> str:
        """
        Generates the necessary includes for the commands of this feature
        """
        code_includes = ""
        has_unobservable_commands = False
        has_observable_commands = False

        for command in self.fdl_parser.commands.values():
            has_unobservable_commands |= not command.observable
            has_observable_commands |= command.observable

        if has_unobservable_commands:
            code_includes += "#include <sila_cpp/server/command/UnobservableCommand.h>"
            if has_observable_commands:
                code_includes += '\n'
        if has_observable_commands:
            code_includes += "#include <sila_cpp/server/command/ObservableCommand.h>"

        return code_includes

    def _generate_properties_include(self) -> str:
        """
        Generates the necessary includes for the properties of this feature
        """
        code_includes = ""
        has_unobservable_properties = False
        has_observable_properties = False

        for prop in self.fdl_parser.properties.values():
            has_unobservable_properties |= not prop.observable
            has_observable_properties |= prop.observable

        if has_unobservable_properties:
            code_includes += "#include <sila_cpp/server/property/UnobservableProperty.h>"
            if has_observable_properties:
                code_includes += '\n'
        if has_observable_properties:
            code_includes += "#include <sila_cpp/server/property/ObservableProperty.h>"

        return code_includes

    def _generate_commands_alias(self) -> str:
        """
        Generates the using aliases for every command manager and wrapper
        """
        code_aliases = ""
        for identifier, command in self.fdl_parser.commands.items():
            template_file = self._get_command_template_name(command) + '_alias'

            code_aliases += self.generate_from_template({
                    'command_id': identifier
                },
                input_template=template_file,
                template_ext=self.CPP_TEMPLATE_EXTENSION
            ) + '\n'

        code_aliases = code_aliases[:-1]

        return code_aliases

    def _generate_properties_alias(self) -> str:
        """
        Generates the using aliases for every property wrapper
        """
        code_aliases = ""
        for identifier, prop in self.fdl_parser.properties.items():
            template_file = self._get_property_template_name(prop) + '_alias'

            code_aliases += self.generate_from_template({
                    'property_id': identifier,
                    'underlying_type': self._get_underlying_type(prop)
                },
                input_template=template_file,
                template_ext=self.CPP_TEMPLATE_EXTENSION
            ) + '\n'

        code_aliases = code_aliases[:-1]

        return code_aliases

    def _generate_commands_declaration(self) -> str:
        """
        Generates the declarations for command executor functions
        """
        code_declarations = ""
        for command_id, command in self.fdl_parser.commands.items():
            parameter_description, response_description = \
                self._generate_parameters_responses_description(command)

            code_declarations += '\n' + self.generate_from_template({
                    'command_id': command_id,
                    'command_description': command.description,
                    'parameters_description': parameter_description,
                    'responses_description': response_description
                },
                input_template='command_declaration',
                template_ext=self.CPP_TEMPLATE_EXTENSION
            ) + '\n'

        code_declarations = code_declarations[1:-1]

        return code_declarations

    def _generate_command_managers_declaration(self) -> str:
        """
        Generates the declaration of the command manager member variables
        """
        code_declarations = ""
        for identifier in self.fdl_parser.commands.keys():
            code_declarations += self.generate_from_template({
                    'command_id': identifier
                },
                input_template='command_manager_declaration',
                template_ext=self.CPP_TEMPLATE_EXTENSION
            ) + '\n'

        code_declarations = code_declarations[:-1]

        return code_declarations

    def _generate_properties_declaration(self) -> str:
        """
        Generates the declaration of the property wrapper member variables
        """
        code_declarations = ""
        for identifier, prop in self.fdl_parser.properties.items():
            code_declarations += ('' if prop.observable else 'const ') + \
                self.generate_from_template({
                        'property_id': identifier
                    },
                    input_template='property_wrapper_declaration',
                    template_ext=self.CPP_TEMPLATE_EXTENSION
                ) + '\n'

        code_declarations = code_declarations[:-1]

        return code_declarations

    def _generate_using_namespaces(self) -> str:
        """
        Generate the code for using the feature namespaces

        :return: The code containing a `using namespace` for each feature
        """
        code_ns_aliases = self.generate_from_template(
                input_template="using_feature_namespaces",
                template_ext=self.CPP_TEMPLATE_EXTENSION
            )

        return code_ns_aliases

    def _generate_command_managers_init(self) -> str:
        """
        Generates the command manager constructor calls
        """
        code_init = ""
        for identifier in self.fdl_parser.commands.keys():
            code_init += self.generate_from_template({
                    'command_id': identifier
                },
                input_template='command_manager_init',
                template_ext=self.CPP_TEMPLATE_EXTENSION
            ) + ',\n'

        if len(self.fdl_parser.properties.items()) == 0:
            code_init = code_init[:-2]

        return code_init

    def _generate_properties_init(self) -> str:
        """
        Generates the property wrapper constructor calls
        """
        code_init = ""
        for identifier, prop in self.fdl_parser.properties.items():
            code_init += self.generate_from_template({
                    'property_id': identifier,
                    'underlying_type': self._get_underlying_type(prop)
                },
                input_template='property_wrapper_init',
                template_ext=self.CPP_TEMPLATE_EXTENSION
            ) + ',\n'

        code_init = code_init[:-2]

        return code_init

    def _generate_command_managers_properties_init(self) -> str:
        """
        Generates the command manager and property wrapper constructor calls
        """
        return self._generate_command_managers_init() + self._generate_properties_init()

    def _generate_command_executors(self) -> str:
        """
        Generates the code that sets the executor functions for all commands
        """
        code = ""
        for identifier in self.fdl_parser.commands.keys():
            code += self.generate_from_template({
                    'command_id': identifier
                },
                input_template='command_executor',
                template_ext=self.CPP_TEMPLATE_EXTENSION
            ) + '\n'

        code = code[:-1]

        return code

    def _generate_commands_implementation(self) -> str:
        """
        Generates the implementation prototypes for each command executor function
        """
        code_implementation = ""
        for identifier, command in self.fdl_parser.commands.items():
            implementation_logic = "// TODO: Write actual Command implementation logic..."
            if command.observable:
                implementation_logic += """
const auto NUM_STEPS = 10;
for (int i = 0; i <= NUM_STEPS; ++i)
{
    // do stuff...
    Command->setExecutionInfo(SiLA2::CReal{i / NUM_STEPS});
}"""
                if command.intermediates:
                    implementation_logic = implementation_logic[:-1] + \
                        f"    Command->setIntermediateResult({identifier}_IntermediateResponses{{}});\n}}"

            code_implementation += self.generate_from_template({
                    'command_id': identifier,
                    'implementation_logic': indent(implementation_logic, 4)
                },
                input_template='command_implementation',
                template_ext=self.CPP_TEMPLATE_EXTENSION
            ) + '\n'

        code_implementation = code_implementation[:-1]

        return code_implementation

    def write_implementation_code(self, output_filename: Union[str, None] = None):
        """
        This method builds an implementation class from a template.

            :param output_filename: filename for the output files without an extension.
                                    The extensions (i.e .h/.cpp) will be appended automatically.
        """

        if output_filename is None:
            output_filename = '{feature_identifier}Impl'.format(
                feature_identifier=str(self.fdl_parser.identifier)
            )
        output_filename += '.{ext}'

        for file_type in ['header', 'source']:
            # configuration options
            template_filename = "sila_implementation_" + file_type

            # initialise variables
            template_vars = {
                'creation_date': date.today().isoformat()
            }

            self.write_from_template(template_vars,
                                     # header only
                                     feature_description=self.fdl_parser.description,
                                     commands_include=self._generate_commands_include(),
                                     properties_include=self._generate_properties_include(),
                                     commands_aliases=self._generate_commands_alias(),
                                     properties_aliases=self._generate_properties_alias(),
                                     commands_declaration=self._generate_commands_declaration(),
                                     command_managers_declaration=self._generate_command_managers_declaration(),
                                     properties_declaration=self._generate_properties_declaration(),
                                     # source only
                                     using_feature_namespaces=self._generate_using_namespaces(),
                                     command_managers_properties_init=self._generate_command_managers_properties_init(),
                                     commands_set_executor=self._generate_command_executors(),
                                     commands_implementation=self._generate_commands_implementation(),
                                     # both
                                     output_filename=output_filename.format(ext='h' if file_type == 'header' else 'cpp'),
                                     input_template=template_filename,
                                     template_ext=self.CPP_TEMPLATE_EXTENSION
            )
