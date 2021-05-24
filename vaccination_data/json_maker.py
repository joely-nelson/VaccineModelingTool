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

    # Now convert the dictionary to a json_file
    json.dump(iso_dict, iso_json)

# Outputs a master json mapping country names to a list of data in the order
# [population, vaccination rate, death rate, hospitalization rate]
# def make_master_json(pop_json, vax_json, deaths_json, hosp_json, master_json):