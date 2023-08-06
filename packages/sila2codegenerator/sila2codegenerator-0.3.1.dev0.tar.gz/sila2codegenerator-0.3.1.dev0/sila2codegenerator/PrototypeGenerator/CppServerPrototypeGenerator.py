"""
________________________________________________________________________

:PROJECT: SiLA2_python

*SiLA2 Code Generator for using Packages*

:details: Class to generate C++ server prototypes of a SiLA2 Client/Server

:file:    ServerPrototypeGenerator.py
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
from datetime import date

# import modules from this package
from ..service_descriptor_parser import ServiceDescriptorParser
from .PrototypeGenerator import PrototypeGenerator

# meta information packages
from typing import Union

# import helper
from .cpp_namespace_helper import generate_namespaces

class CppServerPrototypeGenerator(PrototypeGenerator):
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

            For parameter descriptions compare initialiser :meth:`.PrototypeGenerator.__init__`
        """

        super().__init__(
            service_description=service_description,
            output_dir=output_dir,
            template_dir=template_dir,
            fdl_path=fdl_path,
            ignore_overwrite_warning=ignore_overwrite_warning
        )

    def _generate_feature_registration(self) -> str:
        """
        Generate the code to register all features with the server

        :return: The code for all feature registration
        """

        # Initialise variables
        code_feature_registration = ""

        for feature_id in self.service_dict['SiLA_feature_list']:
            code_feature_registration += self.generate_from_template({
                    'feature_identifier': feature_id
                },
                input_template='feature_registration',
                template_ext=self.CPP_TEMPLATE_EXTENSION
            ) + "\n"

        code_feature_registration = code_feature_registration[:-1]

        return code_feature_registration

    def _generate_grpc_includes(self) -> str:
        """
        Generate the code to include the header files for each feature

        :return: The include code
        """

        code_include = "// include SiLA features"

        for feature_id in self.service_dict['SiLA_feature_list']:
            code_include += "\n" + self.generate_from_template({
                    'feature_identifier': feature_id
                },
                input_template='include_features',
                template_ext=self.CPP_TEMPLATE_EXTENSION
            )

        return code_include

    def _generate_using_namespaces(self) -> str:
        """
        Generate the code for using the feature namespaces

        :return: The code containing a `using namespace` for each feature
        """

        code_ns_aliases = ""
        for feature_id in self.service_dict['SiLA_feature_list']:
            namespace = '::'.join(generate_namespaces(self.fdl_parsers[feature_id]))
            code_ns_aliases += self.generate_from_template({
                'feature_identifier': feature_id,
                'feature_namespace': namespace
            },
            input_template="using_feature_namespaces",
            template_ext=self.CPP_TEMPLATE_EXTENSION)
            code_ns_aliases += '\n'

        return code_ns_aliases

    def write_server_code(self, output_filename: Union[str, None] = None, meta_path: str = "."):
        """
        This method builds a server class from a template.
            The resulting file can be run as SiLA server for the implemented features.

        :param output_filename: filename for server output file
        :param meta_path: Path to where the meta files are stored (FDL, proto, pickle)
        """

        # configuration options
        template_filename = "sila_server"
        if output_filename is None:
            output_filename = '{service_name}Server.cpp'.format(
                service_name=str(self.service_dict['service_name'])
            )

        # add the meta path to the general dictionary
        self.substitution_dict['meta_path'] = meta_path

        # initialise variables
        template_vars = {
            'creation_date': date.today().isoformat(),
            # gRPC C++ needs IPv6 localhost syntax for IP to successfully make the server available on the network
            'IP_address': '[::]' if self.service_dict['IP_address'] in ('localhost', '127.0.0.1') \
                 else self.service_dict['IP_address']
        }

        self.write_from_template(template_vars,
                                 feature_registration=self._generate_feature_registration(),
                                 include_features=self._generate_grpc_includes(),
                                 using_feature_namespaces=self._generate_using_namespaces(),
                                 output_filename=output_filename,
                                 input_template=template_filename,
                                 template_ext=self.CPP_TEMPLATE_EXTENSION
        )
