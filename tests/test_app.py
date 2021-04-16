import os
import json
import pytest
import sys
import subprocess
import filecmp

@pytest.fixture
def data():
    pytest.NUM_TEST_INPUT = 10

class TestApp():
    def test_app(self, data):
        for count in range(1, pytest.NUM_TEST_INPUT):
            test_input_file = "/tests/input/test_input_file_" + str(count) + ".txt"
            subprocess.call([sys.executable, "main.py", test_input_file])
            output_report = os.getcwd() + "/report.csv"
            expected_output_report = os.getcwd() + "/tests/output/test_output_report_" + str(count) + ".csv"
            expected_output_report_summary = os.getcwd() + "/tests/output/test_output_summary_" + str(count) + ".txt"
            assert os.path.isfile(output_report) == True
            assert filecmp.cmp(output_report, expected_output_report, shallow=False)
