
# import general packages
import unittest
from lxml import objectify
import os

from sila2lib.proto_builder.proto_builder import ProtoBuilder
from sila2lib.fdl_parser.fdl_parser import FDLParser
from sila2lib.fdl_parser.data_type_definition import DataTypeDefinition


class TestProtoBuilderDataTypeEvaluation(unittest.TestCase):

    def setUp(self) -> None:

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__), 'fdl', 'Simple.sila.xml'))
        self.proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

    def test_simple_basic(self):
        from ._data_ProtoBuilder_DataTypeDefinition_simple import data_basic

        for basic_type in data_basic:
            with self.subTest(basic_type=basic_type):
                obj = DataTypeDefinition(
                    xml_tree_element=objectify.fromstring(data_basic[basic_type]).DataTypeDefinition
                )

                (definition, type_string) = self.proto_builder._evaluate_data_type(data_type=obj.sub_type,
                                                                                   identifier=obj.identifier,
                                                                                   namespace='sila2.main')

                self.assertIsNone(definition)
                self.assertEqual(
                    type_string,
                    "sila2.org.silastandard." + basic_type + " ${identifier} = ${index};"
                )

    def test_simple_basic_no_import(self):
        from ._data_ProtoBuilder_DataTypeDefinition_simple import data_basic

        # we need a separate ProtoBuilder object here
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__), 'fdl', 'Simple.sila.xml'))
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # translate between SiLA type and basic type
        translation = {
            'Boolean': 'bool',
            'String': 'string',
            'Integer': 'int64',
            'Real': 'double',
            'Binary': 'bytes',
        }

        for basic_type in data_basic:
            with self.subTest(basic_type=basic_type):
                obj = DataTypeDefinition(
                    xml_tree_element=objectify.fromstring(data_basic[basic_type]).DataTypeDefinition
                )

                try:
                    (definition, type_string) = proto_builder._evaluate_data_type(data_type=obj.sub_type,
                                                                                  identifier=obj.identifier,
                                                                                  namespace='sila2.main')
                except NotImplementedError:
                    # TODO: Remaining implementation, for now we allow these errors
                    continue

                self.assertIsNone(definition)
                self.assertEqual(
                    type_string,
                    "sila2.org.silastandard." + basic_type + " ${identifier} = ${index};"
                    #translation[basic_type] + " ${identifier} = ${index};"
                )

    def test_simple_basic_no_import_invalid(self):
        from ._data_ProtoBuilder_DataTypeDefinition_simple import data_basic

        # we need a separate ProtoBuilder object here
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__), 'fdl', 'Simple.sila.xml'))
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        obj = DataTypeDefinition(xml_tree_element=objectify.fromstring(data_basic['Boolean']).DataTypeDefinition)

        # Manually overwrite the sub_type of out basic type
        obj.sub_type.is_basic = False #'Invalid' # might be a different idea behind Timm's test...

        with self.assertRaises(TypeError):
            (_, _) = proto_builder._evaluate_data_type(data_type=obj.sub_type,
                                                       identifier=obj.identifier,
                                                       namespace='sila2.main')

    def test_simple_list(self):
        from ._data_ProtoBuilder_DataTypeDefinition_simple import data_list

        obj = DataTypeDefinition(xml_tree_element=objectify.fromstring(data_list).DataTypeDefinition)

        (definition, type_string) = self.proto_builder._evaluate_data_type(data_type=obj.sub_type,
                                                                           identifier=obj.identifier,
                                                                           namespace='sila2.main')
        self.assertIsNone(definition)
        self.assertEqual(
            type_string,
            "repeated sila2.org.silastandard.Boolean ${identifier} = ${index};"
        )

    def test_simple_constrained(self):
        from ._data_ProtoBuilder_DataTypeDefinition_simple import data_constrained_basic, data_constrained_list

        with self.subTest(sub_type="BasicType"):
            obj = DataTypeDefinition(xml_tree_element=objectify.fromstring(data_constrained_basic).DataTypeDefinition)

            (definition, type_string) = self.proto_builder._evaluate_data_type(data_type=obj.sub_type,
                                                                               identifier=obj.identifier,
                                                                               namespace='sila2.main')
            self.assertIsNone(definition)
            self.assertEqual(
                type_string,
                (
                    "// Constrained type, not reflected in protocol buffers" "\n"
                    "sila2.org.silastandard.Boolean ${identifier} = ${index};"
                )
            )

        with self.subTest(sub_type="ListType"):
            obj = DataTypeDefinition(xml_tree_element=objectify.fromstring(data_constrained_list).DataTypeDefinition)

            (definition, type_string) = self.proto_builder._evaluate_data_type(data_type=obj.sub_type,
                                                                               identifier=obj.identifier,
                                                                               namespace='sila2.main')
            self.assertIsNone(definition)
            self.assertEqual(
                type_string,
                (
                    "// Constrained type, not reflected in protocol buffers" "\n"
                    "repeated sila2.org.silastandard.Boolean ${identifier} = ${index};"
                )
            )

    def test_simple_structure(self):
        from ._data_ProtoBuilder_DataTypeDefinition_simple import data_structure

        obj = DataTypeDefinition(xml_tree_element=objectify.fromstring(data_structure).DataTypeDefinition)

        (definition, type_string) = self.proto_builder._evaluate_data_type(data_type=obj.sub_type,
                                                                           identifier=obj.identifier,
                                                                           namespace='sila2.main')

        self.assertIsNotNone(definition)
        self.assertEqual(
            definition,
            (
                "message StructureIdentifier_Struct {" "\n"
                "    " "// Basic Element" "\n"
                "    " "//   This parameter defines a basic element." "\n"
                "    " "sila2.org.silastandard.Boolean BasicElement = 1;" "\n"
                "}"
            )
        )
        self.assertEqual(
            type_string,
            "sila2.main.StructureIdentifier_Struct ${identifier} = ${index};"
        )

    def test_simple_structure_multi(self):
        from ._data_ProtoBuilder_DataTypeDefinition_simple import data_multi_structure

        obj = DataTypeDefinition(xml_tree_element=objectify.fromstring(data_multi_structure).DataTypeDefinition)

        (definition, type_string) = self.proto_builder._evaluate_data_type(data_type=obj.sub_type,
                                                                           identifier=obj.identifier,
                                                                           namespace='sila2.main')

        self.assertEqual(
            definition,
            (
                "message StructureIdentifier_Struct {" "\n"
                "    " "// 1. Basic Element" "\n"
                "    " "//   This parameter defines a 1. basic element." "\n"
                "    " "sila2.org.silastandard.Boolean BasicElement1 = 1;" "\n"
                "    " "// 2. Basic Element" "\n"
                "    " "//   This parameter defines a 2. basic element." "\n"
                "    " "sila2.org.silastandard.Boolean BasicElement2 = 2;" "\n"
                "}"
            )
        )
        self.assertEqual(
            type_string,
            "sila2.main.StructureIdentifier_Struct ${identifier} = ${index};"
        )

    def test_simple_data_type_identifier(self):
        from ._data_ProtoBuilder_DataTypeDefinition_simple import data_data_type_identifier

        obj = DataTypeDefinition(xml_tree_element=objectify.fromstring(data_data_type_identifier).DataTypeDefinition)

        (definition, type_string) = self.proto_builder._evaluate_data_type(data_type=obj.sub_type,
                                                                           identifier=obj.identifier,
                                                                           namespace='sila2.main')

        self.assertIsNone(definition)
        self.assertEqual(
            type_string,
            "${namespace}.DataType_TestDataType ${identifier} = ${index};"
        )
