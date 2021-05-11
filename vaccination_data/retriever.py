#!/usr/bin/env python

# This module uses resources from the Our World in Data Project by Oxford University.
import requests
import sys
import time
import csv
import json

# Takes arguments unparsed population file, removes all non-recent 
# population data, and outputs a parsed file.
# TODO: remove blank rows
def population_parser(unparsed, parsed):
    parsed_writer = csv.writer(parsed)
    # Go through each row in unparsed file
    for row in csv.reader(unparsed):
        # If the row is not blank, write only the country name, ISO code,
        # and most recent population data to the parsed file.
        if any(field.strip() for field in row):
            parsed_writer.writerow((row[0], row[1], row[58]))

# Takes a parsed population file and ouputs a json mapping country names to populations
def make_pop_json(pop_csv, pop_json):
    pop_reader = csv.reader(pop_csv)
    pop_dict = dict((row[0], row[2]) for row in pop_reader)
    print(json.dumps(pop_dict, pop_json))
    json.dump(pop_dict, pop_json)
    print("here")



# Web address for directory containing vaccination data.
url_vax = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/"
url_jhu = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/"
url_pop = "https://datahub.io/JohnSnowLabs/population-figures-by-country/r/"

# Every 24 hours, retieve data files from the server
while 1:
    # Retrieve each data file - vacinations, loations, manufacturers,
    # and vacinations by state
    vax = requests.get(url_vax + "vaccinations.csv")
    if not vax:
        print("error: vaccinations.csv not found")
    vax_by_man = requests.get(url_vax + "vaccinations-by-manufacturer.csv")
    if not vax_by_man:
        print("error: vaccinations-by-manufacturer.csv not found")
    locations = requests.get(url_vax + "locations.csv")
    if not locations:
        print("error: locations.csv not found")
    us_state_vax = requests.get(url_vax + "us-state-vaccinations.csv")
    if not us_state_vax:
        print("error: us-state-vaccinations.csv not found")
    full_data = requests.get(url_jhu + "full_data.csv")
    if not full_data:
        print("error: full_data.csv not found")
    pop_fig_by_country = requests.get(url_pop + "population-figures-by-country-csv.csv")
    if not pop_fig_by_country:
        print("error: population-figures-by-country-csv.csv not found")

    # Open every data file, including parsed files
    vax_file = open("vaccinations.csv", "w")
    vax_by_man_file = open("vaccinations-by-manufacturer.csv", "w")
    locations_file = open("locations.csv", "w")
    us_state_vax_file = open("us-state-vaccinations.csv", "w")
    full_data_file = open("full-data.csv", "w")
    pop_fig_by_country_file = open("population-figures-by-country-csv.csv", "w")
    pop_fig_by_country_file_parsed = open("population-figures-by-country-csv-parsed.csv", "w")
    vax_file_parsed = open("vaccinations-parsed.csv", "w")

    # Now, write all unparsed files.
    vax_file.write(vax.text.encode("utf-8"))
    vax_by_man_file.write(vax_by_man.text.encode("utf-8"))
    locations_file.write(locations.text.encode("utf-8"))
    us_state_vax_file.write(us_state_vax.text.encode("utf-8"))
    full_data_file.write(full_data.text.encode("utf-8"))
    pop_fig_by_country_file.write(pop_fig_by_country.text.encode("utf-8"))
    vax_file_parsed.write(vax.text.encode("utf-8"))

    # Format the population file
    pop_fig_by_country_file.close()
    pop_fig_by_country_file_unparsed = open("population-figures-by-country-csv.csv", "r")
    population_parser(pop_fig_by_country_file_unparsed, pop_fig_by_country_file_parsed)

    # Convert the population file to a json
    pop_fig_by_country_file_parsed.close()
    pop_fig_by_country_file_parsed = open("population-figures-by-country-csv-parsed.csv", "r")
    pop_fig_by_country_json = open("../json_io_files/population-figures-by-country-json.json", "w")
    make_pop_json(pop_fig_by_country_file_parsed, pop_fig_by_country_json)

    # Close all files that are still open
    vax_file.close()
    vax_by_man_file.close()
    locations_file.close()
    us_state_vax_file.close()
    full_data_file.close()
    pop_fig_by_country_file_unparsed.close()
    pop_fig_by_country_file_parsed.close()
    vax_file_parsed.close()
    pop_fig_by_country_json.close()

    time.sleep(86400)