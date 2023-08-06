"""
________________________________________________________________________

:PROJECT: SiLA2_python

*SiLA service description parser*

:details: SiLA Service description parser. This class is used to describe
          a complete SiLA Service (server/client pair)

:file:    service_descriptor_parser.py
:authors: Mark Dörr (mark@uni-greifswald.de)
          Timm Severin (timm.severin@tum.de)

:date: (creation)          2018-05-30
:date: (last modification) 2019-11-01

.. todo:: - Offer service descriptor file as XML/SDL (Service Description Language)?
          - Implement the default structure to allow writing a sample file

________________________________________________________________________

  **Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.

________________________________________________________________________

"""

# import general packages
import logging
import os
import glob
import json

# meta information packages
from typing import Union
from typing import Dict, Any

class ServiceDescriptorParser:
    """This class is used to describe a complete SiLA2 service by the help of a JSON file."""

    description_dictionary: Dict[str, Any]
    file_json: str

    def __init__(self, project_dir: Union[str, None] =  None, service_description: Union[str, None] = "service_description") :
        """
        Class initialiser

        :param input_file: The .json file from which to read the service description. Can be None to create an empty
                           dictionary.
        """
        
        # prepare the storage dictionary
        self.description_dictionary = {}

        filename_pattern = os.path.join(project_dir, service_description)

        descr_filename_lst_json = glob.glob(filename_pattern + "*.json")

        if len(descr_filename_lst_json) == 1 :
            logging.debug(f"json input found: {descr_filename_lst_json[0]}")

            self.descr_filename_json = descr_filename_lst_json[0]
            self.load_json_file()

        if 'service_type' not in self.description_dictionary:
            logging.warning('No "service_type" given in service description file. Set to "Unknown type".')
            self.description_dictionary['service_type'] = 'Unknown Type'

    def set_input_json_file(self, input_file: str):
        """
        Set the name of descriptor file.

        :param input_file: Name of the file from which to load data.
        """
        self.descr_filename_json = input_file

        self.load_json_file()

    def get_input_json_file(self) -> str:
        """
        Returns the currently used input file.

        :returns: String with the input file used.
        """
        return self.descr_filename_json

    def load_json_file(self) -> bool:
        """
        Load the json file with the service description.

        :returns: Successfully loaded the JSON file.
        """

        if self.descr_filename_json is None:
            logging.error('No filename defined.')
            return False

        try:
            with open(self.descr_filename_json, 'r') as file_input:
                try:
                    self.description_dictionary = json.load(file_input)
                    logging.info('Loaded JSON descriptor file {input_file}.'.format(input_file=self.descr_filename_json))
                except Exception as err:
                    logging.error('An error occurred while loading JSON file {input_file}: {error_message}.'.format(
                        input_file=self.descr_filename_json,
                        error_message=err
                    ))
                    return False
        except FileNotFoundError:
            logging.error('Given input file "{input_file}" does not exist.'.format(input_file=self.descr_filename_json))
            return False
        except Exception as err:
            logging.error('Failed to read input file "{input_file}: {error_message}."'.format(
                input_file=self.descr_filename_json,
                error_message=err
            ))
            return False

        return True

    def write_json_file(self) -> bool:
        """
        Writes the json file back to the stored location.

        :returns: Write process successful.
        """

        if self.descr_filename_json is None:
            logging.error('No filename defined.')
            return False

        try:
            with open(self.descr_filename_json, 'w') as file_output:
                try:
                    json.dump(self.description_dictionary, file_output)
                    logging.info('Successfully wrote service description to JSON file {output_file}.'.format(
                        output_file=self.descr_filename_json
                    ))
                except Exception as err:
                    logging.error('Failed to write JSON descriptor file {output_file}: {error_message}.'.format(
                        output_file=self.descr_filename_json,
                        error_message=err
                    ))
                    return False
        except Exception as err:
            logging.error('Failed to write service description to file {output_file}: {error_message}.'.format(
                output_file=self.descr_filename_json,
                error_message=err
            ))
            return False

        return True
