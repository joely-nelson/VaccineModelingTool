#!/usr/bin/env python

# This module uses resources from the Our World in Data Project by Oxford University.
import requests
import sys
import time
import csv
import json
import vax_data_parser
import json_maker

# Web address for directory containing vaccination data.
url_vax = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/"
url_jhu = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/"
url_lat = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/"
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
    full_data = requests.get(url_jhu + "full_data.csv")
    if not full_data:
        print("error: full_data.csv not found")
    latest_data = requests.get(url_lat + "owid-covid-latest.csv")
    if not latest_data:
        print("error: owid-covid-latest.csv not found")
    pop_fig_by_country = requests.get(url_pop + "population-figures-by-country-csv.csv")
    if not pop_fig_by_country:
        print("error: population-figures-by-country-csv.csv not found")

    # Open every csv data file, including parsed files
    vax_file = open("vaccinations.csv", "w")
    vax_by_man_file = open("vaccinations-by-manufacturer.csv", "w")
    full_data_file = open("full-data.csv", "w")
    latest_data_file = open("owid-covid-latest.csv", "w")
    pop_fig_by_country_file = open("population-figures-by-country-csv.csv", "w")
    pop_fig_by_country_file_parsed = open("population-figures-by-country-csv-parsed.csv", "w")
    vax_file_parsed = open("vaccinations-parsed.csv", "w")
    death_file = open("weekly-deaths.csv", "w")
    case_file = open("weekly-cases.csv", "w")
    r_value_file = open("r-values.csv", "w")
    

    # Now, write all unparsed files.
    vax_file.write(vax.text.encode("utf-8"))
    vax_by_man_file.write(vax_by_man.text.encode("utf-8"))
    full_data_file.write(full_data.text.encode("utf-8"))
    pop_fig_by_country_file.write(pop_fig_by_country.text.encode("utf-8"))
    latest_data_file.write(latest_data.text.encode("utf-8"))

    # Parse the population file
    pop_fig_by_country_file.close()
    pop_fig_by_country_file_unparsed = open("population-figures-by-country-csv.csv", "r")
    vax_data_parser.population_parser(pop_fig_by_country_file_unparsed, 
        pop_fig_by_country_file_parsed)

    # Parse the vaccination file
    vax_file.close()
    vax_file_unparsed = open("vaccinations.csv", "r")
    vax_data_parser.vax_parser(vax_file_unparsed, vax_file_parsed)

    # Parse the full_data file for cases and deaths
    full_data_file.close()
    full_data_file_unparsed = open("full-data.csv", "r")
    vax_data_parser.cases_deaths_parser(full_data_file_unparsed, death_file, case_file)

    # Parse the latest data file for r-values
    latest_data_file.close()
    latest_data_file_unparsed = open("owid-covid-latest.csv")
    vax_data_parser.r_value_parser(latest_data_file_unparsed, r_value_file)

    # Convert the population file to a json
    pop_fig_by_country_file_parsed.close()
    pop_fig_by_country_file_parsed = open("population-figures-by-country-csv-parsed.csv", "r")
    pop_fig_by_country_json = open("../json_io_files/population-figures-by-country-json.json", "w")
    json_maker.make_json(pop_fig_by_country_file_parsed, pop_fig_by_country_json, 0, 2)

    # Convert the vaccination file to a json
    vax_file_parsed.close()
    vax_file_parsed = open("vaccinations-parsed.csv", "r")
    vax_json = open("../json_io_files/vaccinations.json", "w")
    json_maker.make_json(vax_file_parsed, vax_json, 0, 2)

    # Convert the death file to a json
    death_file.close()
    death_file = open("weekly-deaths.csv", "r")
    death_json = open("../json_io_files/weekly-deaths.json", "w")
    json_maker.make_json(death_file, death_json, 0, 1)

    # Convert the case file to a json
    case_file.close()
    case_file = open("weekly-cases.csv", "r")
    case_json = open("../json_io_files/weekly-cases.json", "w")
    json_maker.make_json(case_file, case_json, 0, 1)

    # Convert the r-data file to a json
    # Convert the case file to a json
    r_value_file.close()
    r_value_file = open("r-values.csv", "r")
    r_value_json = open("../json_io_files/r-values.json", "w")
    json_maker.make_json(r_value_file, r_value_json, 1, 2)

    # Make a json containing a dictionary mapping country names to ISO codes
    vax_file_parsed.close()
    vax_file_parsed = open("vaccinations-parsed.csv", "r")
    pop_fig_by_country_file_parsed.close()
    pop_fig_by_country_file_parsed = open("population-figures-by-country-csv-parsed.csv", "r")
    r_value_file.close()
    r_value_file = open("r-values.csv", "r")
    iso_json = open("../json_io_files/countries-to-iso.json", "w")
    json_maker.make_iso_json(pop_fig_by_country_file_parsed, vax_file_parsed, 
        r_value_file, iso_json)

    # Make master json mapping iso codes to a list containing population, vaccinations,
    # deaths, and cases, in that order.
    pop_fig_by_country_json.close()
    vax_json.close()
    death_json.close()
    case_json.close()
    iso_json.close()
    pop_fig_by_country_json = open("../json_io_files/population-figures-by-country-json.json", "r")
    vax_json = open("../json_io_files/vaccinations.json", "r")
    death_json = open("../json_io_files/weekly-deaths.json", "r")
    case_json = open("../json_io_files/weekly-cases.json", "r")
    r_value_json = open("../json_io_files/r-values.json", "r")
    iso_json = open("../json_io_files/countries-to-iso.json", "r")
    master_json = open("../json_io_files/master-json.json", "w")
    json_maker.make_master_json(pop_fig_by_country_json, vax_json, 
        death_json, case_json, r_value_json, iso_json, master_json)

    # Close all files that are still openvg
    vax_file_unparsed.close()
    vax_by_man_file.close()
    full_data_file_unparsed.close()
    death_file.close()
    case_file.close()
    latest_data_file_unparsed.close()
    pop_fig_by_country_file_unparsed.close()
    pop_fig_by_country_file_parsed.close()
    vax_file_parsed.close()
    r_value_file.close()
    pop_fig_by_country_json.close()
    vax_json.close()
    case_json.close()
    death_json.close()
    r_value_json.close()
    iso_json.close()
    master_json.close()
    print("All files closed")

    # Make the loop wait 1 day (86400s) before running again
    time.sleep(86400)