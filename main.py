import requests
from bs4 import BeautifulSoup
import sys
import time
from collections import Counter
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim


def job_scrapping(url):
    # Try to get the connection established to our specified URL something is wrong it throws out an error message
    # All test cases needed - HTTP CONNECTION TIMEOUT AND REQUEST ISSUES test cases
    try:
        resp = requests.get(url, timeout=3)
        # print(resp.status_code)

    except requests.exceptions.HTTPError as err_http:
        print("Http Error:", err_http)
    except requests.exceptions.ConnectionError as err_connection:
        # reconnect=0
        # When error is there an error message is printed and prompts the user to retry connecting if the fixed issue
        # or exit the system
        print(err_connection, "\n")
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

    parsing_data(resp)


def parsing_data(website):
    # Get the content from the specified URL as XML format for me to parse
    soup = BeautifulSoup(website.content, features="xml")

    job_title = soup.findAll('item')

    # This loops goes throughout all the listing in the xml file and then extracts the needed information to be printed
    # on the screen
    while True:
        job_number = 0
        loading_screen()
        f = open("results.txt", "w+")
        empty_list = list()
        location = []
        job_category = input("what jobs are you looking for ex.python?")
        for item in job_title:
            selected_category = item.category.text
            selected_location = item.location.text
            user_location = selected_location
            if selected_category == job_category:

                job_number = job_number + 1

                article_author = item.author.text

                title = item.title.text

                head, sep, tail = title.partition('at ')

                # Writes the data to the txt file results
                f.write(
                    "Job Title:" + head + "\n" + "Posted by:" + article_author + "\n" + "Location:" + item.location.text +
                    "\n" + "Check job at :" + item.link.text + "\n" + "Category :" + item.category.text + "\n" + str(
                        job_number) + "\n")

                print("Job Title:", head, "\n", "Posted by:", article_author, "\n", "Location:", item.location.text,
                      "\n",
                      "Check job at :", item.link.text, "\n", "Category :", item.category.text, "\n", job_number)
                print("_______________________________________________________________________________________________")

                location.append(user_location)
        else:
            print(job_category + " Jobs are not available in the surrounding areas , Please try another category","\n")
            main()

        no_duplicate_list = list(set(location))

        num_per_location = Counter(location)

        analyzing_data(job_number, f, empty_list, no_duplicate_list, num_per_location,job_category)


# Check if there is no result due to error or no posting user can either quit or refresh the lis

def analyzing_data(job_number, file, blank_list, location, num_per_location,job_name):
    if job_number == 0:
        print("It looks like there are no jobs in the Area")
        return blank_list

    choice = input("If you want to see the map type -> map or -> 0 to Quit:,\n ")

    if choice == "map":
        location_selector(location, num_per_location,job_name)

    elif choice == "0":

        exit()
        file.truncate()


# setting up the url in main function since rss feed can be changed.




def location_selector(cities, num_per_location,job_name):
    cities_requested = []
    global item

    print("Cities where " + job_name + " jobs are avaialbe to Choose from: ")

    for i in cities:
        print(i)

    i = 0
    while 1:
        i += 1
        item = input(
            'Enter all areas with State ex:(Boston,MA) you want to see on the map, thern press enter twice when done %d: ' % i)
        if item == '':
            break
        cities_requested.append(item)
        print(cities_requested)
    map(cities_requested, num_per_location)


def map(cities_requested, num_per_location):
    # print(cities)

    map = Basemap(llcrnrlon=-73, llcrnrlat=40.9, urcrnrlon=-69.9, urcrnrlat=42.9,
                  projection='lcc', lat_0=42, lon_0=-71, resolution='h')

    # load the shapefile, use the name 'states'
    map.readshapefile('st99_d00', name='states', drawbounds=True)
    map.fillcontinents(color='orange', lake_color='aqua')

    map.bluemarble()

    # Get the location of each city and plot it
    geolocator = Nominatim()
    for (city) in cities_requested:
        loc = geolocator.geocode(city)
        x, y = map(loc.longitude, loc.latitude)
        map.plot(x, y, marker="1", color='Red', markersize=20)
        plt.text(x, y, city, fontsize=8, fontweight='normal',
                 ha='left', va='center', color='k', bbox=dict(facecolor='b', alpha=0.1))
        plt.title(num_per_location, fontsize=8, color='Black')

    plt.show()
    exit()


def loading_screen():
    toolbar_width = 45

    # setup toolbar
    print("Establishing Connection To Stackoverflow")
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))

    for i in range(toolbar_width):
        time.sleep(0.1)
        # update the bar
        sys.stdout.write("=")
        sys.stdout.flush()

    sys.stdout.write("\n")


def main():
    print("This program will show all jobs available within 50 mile radius from Bridgewater")

    job_scrapping("https://stackoverflow.com/jobs/feed?l=02324&u=Miles&d=50")


if __name__ == "__main__":
    main()