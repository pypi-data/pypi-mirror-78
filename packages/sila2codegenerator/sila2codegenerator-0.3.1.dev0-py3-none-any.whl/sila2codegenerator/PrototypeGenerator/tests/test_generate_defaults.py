
# import general packages
import unittest
import os

# import packages from this package
from .. import generate_defaults

# import library packages
from sila2lib.fdl_parser.fdl_parser import FDLParser


class TestGenerateDefaultDicts(unittest.TestCase):
    """
    Tests to validate whether the :mod:`generate_defaults` helper functions for dictionaries work properly.
    """

    def setUp(self):
        """
        Prepares all tests
            Stores the path from where to load FDL files.
        """

        # we re-use the FDL files used for the ProtoBuilder unittests, so we need the correct path
        self.fdl_path = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'fdl')

        # show complete diffs
        self.maxDiff = None

    def _fdlParser_from_file(self, filename: str) -> FDLParser:
        """
        Generate a FDLParser object which we can use for testing.

        :param filename: FDL-file to load into the :class:`~sila2lib.FDLParser.FALParser.FDLParser`.
        """

        return FDLParser(fdl_filename=os.path.join(self.fdl_path, filename))

    def test_data_type_definition_basic(self):

        fdl_parser = self._fdlParser_from_file('DataTypeDefinition_Basic.sila.xml')

        dictionaries = generate_defaults._generate_default_dicts_data_type_definitions(fdl_parser=fdl_parser)

        self.assertEqual(
            dictionaries,
            (
                "default_dict['DataType_BasicDefinition'] = {" "\n"
                "    " "'BasicDefinition': silaFW_pb2.Boolean(value=False)" "\n"
                "}"
            )
        )

    def test_data_type_definition_constrained(self):

        fdl_parser = self._fdlParser_from_file('DataTypeDefinition_Constrained.sila.xml')

        dictionaries = generate_defaults._generate_default_dicts_data_type_definitions(fdl_parser=fdl_parser)

        self.assertEqual(
            dictionaries,
            (
                "default_dict['DataType_ConstrainedDefinition'] = {" "\n"
                "    " "'ConstrainedDefinition': silaFW_pb2.Boolean(value=False)" "\n"
                "}"
            )
        )

    def test_data_type_definition_data_type_identifier(self):
        fdl_parser = self._fdlParser_from_file('DataTypeDefinition_DataTypeIdentifier.sila.xml')

        dictionaries = generate_defaults._generate_default_dicts_data_type_definitions(fdl_parser=fdl_parser)

        self.assertEqual(
            dictionaries,
            (
                "default_dict['DataType_IdentifierDefinition'] = {" "\n"
                "    " "'IdentifierDefinition': pb2.DataType_TestDataType(**default_dict['DataType_TestDataType'])" "\n"
                "}"
            )
        )

    def test_data_type_definition_list(self):
        fdl_parser = self._fdlParser_from_file('DataTypeDefinition_List.sila.xml')

        dictionaries = generate_defaults._generate_default_dicts_data_type_definitions(fdl_parser=fdl_parser)

        self.assertEqual(
            dictionaries,
            (
                "default_dict['DataType_ListDefinition'] = {" "\n"
                "    " "'ListDefinition': [silaFW_pb2.Boolean(value=False)]" "\n"
                "}"
            )
        )

    def test_data_type_definition_struct(self):
        fdl_parser = self._fdlParser_from_file('DataTypeDefinition_Structure.sila.xml')

        dictionaries = generate_defaults._generate_default_dicts_data_type_definitions(fdl_parser=fdl_parser)

        self.assertEqual(
            dictionaries,
            (
                "default_dict['DataType_StructureDefinition'] = {" "\n"
                "    " "'StructureDefinition': "
                       "pb2.DataType_StructureDefinition.StructureDefinition_Struct"
                       "("
                       "BasicElement=" "silaFW_pb2.Boolean(value=False)"
                       ")" "\n"
                "}"
            )
        )

    def test_data_type_definition_struct_multi(self):
        fdl_parser = self._fdlParser_from_file('DataTypeDefinition_StructureMulti.sila.xml')

        dictionaries = generate_defaults._generate_default_dicts_data_type_definitions(fdl_parser=fdl_parser)

        self.assertEqual(
            dictionaries,
            (
                "default_dict['DataType_StructureDefinition'] = {" "\n"
                "    " "'StructureDefinition': "
                       "pb2.DataType_StructureDefinition.StructureDefinition_Struct"
                       "("
                       "BasicBooleanElement=" "silaFW_pb2.Boolean(value=False), "
                       "BasicStringElement=" "silaFW_pb2.String(value='default string')"
                       ")" "\n"
                "}"
            )
        )

    def test_data_type_definition_struct_of_list(self):
        fdl_parser = self._fdlParser_from_file('DataTypeDefinition_StructureOfList.sila.xml')

        dictionaries = generate_defaults._generate_default_dicts_data_type_definitions(fdl_parser=fdl_parser)

        self.assertEqual(
            dictionaries,
            (
                "default_dict['DataType_StructureDefinition'] = {" "\n"
                "    " "'StructureDefinition': "
                       "pb2.DataType_StructureDefinition.StructureDefinition_Struct"
                       "("
                       "BasicElement=" "[silaFW_pb2.Boolean(value=False)]"
                       ")" "\n"
                "}"
            )
        )

    def test_data_type_definition_struct_of_struct(self):
        fdl_parser = self._fdlParser_from_file('DataTypeDefinition_StructureOfStructure.sila.xml')

        dictionaries = generate_defaults._generate_default_dicts_data_type_definitions(fdl_parser=fdl_parser)

        self.assertEqual(
            dictionaries,
            (
                "default_dict['DataType_StructureDefinition'] = {" "\n"
                "    " "'StructureDefinition': "
                       "pb2.DataType_StructureDefinition.StructureDefinition_Struct"
                       "("
                       "BasicElement="
                            "pb2.DataType_StructureDefinition.StructureDefinition_Struct.BasicElement_Struct"
                            "("
                                "SubStructureElement=" "silaFW_pb2.Boolean(value=False)"
                            ")"
                       ")" "\n"
                "}"
            )
        )

    def test_command_simple(self):

        fdl_parser = self._fdlParser_from_file('Command_Simple.sila.xml')

        dictionaries = generate_defaults._generate_default_dicts_commands(fdl_parser=fdl_parser)

        self.assertEqual(
            dictionaries,
            (
                "default_dict['CommandIdentifier_Parameters'] = {" "\n"
                "    " "'ParameterIdentifier': silaFW_pb2.Boolean(value=False)" "\n"
                "}" "\n"
                "\n"
                "default_dict['CommandIdentifier_Responses'] = {" "\n"
                "    " "'ResponseIdentifier': silaFW_pb2.Boolean(value=False)" "\n"
                "}"
            )
        )

    def test_command_simple_multi(self):

        fdl_parser = self._fdlParser_from_file('Command_SimpleMulti.sila.xml')

        dictionaries = generate_defaults._generate_default_dicts_commands(fdl_parser=fdl_parser)

        self.assertEqual(
            dictionaries,
            (
                "default_dict['CommandIdentifier_Parameters'] = {" "\n"
                "    " "'ParameterIdentifier1': silaFW_pb2.Boolean(value=False)," "\n"
                "    " "'ParameterIdentifier2': silaFW_pb2.Boolean(value=False)" "\n"
                "}" "\n"
                "\n"
                "default_dict['CommandIdentifier_Responses'] = {" "\n"
                "    " "'ResponseIdentifier1': silaFW_pb2.Boolean(value=False)," "\n"
                "    " "'ResponseIdentifier2': silaFW_pb2.Boolean(value=False)" "\n"
                "}"
            )
        )

    def test_command_observable_no_intermediate(self):

        fdl_parser = self._fdlParser_from_file('Command_Observable_NoIntermediate.sila.xml')

        dictionaries = generate_defaults._generate_default_dicts_commands(fdl_parser=fdl_parser)

        self.assertEqual(
            dictionaries,
            (
                "default_dict['CommandIdentifier_Parameters'] = {" "\n"
                "    " "'ParameterIdentifier': silaFW_pb2.Boolean(value=False)" "\n"
                "}" "\n"
                "\n"
                "default_dict['CommandIdentifier_Responses'] = {" "\n"
                "    " "'ResponseIdentifier': silaFW_pb2.Boolean(value=False)" "\n"
                "}"
            )
        )

    def test_command_observable_intermediate(self):

        fdl_parser = self._fdlParser_from_file('Command_Observable_Intermediate.sila.xml')

        dictionaries = generate_defaults._generate_default_dicts_commands(fdl_parser=fdl_parser)

        self.assertEqual(
            dictionaries,
            (
                "default_dict['CommandIdentifier_Parameters'] = {" "\n"
                "    " "'ParameterIdentifier': silaFW_pb2.Boolean(value=False)" "\n"
                "}" "\n"
                "\n"
                "default_dict['CommandIdentifier_Responses'] = {" "\n"
                "    " "'ResponseIdentifier': silaFW_pb2.Boolean(value=False)" "\n"
                "}" "\n"
                "\n"
                "default_dict['CommandIdentifier_IntermediateResponses'] = {" "\n"
                "    " "'IntermediateResponseIdentifier': silaFW_pb2.Boolean(value=False)" "\n"
                "}"
            )
        )

    def test_property_simple(self):

        fdl_parser = self._fdlParser_from_file('Property_Simple.sila.xml')

        dictionaries = generate_defaults._generate_default_dicts_properties(fdl_parser=fdl_parser)

        self.assertEqual(
            dictionaries,
            (
                "default_dict['Get_PropertyIdentifier_Responses'] = {" "\n"
                "    " "'PropertyIdentifier': silaFW_pb2.Boolean(value=False)" "\n"
                "}"
            )
        )

    def test_property_observable(self):

        fdl_parser = self._fdlParser_from_file('Property_Observable.sila.xml')

        dictionaries = generate_defaults._generate_default_dicts_properties(fdl_parser=fdl_parser)

        self.assertEqual(
            dictionaries,
            (
                "default_dict['Subscribe_PropertyIdentifier_Responses'] = {" "\n"
                "    " "'PropertyIdentifier': silaFW_pb2.Boolean(value=False)" "\n"
                "}"
            )
        )
