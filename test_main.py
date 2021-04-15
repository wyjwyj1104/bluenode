import os
import json
import pytest
from bluenode.main import StandardDefinition, StandardDefinitionItem

@pytest.fixture
def data():
    pytest.sdi = StandardDefinitionItem("digits", 1)
    pytest.sd = StandardDefinition()
    pytest.error_codes = {
        "E01": "LXY field under segment LX passes all the validation criteria.",
        "E02": "LXY field under section LX fails the data type (expected: {data_type}) validation, however it passes the max length ({max_length}) validation",
        "E03": "LXY field under section LX fails the max length (expected: {expected_max_length}) validation, however it passes the data type ({given_data_type}) validation",
        "E04": "LXY field under section LX fails all the validation criteria.",
        "E05": "LXY field under section LX is missing.",
    }

    pytest.standard_definitions = {
        "L1":{ "L11":None, "L12":None, "L13":None },
        "L2":{ "L21":None, "L22":None },
        "L3":{ "L31":None },
        "L4":{ "L41":None, "L42":None },
        "L5":{ "L51":None, "L52":None, "L53":None, "L54":None, "L55":None }
        }

class TestStandardDefinitionItem():
    def test_sdi_getDataType(self, data):
        assert pytest.sdi.getDataType() == "digits"

    def test_sdi_getMaxLength(self, data):
        assert pytest.sdi.getMaxLength() == 1

    def test_sdi___str__(self, data):
        assert str(pytest.sdi)  == "[digits,1]"

class TestStandardDefinition():
    def test_sd_getReportFilePath(self, data):
        assert pytest.sd.getReportFilePath() == os.getcwd() + "/report.csv"

    def test_sd_getReportSummaryFilePath(self, data):
        assert pytest.sd.getReportSummaryFilePath() == os.getcwd() + "/summary.txt"


    def test_sd_loadErrorCodes(self, data):
        pytest.sd.loadErrorCodes(os.getcwd() + "/error_codes.json")
        assert len(pytest.sd.getErrorCodes()) > 0
        assert pytest.sd.getErrorCodes() == pytest.error_codes

    def test_sd_load(self, data):
        pytest.sd.load(os.getcwd() + "/standard_definition.json")
        assert len(pytest.sd.getStandardDefinitions()) > 0
        assert pytest.sd.getStandardDefinitions().keys() == pytest.standard_definitions.keys()

    def test_sd_check_int(self, data):
        assert pytest.sd.check_int("1") == True
        assert pytest.sd.check_int("1qwe") == False
