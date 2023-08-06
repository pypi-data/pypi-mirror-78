"""This module defines xml-data that can be used to test the DataTypeDefinition data type"""

data_basic_template = """
<root><DataTypeDefinition>
    <Identifier>BasicIdentifier</Identifier>
    <DisplayName>Basic Identifier</DisplayName>
    <Description>Definition of an identifier for a basic data type</Description>
    <DataType>
        <Basic>{basic_type}</Basic>
    </DataType>
</DataTypeDefinition></root>
"""

data_basic = {
    'Boolean': data_basic_template.format(basic_type="Boolean"),
    'String': data_basic_template.format(basic_type="String"),
    'Integer': data_basic_template.format(basic_type="Integer"),
    'Real': data_basic_template.format(basic_type="Real"),
    'Binary': data_basic_template.format(basic_type="Binary"),
    'Date': data_basic_template.format(basic_type="Date"),
    'Time': data_basic_template.format(basic_type="Time"),
    'Timestamp': data_basic_template.format(basic_type="Timestamp")
}

data_basic_invalid = data_basic_template.format(basic_type="Invalid")

data_list = """
<root><DataTypeDefinition>
    <Identifier>ListIdentifier</Identifier>
    <DisplayName>List Identifier</DisplayName>
    <Description>Definition of an identifier for a list data type</Description>
    <DataType>
        <List>
            <DataType>
                <Basic>Boolean</Basic>
            </DataType>
        </List>
    </DataType>
</DataTypeDefinition></root>
"""

data_structure = """
<root><DataTypeDefinition>
    <Identifier>StructureIdentifier</Identifier>
    <DisplayName>Structure Identifier</DisplayName>
    <Description>Definition of an identifier for a structure data type</Description>
    <DataType>
        <Structure>
            <Element>
                <Identifier>BasicElement</Identifier>
                <DisplayName>Basic Element</DisplayName>
                <Description>This parameter defines a basic element.</Description>             
                <DataType>
                    <Basic>Boolean</Basic>
                </DataType>
            </Element>
        </Structure>
    </DataType>
</DataTypeDefinition></root>
"""

data_multi_structure = """
<root><DataTypeDefinition>
    <Identifier>StructureIdentifier</Identifier>
    <DisplayName>Structure Identifier</DisplayName>
    <Description>Definition of an identifier for a structure data type</Description>
    <DataType>
        <Structure>
            <Element>
                <Identifier>BasicElement1</Identifier>
                <DisplayName>1. Basic Element</DisplayName>
                <Description>This parameter defines a 1. basic element.</Description>             
                <DataType>
                    <Basic>Boolean</Basic>
                </DataType>
            </Element>
            <Element>
                <Identifier>BasicElement2</Identifier>
                <DisplayName>2. Basic Element</DisplayName>
                <Description>This parameter defines a 2. basic element.</Description>             
                <DataType>
                    <Basic>Boolean</Basic>
                </DataType>
            </Element>
        </Structure>
    </DataType>
</DataTypeDefinition></root>
"""

data_constrained_basic = """
<root><DataTypeDefinition>
    <Identifier>ConstrainedIdentifier</Identifier>
    <DisplayName>Constrained Identifier</DisplayName>
    <Description>Definition of an identifier for a constrained data type</Description>
    <DataType>
        <Constrained>
            <DataType>
                <Basic>Boolean</Basic>
            </DataType>
            <Constraints>
                <!-- we do not define any constraints here -->
            </Constraints>
        </Constrained>
    </DataType>
</DataTypeDefinition></root>
"""

data_constrained_list = """
<root><DataTypeDefinition>
    <Identifier>ConstrainedIdentifier</Identifier>
    <DisplayName>Constrained Identifier</DisplayName>
    <Description>Definition of an identifier for a constrained data type</Description>
    <DataType>
        <Constrained>
            <DataType>
                <List>
                    <DataType>
                        <Basic>Boolean</Basic>
                    </DataType>
                </List>
            </DataType>
            <Constraints>
                <!-- we do not define any constraints here -->
            </Constraints>
        </Constrained>
    </DataType>
</DataTypeDefinition></root>
"""


data_data_type_identifier = """
<root><DataTypeDefinition>
    <Identifier>DefinitionIdentifier</Identifier>
    <DisplayName>Definition Identifier</DisplayName>
    <Description>Definition of an identifier for a defined data type</Description>
    <DataType>
        <DataTypeIdentifier>TestDataType</DataTypeIdentifier>
    </DataType>
</DataTypeDefinition></root>
"""