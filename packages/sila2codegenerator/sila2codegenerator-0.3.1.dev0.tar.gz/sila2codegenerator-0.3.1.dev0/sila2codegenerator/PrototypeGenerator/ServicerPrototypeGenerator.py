"""
________________________________________________________________________

:PROJECT: SiLA2_python

*SiLA2 Code Generator for using Packages*

:details: Class to generate servicer prototypes of a SiLA2 Client/Server

:file:    ServicerPrototypeGenerator.py
:authors: Timm Severin (timm.severin@tum.de)
          mark doerr  (mark.doerr@uni-greifswald.de)

:date: (creation)          2019-06-21
:date: (last modification) 2019-11-04

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

# meta information packages
from typing import Union


class ServicerPrototypeGenerator(FDLPrototypeGenerator):
    """TODO: Document"""

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

        For further parameter descriptions compare initialiser :meth:`.PrototypeGenerator.__init__`
        """
        super().__init__(
            fdl_input=fdl_input,
            service_description=service_description,
            output_dir=output_dir,
            template_dir=template_dir,
            ignore_overwrite_warning=ignore_overwrite_warning
        )

    def _generate_servicer_command(self) -> str:
        """
        Generates the command implementations for the servicer

        :return: The code for all servicer command implementations
        """

        # Initialise variables
        code_command_calls = ""

        for command_id, command in self.fdl_parser.commands.items():
            # distinguish between the different command variants
            if command.observable and command.intermediates:
                # observable and defined intermediates
                template_file = 'command_observable_intermediate_servicer'
            elif command.observable and not command.intermediates:
                # observable without any intermediates defined
                template_file = 'command_observable_no-intermediate_servicer'
            else:
                # unobservable
                template_file = 'command_unobservable_servicer'

            code_command_calls += "\n" + \
                self.generate_from_template({
                        'command_id': command_id,
                        'command_name': command.name,
                        'command_description': command.description,
                        'parameter_description': self._generate_parameter_description(command=command),
                        'response_description': self._generate_response_description(element=command),
                        'intermediate_description': self._generate_intermediate_response_description(command=command)
                    },
                    input_template=template_file
                ) + "\n"

        code_command_calls = code_command_calls[1:-1]

        return code_command_calls

    def _generate_servicer_properties(self) -> str:
        """
        Generates the property implementations for the servicer

        :return: The code for all servicer property implementations
        """

        # Initialise variables
        code_property_calls = ""

        for identifier, property_object in self.fdl_parser.properties.items():

            if property_object.observable:
                template_file = 'property_observable_servicer'
            else:
                template_file = 'property_unobservable_servicer'

            code_property_calls += "\n" + \
                self.generate_from_template({
                    'property_id': identifier,
                    'property_name': property_object.name,
                    'property_description': property_object.description,
                    'response_description': self._generate_response_description(element=property_object)
                    },
                    input_template=template_file
                ) + "\n"

        code_property_calls = code_property_calls[1:-1]

        return code_property_calls

    def write_servicer_code(self, output_filename: Union[str, None] = None):
        """
        This method builds a servicer class from a template.
            The resulting file serves as bridge between the server and the real implementation.

        :param output_filename: filename for server output file.
        """

        # configuration options
        template_filename = "sila_servicer"
        if output_filename is None:
            output_filename = str(self.fdl_parser.identifier) + "_servicer.py"

        # initialise variables
        template_vars = {
        }

        self.write_from_template(template_vars,
                                 commands_servicer=self._generate_servicer_command(),
                                 properties_servicer=self._generate_servicer_properties(),
                                 output_filename=output_filename,
                                 input_template=template_filename)
