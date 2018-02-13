import requests
from bs4 import BeautifulSoup
import sys
import time
import os
import pytest


def JobScrapping(url):

    # Try to get the connection established to our specified URL something is wrong it throws out an error message
    # All test cases needed - HTTP CONNECTION TIMEOUT AND REQUEST ISSUES test cases
    try:
        resp = requests.get(url, timeout=3)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err_http:
        print("Http Error:", err_http)
    except requests.exceptions.ConnectionError as err_connection:
        # reconnect=0
        # When error is there an error message is printed and prompts the user to retry connecting if the fixed issue
        # or exit the system
        print("Error collecting data from stack over flow due to internet issue or other URL issues")
        status = input("Do you want to retry connecting , YES or NO")
        if status == "yes":
            main()
        else:
            sys.exit(1)
    except requests.exceptions.Timeout as err_timeout:
        print("Timeout Error:", err_timeout)
    except requests.exceptions.RequestException as error:
        print("OOps: Something Else", error)

    ParsingData(resp)


def ParsingData(resp):
    # Get the content from the specified URL as XML format for me to parse
    soup = BeautifulSoup(resp.content, features="xml")

    job_title = soup.findAll('item')

    # This loops goes throughout all the listing in the xml file and then extracts the needed information to be printed
    # on the screen
    while True:
        job_number = 0
        LoadingScreen()
        for item in job_title:

            job_number = job_number + 1

            article_author = item.author.text

            title = item.title.text

            head, sep, tail = title.partition('at')

            print("Job Title:", head, "\n", "Posted by:", article_author, "\n", "Location:", item.location.text, "\n",
                  "Check job at :", item.link.text, "\n", "Category :", item.category.text, "\n",job_number)

            print("___________________________________________________________________________________________________")

        print("There are", (len(job_title)), "Jobs within 50 miles radius from Bridgewater \n")

        analyzingdata(job_number)

# Check if there is no result due to error or no posting user can either quit or refresh the lis


def analyzingdata(job_number):

            if job_number == 0:

                print("It look like there are no jobs in the Area")

            choice = input("To Refresh List press R or 0 to Quit: ")

            if choice == "r":
                os.system('cls')

            elif choice == "0":

                exit()

# setting up the url in main function since rss feed can be changed.


def LoadingScreen():

    toolbar_width = 45

    # setup toolbar
    print("Establishing Connection To Stackoverflow")
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['

    for i in range(toolbar_width):
        time.sleep(0.1)
        # update the bar
        sys.stdout.write("=")
        sys.stdout.flush()

    sys.stdout.write("\n")


def main():

    print("This program will show all jobs available within 50 mile radius from Bridgwater")
    print("Press Enter To Continue . . .")
    input("")

    JobScrapping("https://stackoverflow.com/jobs/feed?l=02324&u=Miles&d=50")


if __name__ == "__main__":
    main()





