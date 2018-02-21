from nose.tools import assert_true
import requests
import os
import unittest
import main
from bs4 import BeautifulSoup


class Tests(unittest.TestCase):

    def test_empty_text_file(self):
        self.failIf(os.stat("results.txt").st_size == 0)

    def test_correct_url(self):
        response = requests.get('https://stackoverflow.com/jobs/feed?l=02324&u=Miles&d=50')
        assert_true(response.ok)

    def test_wrong_url(self):
        response = requests.get('https://stackoverfow.com/jobs/feed?l=02324&u=Miles&d=50')
        self.failIf(response.status_code != 200)

    #def test_print_blank_list(self):

#        self.failIf(main.parsing_data("https://stackoverflow.com/jobs/feed?l=Jordan&u=Miles&d=20") == "It looks like there are no jobs in the Area")

