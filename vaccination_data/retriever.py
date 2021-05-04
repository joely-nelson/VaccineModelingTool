#!/usr/bin/env python

# This module uses resources from the Our World in Data Project by Oxford University.
import requests
import sys
import time

# Web address for directory containing vaccination data.
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/"

# Every 24 hours, retieve data files from the server
while 1:
    # Retrieve each data file - vacinations, loations, manufacturers,
    # and vacinations by state
    vax = requests.get(url + "vaccinations.csv")
    if not vax:
        print("error: vaccinations.csv not found")
    vax_by_man = requests.get(url + "vaccinations-by-manufacturer.csv")
    if not vax_by_man:
        print("error: vaccinations-by-manufacturer.csv not found")
    locations = requests.get(url + "locations.csv")
    if not locations:
        print("error: locations.csv not found")
    us_state_vax = requests.get(url + "us_state_vaccinations.csv")
    if not us_state_vax:
        print("error: us-state-manufacturer.csv not found")
    



    # Open, write to, and then close each data file
    vax_file = open("vaccinations.csv", "w")
    vax_by_man_file = open("vaccinations-by-manufacturer.csv", "w")
    locations_file = open("locations.csv", "w")
    us_state_vax_file = open("us-state-vaccinations.csv", "w")

    vax_file.write(vax.text.encode("utf-8"))
    vax_by_man_file.write(vax_by_man.text.encode("utf-8"))
    locations_file.write(locations.text.encode("utf-8"))
    us_state_vax_file.write(us_state_vax.text.encode("utf-8"))

    vax_file.close()