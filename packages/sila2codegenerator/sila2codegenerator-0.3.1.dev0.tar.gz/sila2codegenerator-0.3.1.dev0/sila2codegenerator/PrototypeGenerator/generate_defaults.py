"""
________________________________________________________________________

:PROJECT: SiLA2_python

*SiLA2 Code Generator for using Packages*

:details: Methods that generate dictionaries for default values

:file:    generate_defaults.py
:authors: Timm Severin (timm.severin@tum.de)

:date: (creation)          2019-06-21
:date: (last modification) 2019-09-16

.. note:: Consider replacing with the features of sila2lib.proto_builder.dynamic_feature

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

from typing import Union
from typing import List

from sila2lib.fdl_parser.fdl_parser import FDLParser
from sila2lib.fdl_parser.type_base import DataType
from sila2lib.fdl_parser.type_basic import BasicType
from sila2lib.fdl_parser.type_list import ListType
from sila2lib.fdl_parser.type_constrained import ConstrainedType
from sila2lib.fdl_parser.type_structured import StructureType
from sila2lib.fdl_parser.type_data_type_identifier import DataTypeIdentifier


def generate_default_dicts(fdl_parser: FDLParser) -> str:

    return "\n\n".join([
        _generate_default_dicts_data_type_definitions(fdl_parser=fdl_parser),
        _generate_default_dicts_commands(fdl_parser=fdl_parser),
        _generate_default_dicts_properties(fdl_parser=fdl_parser)
    ])


def _generate_default_dicts_data_type_definitions(fdl_parser: FDLParser) -> str:

    # initialise storage variable
    default_dicts = []
    for identifier, data_type_definition in fdl_parser.data_type_definitions.items():
        default_dicts.append(
            _generate_dictionary_str(primary_identifier=identifier,
                                     identifiers=[identifier],
                                     data_type_strings=[
                                         _evaluate_data_type(
                                             data_type=data_type_definition.sub_type,
                                             identifier=identifier,
                                             namespace='pb2.DataType_' + identifier
                                         )
                                     ],
                                     prefix='DataType_',
                                     postfix='')
        )

    return "\n\n".join(default_dicts)


def _generate_default_dicts_commands(fdl_parser: FDLParser) -> str:

    # initialise storage variable
    default_dicts = []
    for identifier, command in fdl_parser.commands.items():
        # evaluate all sub elements
        #   Parameter
        parameter_ids = [param_id for param_id in command.parameters]
        parameter_data_type_strings = [
            _evaluate_data_type(
                data_type=command.parameters[param_id].sub_type,
                identifier=identifier,
                namespace='pb2.' + identifier + '_Parameters')
            for param_id
            in command.parameters
        ]
        default_dicts.append(
            _generate_dictionary_str(primary_identifier=identifier,
                                     identifiers=parameter_ids,
                                     data_type_strings=parameter_data_type_strings,
                                     prefix='',
                                     postfix='_Parameters')
        )
        #   Responses
        response_ids = [response_id for response_id in command.responses]
        response_data_type_strings = [
            _evaluate_data_type(
                data_type=command.responses[response_id].sub_type,
                identifier=identifier,
                namespace='pb2.' + identifier + '_Responses')
            for response_id
            in command.responses
        ]
        default_dicts.append(
            _generate_dictionary_str(primary_identifier=identifier,
                                     identifiers=response_ids,
                                     data_type_strings=response_data_type_strings,
                                     prefix='',
                                     postfix='_Responses')
        )
        if command.intermediates:
            #   IntermediateResponses (only if any defined)
            response_ids = [response_id for response_id in command.intermediates]
            response_data_type_strings = [
                _evaluate_data_type(
                    data_type=command.intermediates[response_id].sub_type,
                    identifier=identifier,
                    namespace='pb2.' + identifier + '_IntermediateResponses')
                for response_id
                in command.intermediates
            ]
            default_dicts.append(
                _generate_dictionary_str(primary_identifier=identifier,
                                         identifiers=response_ids,
                                         data_type_strings=response_data_type_strings,
                                         prefix='',
                                         postfix='_IntermediateResponses')
            )

    return "\n\n".join(default_dicts)


def _generate_default_dicts_properties(fdl_parser: FDLParser) -> str:

    # initialise storage variable
    default_dicts = []
    for identifier, property_obj in fdl_parser.properties.items():

        if property_obj.observable:
            prefix = 'Subscribe_'
        else:
            prefix = 'Get_'
        default_dicts.append(
            _generate_dictionary_str(primary_identifier=identifier,
                                     identifiers=[property_obj.response.identifier],
                                     data_type_strings=[_evaluate_data_type(
                                         data_type=property_obj.response.sub_type,
                                         identifier=identifier,
                                         namespace='pb2.' + prefix + identifier + '_Responses'
                                     )],
                                     prefix=prefix,
                                     postfix='_Responses')
        )

    return "\n\n".join(default_dicts)


def _generate_dictionary_str(primary_identifier: str,
                             identifiers: List[str],
                             data_type_strings: List[str],
                             prefix: str = '',
                             postfix: str = '') -> str:

    dictionary_entries = []
    for (identifier, data_type_str) in zip(identifiers, data_type_strings):
        if data_type_str is not None:
            dictionary_entries.append(
                "'{identifier}': {data_type_str}".format(identifier=identifier, data_type_str=data_type_str)
            )

    return "default_dict['{prefix}{identifier}{postfix}'] = {{\n    {dictionary_entries}\n}}".format(
        identifier=primary_identifier,
        dictionary_entries=',\n    '.join(dictionary_entries),
        prefix=prefix,
        postfix=postfix
    )


def _evaluate_data_type(data_type: DataType, identifier: str, namespace: str) -> str:

    if data_type.is_basic:
        return _evaluate_basic_type_str(data_type=data_type)
    elif data_type.is_list:
        return _evaluate_list_type_str(data_type=data_type, identifier=identifier, namespace=namespace)
    elif data_type.is_constrained:
        return _evaluate_constrained_type_str(data_type=data_type, identifier=identifier, namespace=namespace)
    elif data_type.is_identifier:
        return _evaluate_data_type_identifier_str(data_type=data_type)
    elif data_type.is_structure:
        return _evaluate_structure_type_str(data_type=data_type, identifier=identifier, namespace=namespace)
    else:
        raise TypeError


def _evaluate_basic_type_str(data_type: Union[BasicType, DataType]) -> Union[str, None]:

    if data_type.sub_type == 'Void':
        # handle the special case of an empty parameter
        return None

    return '{sila_namespace}.{basic_type}(value={default_value})'.format(
        sila_namespace='silaFW_pb2',
        basic_type=data_type.sub_type,
        default_value=data_type.default_value
    )


def _evaluate_list_type_str(data_type: Union[ListType, DataType], identifier: str, namespace: str) -> str:

    return '[' + _evaluate_data_type(data_type=data_type.sub_type, identifier=identifier, namespace=namespace) + ']'


def _evaluate_constrained_type_str(data_type: Union[ConstrainedType, DataType], identifier: str, namespace: str) -> str:

    return _evaluate_data_type(data_type=data_type.sub_type, identifier=identifier, namespace=namespace)


def _evaluate_data_type_identifier_str(data_type: Union[DataTypeIdentifier, DataType]) -> str:

    return "pb2.DataType_{sub_identifier}(**default_dict['DataType_{sub_identifier}'])".format(sub_identifier=data_type.sub_type)


def _evaluate_structure_type_str(data_type: Union[StructureType, DataType], identifier: str, namespace: str) -> str:

    sub_namespace = '{namespace}.{identifier}_Struct'.format(
        namespace=namespace,
        identifier=identifier
    )
    # we need to evaluate all sub elements
    sub_elements = []
    for structure_element in data_type.sub_type:
        sub_elements.append(
            structure_element.identifier + '=' +
            _evaluate_data_type(data_type=structure_element.sub_type,
                                identifier=structure_element.identifier,
                                namespace=sub_namespace)
        )

    return '{namespace}.{identifier}_Struct({sub_elements})'.format(
        namespace=namespace,
        identifier=identifier,
        sub_elements=', '.join(sub_elements)
    )
