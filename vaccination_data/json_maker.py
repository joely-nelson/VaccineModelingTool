#!/usr/bin/env python
# Author: Kenny Krivanek
# Purpose: This module contains all functions that manipulate various files to create json files.
import requests
import sys
import time
import csv
import json

# Takes a parsed csv file and ouputs a json mapping
# to data columns to each other.
def make_json(csv_file, json_file, index_1, index_2):
    """
    Takes a csv file and converts it into a single json file by mapping one column to
    another column

    PRE: the number of columns in csv_file is less than both
         index_1 + 1 and index_2 + 1.

    ARGS:
        - csv_file: any opened csv file with a number of columns that is less than both
          index_1 + 1 and index_2 + 1.
        - json_file: a json file that will map the keys in the column indicated by 
          index_1 to the values in the column indicated by index_2
        - index_1: column of the keys in the json (0-indexed)
        - index_2: column of the values in the json (0-indexed)
    """

    csv_reader = csv.reader(csv_file)
    aux_dict = dict((row[index_1], row[index_2]) for row in csv_reader)
    json.dump(aux_dict, json_file)

def make_iso_json(pop_csv, vax_csv, r_csv, iso_json):
    """
    Takes the parsed population, vaccination, and r files (each from different sources)
    and makes a parsed json of mapping country names to 3-letter ISO codes

    PRE: 
        The correct files are used for pop_csv, vax_csv, and r_csv

    ARGS:
        - pop_csv: the parsed population file obtained by running population_parser
          on the unparsed population file from JohnSnowLabs
        - vax_csv: the parsed vaccination file obtained by running vax_parser on 
          the "vaccinations" file from OWID
        - r_csv: the parsed reproduction number file obtained by running r_value_parser
          on the owid-covid-latest file from OWID
        - iso_json: a json file which maps the country names in each of the above files
          to the corresponding iso_codes in said files.

    NOTES:
        Micronesia is represented differently in the cases and deaths file,
        so an explicit modification has to be added here. 
    """

    iso_dict = {}
    # Add all ISO codes in population file
    for row in csv.reader(pop_csv):
        iso_dict[row[0]] = row[1]
    # Add all ISO codes in vaccination file
    for row in csv.reader(vax_csv):
        iso_dict[row[0]] = row[1]
    # Add all ISO codes in r-value file
    for row in csv.reader(r_csv):
        iso_dict[row[1]] = row[0]

    # Micronesia is listed differently in the deaths/cases file, so we'll
    # add the iso code right here for now.
    iso_dict["Micronesia (country)"] = "FSM"

    # Now convert the dictionary to a json_file
    json.dump(iso_dict, iso_json)

def make_master_json(pop_json, vax_json, death_json, case_json, r_json, iso_json, master_json):
    """
    Takes json files mapping iso codes to population, daily average COVID-19 vaccinations, and
    COVID-19 reproduction numbers, as well as json files mapping country names to COVID-19 
    weekly deaths and cases and a json file mapping country names to 3-letter ISO codes, and 
    produces a "master json" containing all the data necessary for running the modeling tool.

    PRE: The correct files are used for pop_json, vax_json, death_json, case_json, r_json,
         and iso_json

    ARGS:
        - pop_json: a json file mapping country names to population data for each country
        - vax_csv: a json file mapping country names to average daily vaccination rate
          over the last 7 days for each country
        - death_json: a json file mapping country names to the most recent weekly COVID-19
          death data for each country
        - case_json: a json file mapping country names to the most recent weekly COVID-19
          case data for each country
        - r_json: a json file mapping country names to reproduction values of COVID-19 for
          each country
        - iso_json: a json file which maps the country names in each of the above files
          to the corresponding iso_codes in said files.
        - master_json: a json containing ISO codes for each country mapped to a dictionary
          of data formatted as follows:
            {
                vac_start: number of days after the pandemic at which vaccinations start
                vac_rate: number of vaccinations per day
                vac_uptake: percentage of people willing to be vaccinated
                r: reproduction value of the virus
                mortality: mortality rate of the virus (weekly deaths/weely cases)
                avg_days_in_exposed: average number of days a person is exposed to the virus
                avg_days_in_infected: average number of days a person is infected with the virus
                vac_efficacy: Efficacy of vaccinations given at preventing death
            }
          Where data is unavailable for a given country, defaults provided by the file 
          global_defaults.json in the folder configuration_files will be used.
    """

    # Convert all the json files to dictionaries
    pop_dict = json.load(pop_json)
    vax_dict = json.load(vax_json)
    death_dict = json.load(death_json)
    case_dict = json.load(case_json)
    r_dict = json.load(r_json)
    iso_dict = json.load(iso_json)
    default_json = open("../configuration_files/global_defaults.json", "r")
    default_dict = json.load(default_json)
    default_json.close()

    # Dictionary containing a map of ISO codes to a list of data
    master_dict = {}

    # First, add all population data
    for key in pop_dict:
        master_dict[iso_dict[key]] = {"population" : pop_dict[key]}

    # Now, add all vaccination data
    for key in vax_dict:
        # If this country was not in the population dictionary, skip over
        # population for now and add vaccination data, otherwise just
        # append vaccination data
        if not iso_dict[key] in master_dict:
            master_dict[iso_dict[key]] = {"population" : ""}

        # If the field is empty, use the default
        if vax_dict[key] in master_dict:
            master_dict[iso_dict[key]]["vac_rate"] = default_dict["vac_rate"]
        else:
            master_dict[iso_dict[key]]["vac_rate"] = vax_dict[key]

    # Now add in all r values
    for key in r_dict:
        # If this country was not in the population dictionary or vaccination
        # dictionary, skip over set defaults for population and vaccination
        # rate.  Otherwise, just append r data
        if not iso_dict[key] in master_dict:
            master_dict[iso_dict[key]] = {"population" : "",
                                          "vac_rate" : default_dict["vac_rate"]}

        # If there is an entry but the field is empty, use the default
        if r_dict[key] == "":
            master_dict[iso_dict[key]]["r"] = default_dict["r"]
        else:
            master_dict[iso_dict[key]]["r"] = r_dict[key]

    # Now add all mortality data
    for key in death_dict:
        if key in iso_dict and (not death_dict[key] == "weekly_deaths") and \
            (not case_dict[key] == "weekly_cases"):
                # If this country was not in population or vaccination dictionary, 
                # set defaults for population, vaccination, and r data
                if not iso_dict[key] in master_dict:
                    master_dict[iso_dict[key]] = {"population" : "",
                                                  "vac_rate" : default_dict["vac_rate"],
                                                  "r" : default_dict["r"]}
                # If the country has no data for deaths or cases, use default
                elif case_dict[key] == "" or death_dict[key] == "":
                    master_dict[iso_dict[key]]["mortality"] = default_dict["mortality"]
                # If the country has no cases, put mortality rate as 0
                elif float(case_dict[key]) == 0:
                    master_dict[iso_dict[key]]["mortality"] = 0
                # Otherwise divide deaths by cases to get mortality rate
                else:
                    master_dict[iso_dict[key]]["mortality"] = float(death_dict[key]) \
                                                    / float(case_dict[key]) * 100

    # Now, make sure all entries are filled in through the master_dict,
    # setting the values to the defaults if they are not present.
    for key in master_dict:
        master_dict[key]["vac_start"] = default_dict["vac_start"]
        master_dict[key]["vac_uptake"] = default_dict["vac_uptake"]
        master_dict[key]["vac_efficacy"] = default_dict["vac_efficacy"]
        master_dict[key]["avg_days_in_exposed"] = default_dict["avg_days_in_exposed"]
        master_dict[key]["avg_days_in_infected"] = default_dict["avg_days_in_infected"]
        if not "population" in master_dict[key]:
            master_dict[key]["population"] = ""
        if not "vac_rate" in master_dict[key]:
            master_dict[key]["vac_rate"] = default_dict["vac_rate"]
        if not "r" in master_dict[key]:
            master_dict[key]["r"] = default_dict["r"]
        if not "mortality" in master_dict[key]:
            master_dict[key]["mortality"] = default_dict["mortality"]

    # Now, make master json
    json.dump(master_dict, master_json)