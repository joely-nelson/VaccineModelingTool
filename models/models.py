# models.py
# by Joely Nelson
# made for Capstone for CSE 482B, Capstone Software Design to Empower Underserved Populations 
# This file includes some simple modeling functions.

import numpy as np
from scipy.integrate import odeint
import csv
import json

def simulate(model, x0, t, k):
    '''
    Given a model, an initial values vector, a time vector, and a vector of parameters
    Will return the result of running this model.
    Note that it will be returned as a vector where every element is another vector for
    a given time point. Each vector for a given time point will include the values
    for each category at that time.
    '''
    ret = odeint(lambda x, t: model(x, t, k), x0, t)
    return ret


def seird_vac_model3(x, t, k):
    '''
    The ODES for a simple SEIRD model with vaccination rates that represent
    the number of people vaccinated per day. Models ONLY after vaccination
    begins.
    ARGS:
        - x: a vector containing the current values for S(uceptible),
          I(infected), and R(ecovered) individuals
        - t: the current time
        - k: a vector with the parameter:
            - alpha: virus-induced fatality rate
            - beta: the contact rate
            - gamma: the recovery rate
            - eps: rate of progression from exposed to infected
            - vac_rate: after vaccinations start, people are vaccinated at a rate
            - uptake_pop: population willing to be vaccinated.
    RETURNS:
        - dx/dt (so ds/dt, di/dt, dr/dt, dd/dt)
    NOTES:
        Best value for k is:
        [0.005, 0.28037216445437113, 0.2, 0.2]
    '''
    s, e, i, r, d, v = x
    n = x.sum()
    
    alpha, beta, gamma, eps, vac_rate, uptake_pop = k
    
    
    de = (beta * s * i / n) - (eps * e)
    di = (eps * e) - (gamma * i) - (alpha * i)
    dr = (gamma * i)
    dd = (alpha * i)
    
    # only vaccinate people if there are people to vaccinate
    # TODO: Change how uptake_pop is modeled
    if v >= uptake_pop or v >= s:
        # no one to vaccinate
        ds = (-beta * s * i / n) 
        dv = 0
    elif v + vac_rate > uptake_pop or v + vac_rate >= s:
        new_vac_rate1 = uptake_pop - v
        new_vac_rate2 = s - v
        new_vac_rate = min(new_vac_rate1, new_vac_rate2)
        ds = (-beta * s * i / n) - new_vac_rate
        dv = new_vac_rate
    else:
        # normal, vaccinate at normal rate
        ds = (-beta * s * i / n) - vac_rate 
        dv = vac_rate

    return ds, de, di, dr, dd, dv


def seird_model(x, t, k):
    '''
    The ODES for a simple SIR model.
    ARGS:
        - x: a vector containing the current values for S(uceptible),
          I(infected), and R(ecovered) individuals
        - t: the current time
        - k: a vector with the parameter:
            - alpha: virus-induced fatality rate
            - beta: the contact rate
            - gamma: the recovery rate
            - eps: rate of progression from exposed to infected
    RETURNS:
        - dx/dt (so ds/dt, di/dt, dr/dt, dd/dt)
    NOTES:
        Best value for k is:
        [0.005, 0.28037216445437113, 0.2, 0.2]
    '''
    s, e, i, r, d = x
    n = x.sum()
    
    alpha, beta, gamma, eps = k
    
    ds = (-beta * s * i / n)
    de = (beta * s * i / n) - (eps * e)
    di = (eps * e) - (gamma * i) - (alpha * i)
    dr = (gamma * i)
    dd = (alpha * i)
    return ds, de, di, dr, dd


def simulate_region(total_pop, alpha, beta, eps, gamma, 
                    vac_start_day, vac_rate, uptake_per, num_vac_days):
    '''
    Given some model parameters, returns a time series of the different populations
    ARGS:
        - total_pop: the total population of that region at the start
        - alpha: % chance that an infected person will die while they are infected
        - beta: contact rate
        - eps: rate at which someone goes from infected to recovered
        - gamma: rate at which someone goes from exposed to recovered
        - vac_rate: the rate at which vaccines occur
        - vac_start_day: the date that vaccinations begin
        - uptake_per: the % of the population willing to be vaccinated
        - num_vac_days: number of days to model after the vaccinations begin
    RETURNS:
        Two vectors
        - first vector represents the time points. Call it t. It will start 
          at 0 and increment by 1 until it reaches vac_start_day + num_vac_days
        - second vector represents the number of people in each of the time points. 
          Call it v. v[i] corresponds to the number of suceptible, exposed, infected,
          recovered, dead, and vaccinatied individuals at the date t[i]. v[i] is another
          array of length 6.
              v[i][0]: number suceptible individuals
              v[i][1]: number exposed individuals
              v[i][2]: number infected individuals
              v[i][3]: number dead individuals
              v[i][4]: number recovered individuals
              v[i][5]: number vaccinated individuals
    '''
    # Modeling initial pandemic:
    # Initial number of infected, recovered, suceptible indivduals
    # Hardcoded in for now
    i0 = 0
    e0 = 50
    r0 = 0
    d0 = 0
    s0 = total_pop - i0 - e0 - r0 - d0
    x0 = (s0, e0, i0, r0, d0)
    # parameters
    k = [alpha, beta, eps, gamma]
    t1 = np.linspace(0, vac_start_day, vac_start_day)
    # simulating
    v1 = simulate(seird_model, x0, t1, k)
    
    # Model after vaccines are introduced
    x0 = list(v1[-1]) + [0]
    # new paramaeters
    k = k + [vac_rate, uptake_per*total_pop]
    t2 = np.linspace(0, num_vac_days, num_vac_days)
    # simulating
    v2 = simulate(seird_vac_model3, x0, t2, k)
    
    # combining pre vaccination sim and post vacc sim
    v1 = np.insert(v1, v1.shape[1], 0, axis = 1)
    result = np.concatenate((v1, v2), axis=0)
    ts = np.linspace(0, vac_start_day + num_vac_days, vac_start_day + num_vac_days)
    return ts, result


def simulate_world(alpha, beta, gamma, eps, vac_start_day, uptake_per, num_vac_days, vac_rate):
    '''
    Simulates the entire world given parameters from files.
    ARGS:
        default parameters to be fed into model
    RETURNS:
        None. Writes a json file into the json_io_files directory named
        model_output.json. This file represents a dictionary where the keys
        are the countries and the values are a the result of calling simulate
        region for that country.
    OTHER NOTES:
        When fit to USA, best alpha, beta, gamma, eps is:
            alpha = 0.005
            beta = 0.27
            gamma = 0.2
            eps = 0.2    
    '''
    ret_dict = dict()
    
    # loop through population file to get population for each country
    with open('./vaccination_data/population-figures-by-country-csv-parsed.csv') as csv_file:
        csv_dict = csv.DictReader(csv_file)
        for row in csv_dict:
            # get country and population for country. Ignore if data missing.
            country = row['Country']
            if row['Year_2016'] != '':
                total_pop = int(row['Year_2016'])

                # simulate
                t, v = simulate_region(total_pop, alpha, beta, eps, gamma, 
                            vac_start_day, vac_rate, uptake_per, num_vac_days)

                # add results to the ret dict
                ret_dict[country] = (list(t), [list(i) for i in v])
                
    with open("./json_io_files/model_output.json", "w") as write_file:
        json.dump(ret_dict, write_file)
