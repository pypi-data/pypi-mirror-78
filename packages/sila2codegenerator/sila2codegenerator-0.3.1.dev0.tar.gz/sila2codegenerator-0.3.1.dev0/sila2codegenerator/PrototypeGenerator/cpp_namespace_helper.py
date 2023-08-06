"""
________________________________________________________________________

:PROJECT: SiLA2_python

*SiLA2 Code Generator for using Packages*

:details: Methods that help generating C++ namespaces from the SiLA feature namespaces

:file:    cpp_namespace_helper.py
:authors: Florian Meinicke (florian.meinicke@cetoni.de)

:date: (creation)          2020-08-12
:date: (last modification) 2020-08-12

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

# import packages from the SiLA2 library
from sila2lib.fdl_parser.fdl_parser import FDLParser


def generate_namespaces(fdl_parser: FDLParser) -> list:
    """
    Generates a list where each element is a namespace part of the given feature

    :param fdl_parser: The FDLParser for the feature for which the namespace should be generated
    :return: A list where each element is a part of the feature's namespace
    """
    # because the calls to `split` create nested lists
    # we need some list comprehension magic here to flatten the list again
    # result is like: namespaces = ["sila2", "originator", "category", "feature_id", "version"]
    namespaces = [
        namespace for sub_list in [
            ["sila2"],
            fdl_parser.originator.split("."),
            fdl_parser.category.split(".") if fdl_parser.category is not None else ['none'],
            [fdl_parser.identifier.lower()],
            ['v' + str(fdl_parser.feature_version_major)]
        ]
        for namespace in sub_list
    ]

    return namespaces
