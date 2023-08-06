"""
________________________________________________________________________

:PROJECT: SiLA2_python

*SiLA2 Code Generator for using Packages*

:details: Class to generate Python server prototypes of a SiLA2 Client/Server

:file:    ServerPrototypeGenerator.py
:authors: Timm Severin (timm.severin@tum.de)
          mark doerr  (mark.doerr@uni-greifswald.de)

:date: (creation)          2019-06-21
:date: (last modification) 2020-08-14

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

# meta information packages
from typing import Union


class PyServerPrototypeGenerator(PrototypeGenerator):
    """TODO: Document"""

    def __init__(self,
                 service_description: Union[ServiceDescriptorParser, None] = None,
                 output_dir: Union[str, None] = None,
                 template_dir: Union[str, None] = None,
                 fdl_path: Union[str, None] = None,
                 ignore_overwrite_warning: bool = False):
        """
        Class initialiser

            For parameter descriptions compare initialiser :meth:`.PrototypeGenerator.__init__`
        """

        super().__init__(
            service_description=service_description,
            output_dir=output_dir,
            template_dir=template_dir,
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
                input_template='feature_registration'
            ) + "\n"

        code_feature_registration = code_feature_registration[:-1]

        return code_feature_registration

    def _generate_grpc_imports(self) -> str:
        """
        Generate the code to import the gRPC modules for each feature

        :return: The import code
        """

        code_import = "# Import gRPC libraries of features"

        for feature_id in self.service_dict['SiLA_feature_list']:
            code_import += "\n" + self.generate_from_template({
                    'feature_identifier': feature_id
                },
                input_template='import_grpc'
            )

        return code_import

    def _generate_servicer_imports(self) -> str:
        """
        Generate the code to import the servicer modules for each feature

        :return: The import code
        """

        code_import = "# Import the servicer modules for each feature"

        for feature_id in self.service_dict['SiLA_feature_list']:
            code_import += "\n" + self.generate_from_template({
                    'feature_identifier': feature_id
                },
                input_template='import_servicer'
            )

        return code_import

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
            output_filename = '{service_name}_server.py'.format(
                service_name=str(self.service_dict['service_name'])
            )

        # add the meta path to the general dictionary
        self.substitution_dict['meta_path'] = meta_path

        # initialise variables
        template_vars = {
        }

        self.write_from_template(template_vars,
                                 feature_registration=self._generate_feature_registration(),
                                 import_grpc_modules=self._generate_grpc_imports(),
                                 import_servicer_modules=self._generate_servicer_imports(),
                                 output_filename=output_filename,
                                 input_template=template_filename)
