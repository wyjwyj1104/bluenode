import os
import json

class StandardDefinitionItem:
    def __init__(self, data_type, max_length):
        """
        StandardDefinitionItem Constructor

        Initializes private variables, to manipulate the LXY data item values,
        including data type and max length.

        :param data_type: Data type value of one LXY data
        :param max_length: Max length value of one LXY data.
        """
        self.__data_type = data_type
        self.__max_length = max_length

    def getDataType(self):
        """
        Getter for private variable data_type.
        :return __data_type: Data type value of current LXY data.
        """
        return self.__data_type

    def getMaxLength(self):
        """
        Getter for private variable max_length.
        :return __data_type: Max length value of current LXY data.
        """
        return self.__max_length

    def __str__(self):
        """
        Overrided toString function for printing, dev purpose.
        :return str: visualized string data of the LXY data.
        """
        return '[' + self.__data_type + ',' + str(self.__max_length) + ']'

class StandardDefinition:
    def __init__(self):
        """
        StandardDefinition Constructor

        Initializes private variables, including fixed file paths, such as
        report.csv and summary.txt, and other values to be accessed from scope.
        """
        self.__file_path = ""
        self.__standard_definitions = {}
        self.__error_codes = {}
        self.__report = None
        self.__report_file_path = os.getcwd() + "/report.csv"
        self.__report_summary = None
        self.__report_summary_file_path = os.getcwd() + "/summary.txt"

    def loadErrorCodes(self, file_path):
        """
        Load error codes data from error_codes.json.

        Loads all the initial error codes data from file given,
        providing the data to be used for error handling and message outputs
        using the template given in the file, loaded into the system with
        dictionaries in StandardDefinition to be used for further processing.

        :param file_path: File path of the error_codes.json.
        """
        error_file = loadFileP(file_path)
        data = json.loads(error_file.read())
        for e in data:
            self.__error_codes[e["code"]] = e["message_template"]

    def load(self, file_path):
        """
        Load standard definition data from standard_definition.json.

        Loads all the initial standard definition data from file given,
        providing the data to be processed with data loaded from input_file.txt,
        loaded into the system with dictionaries and StandardDefinitionItem
        object values.

        :param file_path: File path of the standard_definition.json.
        """
        self.open_report()
        self.__file_path = file_path
        sd_file = loadFileP(self.__file_path)
        data = json.loads(sd_file.read())
        for l in data:
            key = l["key"]
            sub_sections = {}
            for sub in l["sub_sections"]:
                sub_key = sub["key"]
                sub_data_type = sub["data_type"]
                sub_max_length = sub["max_length"]
                sub_sections[sub_key] = StandardDefinitionItem(sub_data_type, sub_max_length)
            self.__standard_definitions[key] = sub_sections

    def open_report(self):
        """
        Opens the data file to be generated after the processing.
        1. report.csv
        2. summary.txt

        Creates the file pointers to be accessed through parsing and writing.

        """
        self.__report = open(self.__report_file_path, 'w')
        self.__report.writelines("Section,Sub-Section,Given DataType,Expected DataType,Given Length,Expected MaxLength,Error Code\n")
        self.__report_summary = open(self.__report_summary_file_path, 'w')

    def write_report(self, line):
        """
        Write a line of string into the opened report file. (report.csv)

        :param line: String value to write to the file with.
        """
        if self.__report:
            self.__report.writelines(line)

    def write_summary(self, line):
        """
        Write a line of string into the opened report summary file. (summary.txt)

        :param line: String value to write to the file with.
        """
        if self.__report_summary:
            self.__report_summary.writelines(line)

    def generate_summary_line(self, section_key, sub_section_key, error_message):
        """
        Generates the string to match the format of summary.txt on each line.

        Gathers all the data value from parsing function, and generates a string
        to write to the summary.txt file, matching the syntax and convention as
        expected output.

        :param section_key: LXY key value.
        :param sub_section_key: LX key value.
        :param error_message: Error message formatted from parsed result.
        :return result: Returns string value of the generated result.
        """
        return error_message.replace("LXY", sub_section_key).replace("LX", section_key) + '\n'

    def generate_report_line(self, section_key, sub_section_key, given_data_type, expected_data_type, given_data_len, expected_max_length, error_code):
        """
        Generates the string to match the format of report.csv on each line.

        Gathers all the data value from parsing function, and generates a string
        to write to the report.csv file, matching the syntax and convention as
        expected output.

        :param section_key: LXY key value.
        :param sub_section_key: LX key value.
        :param given_data_type: Data type value from parsed line.
        :param expected_data_type: LXY matching data type.
        :param given_data_len: Data length value from parsed line.
        :param expected_max_length: LXY matching data max length.
        :param error_code: Error code from parsing result.
        :return result: Returns string value of the generated result.
        """
        result = ""
        result += section_key + ','
        result += sub_section_key + ','
        result += (given_data_type if given_data_type else "") + ','
        result += expected_data_type + ','
        result += (str(given_data_len) if given_data_len else "") + ','
        result += str(expected_max_length) + ','
        result += error_code + '\n'
        return result

    def finish_report(self):
        """
        Close all possible opened file pointers. (Manual destructor)
        """
        if self.__report:
            self.__report.close()
        if self.__report_summary:
            self.__report_summary.close()

    def check_int(self, val):
        """
        Validation function to check if a string value can be converted into
        int.

        An util function that tries converting string into int, returns True if
        possible, else False.

        :param val: String value to validate with.
        :return Boolean: Returns True/False of the validation.
        """
        try:
            int(val)
            return True
        except ValueError:
            return False

    def parse(self, line, line_length):
        """
        Main parsing logic.

        Parses each line loaded from input_file.txt that are not empty.
        Generates proper data to be written to the report and summary.
        Write over the opened report and summary file with updated data
        processed from the function.

        Main engine logic to process the data from file to the report template
        given.

        eg.
        L1&99&&A&1
        --> ['L1','99','','A','1']
        --> L1,L11,digits,digits,2,1,E03
        --> L11 field under section L1 fails the max length ...

        :param line: Array of strings parsed from each line in the input_file.txt.
        :param line_length: Length of the input data for each line.
        """
        if line_length > 0:
            section_key = line[0]
            section = self.__standard_definitions[section_key]
            seciton_len = len(section)

            sub_section = None
            expected_data_type = None
            expected_max_length = None
            same_type = False
            for count in range(0, seciton_len):
                # Reset data values
                given_data = None
                given_data_type = None
                given_data_len = 0
                error_code = None
                error_message = None
                sub_section_key = section_key + str(count+1)
                sub_section = section[sub_section_key]
                expected_data_type = sub_section.getDataType()
                expected_max_length = sub_section.getMaxLength()
                if count+1 < line_length:
                    given_data = line[count+1]
                    if given_data:
                        given_data_type = "digits" if self.check_int(given_data) else "word_characters" if isinstance(given_data, str) else "others"
                    given_data_len = len(given_data)
                    if given_data_type == expected_data_type:
                        same_type = True

                if line_length-1 < seciton_len:
                    # "message_template": "LXY field under section LX is missing."
                    error_code = "E05"
                    error_message = self.__error_codes[error_code]
                elif given_data_len <= 0:
                    # "message_template": "LXY field under section LX fails all the validation criteria."
                    error_code = "E04"
                    error_message = self.__error_codes[error_code]

                if given_data_len > expected_max_length:
                    # "message_template": "LXY field under section LX fails the max length (expected: {data_type}) validation, however it passes the data type ({data_type}) validation"
                    error_code = "E03"
                    if same_type:
                        error_message = self.__error_codes[error_code].format(expected_max_length=expected_max_length, given_data_type=given_data_type)
                elif given_data_len != 0:
                    if not same_type:
                        # "message_template": "LXY field under section LX fails the data type (expected: {data_type}) validation, however it passes the max length ({max_length}) validation"
                        error_code = "E02"
                        error_message = self.__error_codes[error_code].format(data_type=expected_data_type, max_length=expected_max_length)

                if not error_code and not error_message:
                    error_code = "E01"
                    error_message = self.__error_codes[error_code]

                # Write to report.csv
                report_line = self.generate_report_line(section_key, sub_section_key, given_data_type, expected_data_type, given_data_len, expected_max_length, error_code)
                self.write_report(report_line)

                # Write to summary.txt
                summary_line = self.generate_summary_line(section_key, sub_section_key, error_message)
                self.write_summary(summary_line)

def loadFileP(file_path):
    """
    Open file validation function.

    An util function that opens the FileIO with the validated file path and
    returns the opened file pointer for further access.

    :param file_path: Path of the file to open and validate with.
    :return FileIO: Returns the opened file pointer after validation.
    """
    if not os.path.isfile(file_path):
       print("File path {} does not exist. Exiting...".format(file_path))
       sys.exit()
    try:
        return open(file_path)
    except IOError:
        raise Exception('ERROR::IOERROR')

def main(standard_definition):
    """
    Application main function.

    Load from input_file.txt in current directory, processes the input data
    using standard definition data initialized from standard_definition.json.

    Closes all the file pointers opened from the process.

    :param standard_definition: StandardDefinition object that was created
                                from init function
    """

    input_file_path = os.getcwd() + "/input_file.txt"
    input_file = loadFileP(input_file_path)
    for line in input_file:
        parsed_line = line.strip().split("&")
        parsed_line_len = len(parsed_line)
        standard_definition.parse(parsed_line, parsed_line_len)

    standard_definition.finish_report()


def init():
    """
    Application main initialization function.

    Load from standard_definition.json in current directory, processes the
    initial standard definition data into the system for further operations.

    Also loads the error codes and message templates from error_code.json.

    :return sd: StandardDefinition object loaded with initial data.
    """
    sd_file_path = os.getcwd() + "/standard_definition.json"
    sd = StandardDefinition()
    sd.load(sd_file_path)
    ec_file_path = os.getcwd() + "/error_codes.json"
    sd.loadErrorCodes(ec_file_path)
    return sd

if __name__ == "__main__":
    """
    Application main function.

    Fully operates as guided in INSTRUCTIONS.md, reads in the data file and
    process the data with system logic, output and generates proper report and
    summary data on to the files, report.csv and summary.txt.
    """
    main(init())
