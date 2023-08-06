"""
________________________________________________________________________

:PROJECT: SiLA2_python

*SiLA2 Code Generator for using Packages*

:details: Base class to generate prototypes of features of a SiLA2 Client/Server

:file:    FDLPrototypeGenerator.py
:authors: Timm Severin (timm.severin@tum.de)

:date: (creation)          2019-06-21
:date: (last modification) 2019-09-16

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

# import modules from this package
from ..service_descriptor_parser import ServiceDescriptorParser
from .PrototypeGenerator import PrototypeGenerator

# import packages from the SiLA2 library
from sila2lib.fdl_parser.fdl_parser import FDLParser
from sila2lib.fdl_parser.command import Command
from sila2lib.fdl_parser.property import Property

# meta information packages
from typing import Union


class FDLPrototypeGenerator(PrototypeGenerator):
    """Base class for prototype generation that requires a FDLParser object"""
    fdl_parser: FDLParser

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
            service_description=service_description,
            output_dir=output_dir,
            template_dir=template_dir,
            ignore_overwrite_warning=ignore_overwrite_warning
        )

        # if necessary create the FDLParser object from the input
        if isinstance(fdl_input, FDLParser):
            self.fdl_parser = fdl_input
        else:
            self.fdl_parser = FDLParser(fdl_filename=fdl_input)

        # extract feature information that is available for the template substitution
        self.substitution_dict['feature_name'] = self.fdl_parser.name
        self.substitution_dict['feature_identifier'] = self.fdl_parser.identifier
        self.substitution_dict['feature_description'] = self.fdl_parser.description

    def _generate_parameter_description(self, command: Command) -> str:
        """
        Generates a description of all parameters of the given command.


        :param command: A :class:`Command` object for which to generate the description(s).

        :return: A string with all parameters described based on the `parameter_description.pyt` template file.

        .. note:: This will *only* generate descriptions for the parameters defined in the FDL/.proto files, i.e. not
                  the python parameters `request` and `context` of the servicer/stubs (defined in gRPC, exact naming
                  might vary). However, the description generated here describes the elements that are supplied via
                  `request`, so this is the most interesting part.
        """

        description = ''
        for identifier, parameter in command.parameters.items():
            description += \
                self.generate_from_template({
                        'parameter_id': identifier,
                        'parameter_name': parameter.name,
                        'parameter_description': parameter.description
                    },
                    input_template='parameter_description'
                ) + "\n"

        return description.strip()

    def _generate_response_description(self, element: Union[Command, Property]):
        """
        Generates a description of all responses of the given command or property.

        :param element: A :class:`~sila2lib.FDLParser.Command.Command` or :class:`~sila2lib.FDLParser.property.Property`
                        object for which to generate the description(s).

        :return: A string with all responses described based on the `parameter_description.pyt` template file.

        .. note:: This will *only* generate descriptions for the responses defined in the FDL/.proto files, i.e. not
                  the python parameters `request` and `context` of the servicer/stubs (defined in gRPC, exact naming
                  might vary). However, the description generated here describes the elements that are supplied via
                  `request`, so this is the most interesting part.
        """

        if type(element) is Property:
            description = self.generate_from_template({
                        'parameter_id': element.response.identifier,
                        'parameter_name': element.response.name,
                        'parameter_description': element.response.description
                    },
                    input_template='parameter_description'
                )
        else:
            description = ''
            for identifier, response in element.responses.items():
                description += \
                    self.generate_from_template({
                        'parameter_id': identifier,
                        'parameter_name': response.name,
                        'parameter_description': response.description
                    },
                        input_template='parameter_description'
                    ) + "\n"

        return description.strip()

    def _generate_intermediate_response_description(self, command: Command):
        """
        Generates a description of all intermediate responses of the given command.

        :param command: A :class:`~sila2lib.FDLParser.Command.Command` object for which to generate the description(s).

        :return: A string with all intermediate responses described based on the `parameter_description.pyt` template
                 file.

        .. note:: This will *only* generate descriptions for the responses defined in the FDL/.proto files, i.e. not
                  the python parameters `request` and `context` of the servicer/stubs (defined in gRPC, exact naming
                  might vary). However, the description generated here describes the elements that are supplied via
                  `request`, so this is the most interesting part.
        """

        description = ''
        for identifier, intermediates in command.intermediates.items():
            description += \
                self.generate_from_template({
                        'parameter_id': identifier,
                        'parameter_name': intermediates.name,
                        'parameter_description': intermediates.description
                    },
                    input_template='parameter_description'
                ) + "\n"

        return description.strip()
