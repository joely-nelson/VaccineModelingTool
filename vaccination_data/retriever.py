#!/usr/bin/env python

# This module uses resources from the Our World in Data Project by Oxford University.
import requests
import sys
import time
import csv

# Takes arguments unparsed population file, removes all blank rows and non-recent 
# population data, and outputs a parsed file.
def population_parser(unparsed, parsed):
    parsed_writer = csv.writer(parsed)
    # Go through each row in unparsed file
    for row in csv.reader(unparsed):
        # If the row is not blank, write only the country name, ISO code,
        # and most recent population data to the parsed file.
        if any(field.strip() for field in row):
            parsed_writer.writerow((row[0], row[1], row[58]))

# def vaccination_parser(unparsed, parsed):

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
    us_state_vax = requests.get(url_vax + "us_state_vaccinations.csv")
    if not us_state_vax:
        print("error: us-state-manufacturer.csv not found")
    full_data = requests.get(url_jhu + "full_data.csv")
    if not full_data:
        print("error: us-state-manufacturer.csv not found")
    pop_fig_by_country = requests.get(url_pop + "population-figures-by-country-csv.csv")
    if not full_data:
        print("error: us-state-manufacturer.csv not found")

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

    # TODO: Format the vaccination file

    vax_file.close()
    vax_by_man_file.close()
    locations_file.close()
    us_state_vax_file.close()
    full_data_file.close()
    pop_fig_by_country_file_unparsed.close()
    pop_fig_by_country_file_parsed.close()
    vax_file_parsed.close()