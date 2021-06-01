#!/usr/bin/env python

# This module contains all functions that manipulate various files to create json files.
import requests
import sys
import time
import csv
import json

# Takes a parsed csv file and ouputs a json mapping
# to data columns to each other.
def make_json(csv_file, json_file, index_1, index_2):
    csv_reader = csv.reader(csv_file)
    aux_dict = dict((row[index_1], row[index_2]) for row in csv_reader)
    json.dump(aux_dict, json_file)

# Takes the parsed population and vaccination files (each from different sources)
# and makes a parsed json of mapping country names to ISO codes
def make_iso_json(pop_csv, vax_csv, r_csv, iso_json):
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

# Outputs a master json mapping iso codes to a dictionary of data containing 
def make_master_json(pop_json, vax_json, death_json, case_json, r_json, iso_json, master_json):
    # Convert all the json files to dictionaries
    pop_dict = json.load(pop_json)
    vax_dict = json.load(vax_json)
    death_dict = json.load(death_json)
    case_dict = json.load(case_json)
    r_dict = json.load(r_json)
    iso_dict = json.load(iso_json)

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
            master_dict[iso_dict[key]]["vac_rate"] = 1000
        else:
            master_dict[iso_dict[key]]["vac_rate"] = vax_dict[key]

    # Now add in all r values
    for key in r_dict:
        # If this country was not in the population dictionary or vaccination
        # dictionary, skip over set defaults for population and vaccination
        # rate.  Otherwise, just append r data
        if not iso_dict[key] in master_dict:
            master_dict[iso_dict[key]] = {"population" : "",
                                          "vac_rate" : "1000"}

        # If there is an entry but the field is empty, use the default
        if r_dict[key] == "":
            master_dict[iso_dict[key]]["r"] = 2.1
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
                                                  "vac_rate" : "1000",
                                                  "r" : "2.1"}
                # If the country has no data for deaths or cases, use default
                elif case_dict[key] == "" or death_dict[key] == "":
                    master_dict[iso_dict[key]]["mortality"] = 5
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
        master_dict[key]["vac_start"] = 200
        master_dict[key]["vac_uptake"] = 80.1
        master_dict[key]["vac_efficacy"] = 85
        master_dict[key]["avg_days_in_exposed"] = 14
        master_dict[key]["avg_days_in_infected"] = 14
        if not "population" in master_dict[key]:
            master_dict[key]["population"] = ""
        if not "vac_rate" in master_dict[key]:
            master_dict[key]["vac_rate"] = 1000
        if not "r" in master_dict[key]:
            master_dict[key]["r"] = 2.1
        if not "mortality" in master_dict[key]:
            master_dict[key]["mortality"] = 5

    # Now, make master json
    json.dump(master_dict, master_json)