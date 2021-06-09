#!/usr/bin/env python

# This module contains all the functions for parsing obtained data files
import requests
import sys
import time
import csv
import json

def population_parser(unparsed, parsed):
    """
    Takes an unparsed file of population data and creates a parsed file containing only
    the most recent population data for each country. 

    PRE: 
        Correct file is used for unparsed (see ARGS)

    ARGS:
        - unparsed: an opened csv file containing unparsed population data obtained from
          the JohnSnowLabs project
        - parsed: a csv file into which only the most recent population data will
          be put, with the following fields for each column:
            - column 0: country name
            - column 1: ISO code (uniform three-letter code for each country)
            - column 2: Most recent population data
    """

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

def vax_parser(unparsed, parsed):
    """
    Takes an unparsed file of vaccination data and creates a parsed file containing only
    the daily average of vaccinations over the last 7 days for each country

    PRE: 
        Correct file is used for unparsed (see ARGS)

    ARGS:
        - unparsed: an opened csv file containing unparsed vaccination data obtained from
          the OWID COVID data project, specifically the file vaccinations
        - parsed: an opened csv file into which only the daily average of vaccinations
          will be put, with the following fields for each column
            - column 0: country name
            - column 1: ISO code (uniform three-letter code for each country)
            - column 2: daily average of vaccinations over the last 7 days
    """
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
    
def cases_deaths_parser(unparsed, parsed_deaths, parsed_cases):
    """
    Takes an unparsed data file containing COVID-19 death rates and case rates on a 
    country-by-country basis and puts in a parsed file only the most recent weekly 
    data for each country.

    PRE: 
        Correct file is used for unparsed (see ARGS)


    ARGS:
        - unparsed: an opened csv file containing unparsed vaccination data obtained from
          the OWID COVID data project's JHU data, specifically the file full_data
        - parsed_deaths: an opened csv file into which only the most recent weekly death data
          will be put, with th columns as follows:
            - column 0: country name
            - column 1: most recently weekly deaths
        - parsed_cases : an opened csv file into which only the most recent weekly case data
          will be put, with th columns as follows:
            - column 0: country name
            - column 1: most recently weekly deaths
    """
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

def r_value_parser(unparsed, parsed):
    """
    Takes an unparsed data file containing the latest COVID-19 data and puts into
    a single csv file only the most recent COVID-19 reproduction numbers for countries
    that have them.

    PRE: 
        Correct file is used for unparsed (see ARGS)

    ARGS:
        - unparsed: an opened csv file containing unparsed COVID-19 data obtained from
          the OWID COVID data project, specifically the file owid-covid-latest
        - parsed: an opened csv file into which only the daily average of vaccinations
          will be put, with the following fields for each column
            - column 0: ISO code (uniform three-letter code for each country)
            - column 1: country name
            - column 2: r-value for said country
    """

    r_writer = csv.writer(parsed)
    # Go through each row in unparsed file
    for row in csv.reader(unparsed):
        # Write the country name, iso code, and r-value
        r_writer.writerow((row[0], row[2], row[16]))