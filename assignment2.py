#Part II Download the Data

import urllib.request
def downloadData(url):

    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')


#Part III Process Data

import csv
import datetime
import logging


def processData(csv_text):

    logger = logging.getLogger('assignment2')
    person_dict = {}
    reader = csv.DictReader(csv_text.splitlines())

    for line_num, row in enumerate(reader, start=2):
        pid = int(row['id'])
        name = row['name']
        bday_str = row['birthday']

        try:
            day, month, year = bday_str.split('/')
            date_obj = datetime.date(int(year), int(month), int(day))
            person_dict[pid] = (name, date_obj)
        except Exception:
            logger.error(f"Error processing line #{line_num} for ID #{pid}")

    return person_dict

#Part IV Display/User Input

def displayPerson(pid, personData):

    record = personData.get(pid)
    if record:
        name, bdate = record
        print(f"Person #{pid} is {name} with a birthday of {bdate.isoformat()}")
    else:
        print("No user found with that id")

#Part V Putting it All Together

import argparse
import sys

def configureLogging():

    logger = logging.getLogger('assignment2')
    logger.setLevel(logging.ERROR)
    handler = logging.FileHandler('errors.log', mode='w')
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True,
                        help='URL to the CSV file of birthdays')
    args = parser.parse_args()

    # Download
    try:
        csvData = downloadData(args.url)
    except Exception as e:
        print(f"Failed to download data: {e}")
        sys.exit(1)

    configureLogging()

    personData = processData(csvData)


    while True:
        try:
            user_input = int(input("Enter an ID to lookup (<=0 to exit): "))
        except ValueError:
            print("Please enter a valid integer.")
            continue

        if user_input <= 0:
            break

        displayPerson(user_input, personData)

if __name__ == '__main__':
    main()
