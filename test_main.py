import requests
import os
import unittest
import main


class Tests(unittest.TestCase):
    # Expected to fail if txt file is empty
    def test_empty_text_file(self):
        self.failIf(os.stat("results.txt").st_size == 0)

    # will pass since the url used is correct
    def test_correct_url(self):
        self.failIf(main.job_scrapping(url="https://stackoverflow.com/jobs/feed?l=02324&u=Miles&d=50"))

    # will not pass since the url entered has an error
    def test_wrong_url(self):
        response = requests.get('https://stackoverfow.com/jobs/feed?l=02324&u=Miles&d=50')
        self.failIf(response.status_code != 200)

    #  Test to check if there was not results from the correct URL
    def test_no_results(self):
        self.failIf(main.analyzing_data(file=False, job_number=0, blank_list=False))
