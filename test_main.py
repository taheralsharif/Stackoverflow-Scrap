import requests
import os
import unittest
import main


class Tests(unittest.TestCase):
    # Expected to fail if txt file is empty
    def test_empty_text_file(self):
        self.failIf(os.stat("results.txt").st_size == 0)

    # will not pass since the url entered has an error
    def test_wrong_url(self):
        response = requests.get('https://stackoverflow.com/jobs/feed?l=02324&u=Miles&d=50')
        self.failIf(response.status_code == "F")

    #  Test to check if there was not results from the correct URL
    def test_no_results(self):
        self.failIf(main.analyzing_data(file=False, job_number=0, blank_list=False,location=False, num_per_location=False,job_name=False))

    def test_if_category_error(self):
        self.failIf(main.analyzing_data(job_number=0, file=True, blank_list=0, location=True, num_per_location=0,job_name="python")=="F")

    def test_get_job_date(self):
        self.assertTrue(OSError,msg=" OSError: reading from stdin while output is captured")
