"""
________________________________________________________________________

:PROJECT: SiLA2_python

*SiLA2 Code Generator for using Packages*

:details: Class to generate Python implementation prototypes of a SiLA2 Client/Server

:file:    PyImplementationPrototypeGenerator.py
:authors: Timm Severin (timm.severin@tum.de)

:date: (creation)          2019-06-21
:date: (last modification) 2020-08-12

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

# import modules from this package
from ..service_descriptor_parser import ServiceDescriptorParser
from .FDLPrototypeGenerator import FDLPrototypeGenerator

# import packages from the SiLA2 library
from sila2lib.fdl_parser.fdl_parser import FDLParser
from sila2lib.fdl_parser.data_type_intermediate import IntermediateDataType
from sila2lib.fdl_parser.data_type_response import ResponseDataType
from sila2lib.fdl_parser.type_basic import BasicType
from sila2lib.fdl_parser.type_base import DataType

# meta information packages
from typing import Union
from typing import Dict


class PyImplementationPrototypeGenerator(FDLPrototypeGenerator):
    """TODO: Document"""

    simulation: bool

    def __init__(self,
                 fdl_input: Union[str, FDLParser],
                 service_description: Union[ServiceDescriptorParser, None] = None,
                 output_dir: Union[str, None] = None,
                 template_dir: Union[str, None] = None,
                 simulation: bool = True,
                 ignore_overwrite_warning: bool = False):
        """
        Class initialiser

        :param fdl_input: Either a reference to an FDLParser object (sila2lib.fdl_parser) or a string to an FDL
                          file. This is used to extract further information on methods and properties of the server
        :param simulation: Generate the simulation implementation or the real one

        .. note:: For further parameter descriptions compare initialiser :meth:`.PrototypeGenerator.__init__`
        """
        super().__init__(
            fdl_input=fdl_input,
            service_description=service_description,
            output_dir=output_dir,
            template_dir=template_dir,
            ignore_overwrite_warning=ignore_overwrite_warning
        )

        # add the mode to the replacement dictionary
        self.simulation = simulation
        self.substitution_dict['implementation_mode'] = 'Simulation' if self.simulation else 'Real'

    def _generate_default_value(self, element: Union[DataType, BasicType], namespace: str) -> str:
        # TODO: Implement

        response_string = ''

        # the value is constructed more complex from the sub_type
        if element.is_basic:
            response_string += 'fwpb2.' + element.sub_type + '(value=' + str(element.default_value) + ')'
        else:
            # complex type, figure out the rest
            if element.is_list:
                response_string += '[' + self._generate_default_value(element.sub_type, namespace=namespace) + ']'
            elif element.is_structure:
                response_string += 'a'
            elif element.is_constrained:
                # do not handle this here
                response_string += self._generate_default_value(element.sub_type, namespace=namespace)
            elif element.is_identifier:
                response_string += 'pb2.DataType_' + element.sub_type + '(' + \
                                   self._generate_default_value(
                                       self.fdl_parser.data_type_definitions[element.sub_type].sub_type,
                                       namespace='pb2'
                                   ) + ')'
            else:
                raise TypeError

        return response_string

    def _generate_implementation_commands(self) -> str:
        """
        Generates the command implementations for the real/simulation implementation

        :return: The code for all command implementations
        """

        # Initialise variables
        code_command_implementations = ""

        for identifier, command in self.fdl_parser.commands.items():
            # distinguish between the different command variants
            if command.observable and command.intermediates:
                # observable and defined intermediates
                template_file = 'command_observable_intermediate_implementation'
            elif command.observable and not command.intermediates:
                # observable without any intermediates defined
                template_file = 'command_observable_no-intermediate_implementation'
            else:
                # unobservable
                template_file = 'command_unobservable_implementation'

            namespace_intermediate = identifier + '_IntermediateResponses'
            namespace_responses = identifier + '_Responses'

            default_intermediates = [
                identifier + '=' + self._generate_default_value(
                    element=intermediate.sub_type,
                    namespace=namespace_intermediate)
                for identifier, intermediate
                in command.intermediates.items()
            ]
            default_responses = [
                identifier + '=' + self._generate_default_value(
                    element=response.sub_type,
                    namespace=namespace_responses)
                for identifier, response
                in command.responses.items()
            ]

            code_command_implementations += "\n" + \
                self.generate_from_template({
                        'command_id': identifier,
                        'command_name': command.name,
                        'command_description': command.description,
                        'parameter_description': self._generate_parameter_description(command),
                        'response_description': self._generate_response_description(element=command),
                        'intermediate_description': self._generate_intermediate_response_description(command=command),
                        'default_value_intermediate': ', '.join(default_intermediates),
                        'default_value_result': ', '.join(default_responses)
                    },
                    input_template=template_file
                ) + "\n"

        code_command_implementations = code_command_implementations[1:-1]

        return code_command_implementations

    def _generate_implementation_properties(self) -> str:
        """
        Generates the property implementations for the real/simulation implementation

            :return: The code for all property implementations
        """

        # Initialise variables
        code_property_implementations = ""

        for identifier, property_object in self.fdl_parser.properties.items():
            # distinguish between the different command variants
            if property_object.observable:
                # observable and defined intermediates
                namespace_response = 'Subscribe_' + identifier + '_Responses'
                template_file = 'property_observable_implementation'
            else:
                # unobservable
                namespace_response = 'Get_' + identifier + '_Responses'
                template_file = 'property_unobservable_implementation'

            default_response = property_object.response.identifier + '=' + \
                self._generate_default_value(element=property_object.response.sub_type, namespace=namespace_response)

            code_property_implementations += "\n" + \
                self.generate_from_template({
                        'property_id': property_object.identifier,
                        'property_name': property_object.name,
                        'property_description': property_object.description,
                        'response_description': self._generate_response_description(element=property_object),
                        'default_value_response': default_response
                    },
                    input_template=template_file
                ) + "\n"

        code_property_implementations = code_property_implementations[1:-1]

        return code_property_implementations

    def write_implementation_code(self, output_filename: Union[str, None] = None):
        """
        This method builds an implementation class from a template.
            The resulting file can be the simulation or real implementation.

            :param output_filename: filename for server output file
        """

        # configuration options
        template_filename = "sila_implementation"
        if output_filename is None:
            output_filename = '{feature_identifier}_{implementation_mode}.py'.format(
                feature_identifier=str(self.fdl_parser.identifier),
                implementation_mode=('simulation' if self.simulation else 'real')
            )

        # initialise variables
        template_vars = {
        }

        self.write_from_template(template_vars,
                                 commands_implementation=self._generate_implementation_commands(),
                                 properties_implementation=self._generate_implementation_properties(),
                                 output_filename=output_filename,
                                 input_template=template_filename)
