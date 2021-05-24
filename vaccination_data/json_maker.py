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
def make_iso_json(pop_csv, vax_csv, iso_json):
    iso_dict = {}
    # Add all ISO codes in population file
    for row in csv.reader(pop_csv):
        iso_dict[row[0]] = row[1]
    # Add all ISO codes in vaccination file
    for row in csv.reader(vax_csv):
        iso_dict[row[0]] = row[1]

    # Micronesia is listed differently in the deaths/cases file, so we'll
    # add the iso code right here for now.
    iso_dict["Micronesia (country)"] = "FSM"

    # Now convert the dictionary to a json_file
    json.dump(iso_dict, iso_json)

# Outputs a master json mapping country names to a list of data in the order
# [population, vaccination rate, death rate, case rate]
def make_master_json(pop_json, vax_json, death_json, case_json, iso_json, master_json):
    # Convert all the json files to dictionaries
    pop_dict = json.load(pop_json)
    vax_dict = json.load(vax_json)
    death_dict = json.load(death_json)
    case_dict = json.load(case_json)
    iso_dict = json.load(iso_json)

    # Dictionary containing a map of ISO codes to a list of data
    master_dict = {}

    # First, add all population data
    for key in pop_dict:
        master_dict[iso_dict[key]] = [pop_dict[key]]

    # Now, add all vaccination data
    for key in vax_dict:
        # If this country was not in the population dictionary, skip over
        # population for now and add vaccination data, otherwise just
        # append vaccination datas
        if not iso_dict[key] in master_dict:
            master_dict[iso_dict[key]] = ['', vax_dict[key]]
        else:
            master_dict[iso_dict[key]].append(vax_dict[key])

    # Now add all death data
    for key in death_dict:
        if key in iso_dict:
            # If this country was not in population or vaccination dictionary, skip over
            # population and vaccination data for now and add death data, otherwise just 
            # append death data
            if not iso_dict[key] in master_dict:
                master_dict[iso_dict[key]] = ['', '', death_dict[key]]
            else:
                master_dict[iso_dict[key]].append(death_dict[key])
        else:
            print(key)

    # Now add all case data
    for key in case_dict:
        if key in iso_dict:
            # If this country was not in population, vaccination or death dictionary, skip over
            # population, vaccination, and death data for now and add case data, 
            # otherwise just append case data
            if not iso_dict[key] in master_dict:
                master_dict[iso_dict[key]] = ['', '', '', case_dict[key]]
            else:
                master_dict[iso_dict[key]].append(case_dict[key])
        else:
            print(key)

    # Now, make sure all values of master_dict are of length 4
    for key in master_dict:
        if len(master_dict[key]) < 4:
            if len(master_dict[key]) == 1:
                master_dict[key].append('')
                master_dict[key].append('')
                master_dict[key].append('')
            elif len(master_dict[key]) == 2:
                master_dict[key].append('')
                master_dict[key].append('')
            else:  
                master_dict[key].append('')

    # Now, make master json
    json.dump(master_dict, master_json)