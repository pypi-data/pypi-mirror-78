"""
________________________________________________________________________

:PROJECT: SiLA2_python

*SiLA2 Code Generator for using Packages*

:details: Class to generate C++ project file prototypes of a SiLA2 Client/Server

:file:    CppImplementationPrototypeGenerator.py
:authors: Florian Meinicke (florian.meinicke@cetoni.de)
          Timm Severin (timm.severin@tum.de)

:date: (creation)          2020-08-14
:date: (last modification) 2020-08-14

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

# import the general packages required
import os

# import modules from this package
from ..service_descriptor_parser import ServiceDescriptorParser
from .PrototypeGenerator import PrototypeGenerator

# meta information packages
from typing import Union

# import helper
from .cpp_namespace_helper import generate_namespaces

class CppProjectPrototypeGenerator(PrototypeGenerator):
    """TODO: Document"""

    def __init__(self,
                 service_description: Union[ServiceDescriptorParser, None] = None,
                 output_dir: Union[str, None] = None,
                 template_dir: Union[str, None] = None,
                 fdl_path: str = '.',
                 meta_dir: str = "",
                 ignore_overwrite_warning: bool = False):
        """
        Class initialiser

        :param fdl_path: Path to where **all** FDL input files are stored
        :param meta_dir: Directory where the meta files are stored (FDL, proto)

            For parameter descriptions compare initialiser :meth:`.PrototypeGenerator.__init__`
        """

        super().__init__(
            service_description=service_description,
            output_dir=output_dir,
            template_dir=template_dir,
            fdl_path=fdl_path,
            ignore_overwrite_warning=ignore_overwrite_warning
        )
        self._meta_dir = meta_dir

    def _generate_cmake_protos_declaration(self) -> str:
        """
        Generates the CMake proto files declarations
        """
        code_declarations = ""

        for feature_id in self.service_dict['SiLA_feature_list']:
            code_declarations += f"{'/'.join([self._meta_dir, feature_id])}.proto\n"

        code_declarations = code_declarations[:-1]
        return code_declarations

    def _generate_resource_file_entries(self) -> str:
        """
        Generates the resource file entries for the QRC file
        """
        code_entries = ""

        for feature_id in self.service_dict['SiLA_feature_list']:
            feature_path = feature_id if not self._meta_dir else '/'.join([self._meta_dir, feature_id])
            code_entries += f"<file alias=\"{feature_id}.sila.xml\">{feature_path}.sila.xml</file>\n"

        code_entries = code_entries[:-1]
        return code_entries


    def write_project_code(self):
        """
        This method builds necessary project files (CMake, QRC) from a template.
        """

        # initialise variables
        template_vars = {
        }

        output_filename = "CMakeLists.txt"
        self.write_from_template(template_vars,
            cmake_protos_declaration=self._generate_cmake_protos_declaration(),
            output_filename=output_filename,
            input_template=output_filename.split('.')[0],
            template_ext=output_filename.split('.')[1]
        )

        output_filename = str(self.service_dict['service_name']) + '.qrc'
        self.write_from_template(template_vars,
            resource_file_entries=self._generate_resource_file_entries(),
            output_filename=output_filename,
            input_template='project_resources',
            template_ext=output_filename.split('.')[1]
        )