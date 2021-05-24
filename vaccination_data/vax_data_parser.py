#!/usr/bin/env python

# This module contains all the functions for parsing obtained data files
import requests
import sys
import time
import csv
import json

# Takes arguments unparsed population file, removes all non-recent 
# population data, and outputs a parsed file.
def population_parser(unparsed, parsed):
    parsed_writer = csv.writer(parsed)
    # Go through each row in unparsed file
    for row in csv.reader(unparsed):
        # If the row is not blank, write only the country name, ISO code,
        # and most recent population data to the parsed file.
        if any(field.strip() for field in row):
            # Eritrea does not have most recent data, so we have to go back a bit
            if row[1] == "ERI":
                parsed_writer.writerow((row[0], row[1], row[53]))
            elif row[0] == "Country":
                parsed_writer.writerow((row[0], row[1], "population"))
            else: 
                parsed_writer.writerow((row[0], row[1], row[58]))

# Takes most recent weekly and daily averages for countries and puts them into a
# a parsed data file.  Note that the data must be sorted by country and then
# sorted by date with the least recent dates occuring first in the csv file in order
# for this parser to work.
def vax_parser(unparsed, parsed):
    parsed_writer = csv.writer(parsed)
    # Dictionary that keeps track of how many times we've seen each country
    country_entries = {}
    # Keeps track of vaccinations over the last 7 days for each country.
    vax_7_day = {}
    # List of lines in csv file
    csv_lines = list(csv.reader(unparsed))

    # Goes through each country in reverse order, takes a 7 day average of 
    # vaccination numbers for the previous seven days.
    for row in reversed(csv_lines):
        # Don't want to parse header row
        if row[0] != "location" and row[7] != "":
            # If we haven't seen this country yet, note that now we have and record
            # the number of vaccinations for the most recent day.
            if not row[1] in country_entries:
                country_entries[row[1]] = 1
                vax_7_day[row[1]] = int(row[7])
            # If we've seen this country less than 7 times, increment the number of times
            # we've seen it, and add the vaccinations for the current day.
            elif country_entries[row[1]] < 7:
                country_entries[row[1]] += 1
                vax_7_day[row[1]] += int(row[7])

    # Now, go through each country in order, and write the totals for each country
    for row in csv_lines:
        # First row has to be different
        if row[0] == "location":
            parsed_writer.writerow((row[0], row[1], "weekly_vaccinations"))
        # If the country has no data, then write the line blank
        elif not row[1] in country_entries:
            parsed_writer.writerow((row[0], row[1], ""))
            # Set row to 8 so that it isn't written again
            country_entries[row[1]] = 8
        # Besides that, write the 7-day average the first time that country is seen
        elif country_entries[row[1]] <= 7:
            parsed_writer.writerow((row[0], row[1], 
                vax_7_day[row[1]] / country_entries[row[1]]))
            country_entries[row[1]] = 8

# Takes an unparsed data file containing COVID-19 death rates on a country-by-country
# basis and outputs a parsed file with only the most recent weekly data for each country    
def cases_deaths_parser(unparsed, parsed_deaths, parsed_cases):
    deaths_writer = csv.writer(parsed_deaths)
    cases_writer = csv.writer(parsed_cases)
    # Dictionary that keeps track of most recent weekly deaths
    recent_deaths = {}
    # Dictionary that keeps track of most recent weekly cases
    recent_cases = {}
    # List of lines in csv file
    csv_lines = list(csv.reader(unparsed))

    # Goes through all the countries in reverse order to get the most recent
    # weekly deaths
    for row in reversed(csv_lines):
        if (row[1] != "location") and (not row[1] in recent_deaths):
            recent_deaths[row[1]] = row[7]
            recent_cases[row[1]] = row[6]

    # Keeps track of countries already written
    countries_seen = set()

    # Write all countries to csv file
    for row in csv_lines:
        if row[1] == "location":
            deaths_writer.writerow((row[1], row[7]))
            cases_writer.writerow((row[1], row[6]))
        elif not row[1] in countries_seen:
            deaths_writer.writerow((row[1], recent_deaths[row[1]]))
            cases_writer.writerow((row[1], recent_cases[row[1]]))
            countries_seen.add(row[1])