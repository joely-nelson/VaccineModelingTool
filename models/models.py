# Author: Joely Nelson
# Made for Capstone for CSE 482B, Capstone Software Design to Empower
# Underserved Populations.
# This file includes some simple modeling functions.

import numpy as np
from scipy.integrate import odeint


def simulate(model, x0, t, k):
    '''
    Given a model, an initial values vector, a time vector, and a vector of
    parameters Will return the result of running this model.
    ARGS:
        - model: a function that takes in the following parameters:
                 - x (a vector containing current values of populations),
                 - t (a current time)
                 - k (a vector of the parameters)
                 must return a vector representing the dx at that time t
        - x0: a vector representing the initial values for x
        - t: a time vector to simulate for
        - k: the parameters needed by the model
    RETURNS:
        A vector where every element is a vector for x at a given time point.
        Will be len(t) long and len(x) wide.
    '''
    ret = odeint(lambda x, t: model(x, t, k), x0, t)
    return ret


def seird_model(x, t, k):
    '''
    The ODES for a simple SEIR model. Used for simulating before vaccination.
    ARGS:
        - x: a vector containing the current values for S(uceptible),
             E (exposed), I(infected), and R(ecovered) individuals
        - t: the current time
        - k: a vector with the parameter:
            - alpha: virus-induced fatality rate
            - beta: the contact rate
            - gamma: the recovery rate
            - eps: rate of progression from exposed to infected
    RETURNS:
        - dx/dt (otherwise known as: ds/dt, di/dt, dr/dt, dd/dt) for current t
    '''
    s, e, i, r, d = x
    n = x.sum()

    alpha, beta, eps, gamma = k

    ds = (-beta * s * i / n)
    de = (beta * s * i / n) - (eps * e)
    di = (eps * e) - (gamma * i) - (alpha * i)
    dr = (gamma * i)
    dd = (alpha * i)
    return ds, de, di, dr, dd


def seird_vac_model(x, t, k):
    '''
    The ODES for a simple SEIRD model with vaccination rates that represent
    the number of people vaccinated per day. Models ONLY after vaccination
    begins.
    ARGS:
        - x: a vector containing the current values for the individuals
            - s: suceptible
            - e: exposed
            - i: infected
            - r: recovered
            - d: dead
            subscript 1 means that they're unwilling/unable to be vaccinated
            subscript 2 means they are willing/able to be vaccianted
            subscript 3 means that they are vaccinated
            vector should be length 15: 
            x = s_1, e_1, i_1, r_1, d, s_2, e_2, i_2, r_2, d_2, s_3, e_3, i_3, r_3, d_3
        - t: the current time
        - k: a vector with the parameters in the following order:
            - alpha: virus-induced fatality rate
            - beta: the contact rate
            - gamma: the recovery rate
            - eps: rate of progression from exposed to infected
            - vac_rate: after vaccinations start, people are vaccinated at a rate
            - uptake_pop: population willing to be vaccinated.
            - vac_eff_i: the vaccine efficacy at preventing infection
            - vac_eff_d: the vaccine efficacy at preventing death
    RETURNS:
        - dx/dt for current time t
    '''
    (s_1, e_1, i_1, r_1, d_1,
     s_2, e_2, i_2, r_2, d_2, 
     s_3, e_3, i_3, r_3, d_3) = x
    # n is all (living) people
    n = x.sum()
    # infection rate depends on all infected people
    i = i_1 + i_2 + i_3
    
    alpha, beta, eps, gamma, vac_rate, vac_eff_i, vac_eff_d = k
    
    # Group 1 (Unwilling or unable to be vaccinated)
    # novax people people remain unchanged in their movements
    ds_1 = (-beta * s_1 * i / n)
    de_1 = (beta * s_1 * i / n) - (eps * e_1)    
    di_1 = (eps * e_1) - (gamma * i_1) - (alpha * i_1)
    dr_1 = (gamma * i_1)
    dd_1 = (alpha * i_1)
    
    # Group 2 (Willing and able to be vaccinated)
    # vax people move between i/e/r/d as before
    de_2 = (beta * s_2 * i / n) - (eps * e_2)    
    di_2 = (eps * e_2) - (gamma * i_2) - (alpha * i_2)
    dr_2 = (gamma * i_2)
    dd_2 = (alpha * i_2)
    
    # check if there are people left to vaccinate
    if s_2 - (beta * s_2 * i / n) - vac_rate < 0:
        # only vaccinate remaining people 
        # to avoid having negative people in a category
        new_vac_rate = max(0, s_2)
        ds_2 = (-beta * s_2 * i / n) - new_vac_rate
        ds_3 = new_vac_rate
    else:
        # normal, vaccinate at normal rate
        ds_2 = (-beta * s_2 * i / n) - vac_rate 
        ds_3 = vac_rate
        
    # Group 3 (Already vaccinated)
    # They are more protected, but not entirley protected, 
    # from infection and death
    ds_3 += (-beta * (1 - vac_eff_i) * s_3 * i / n)
    de_3 = (beta * (1 - vac_eff_i) * s_3 * i / n) - (eps * e_3) 
    di_3 = (eps * e_3) - (gamma * i_3) - (alpha * (1 - vac_eff_d) * i_3)
    dr_3 = (gamma * i_3)
    dd_3 = (alpha * (1 - vac_eff_d) * i_3)
    
    
    # return vector
    dx = (ds_1, de_1, di_1, dr_1, dd_1,
          ds_2, de_2, di_2, dr_2, dd_2,
          ds_3, de_3, di_3, dr_3, dd_3)

    return dx


def simulate_region(total_pop,
                    mortality,
                    reproduction_value,
                    avg_exposed_days,
                    avg_infected_days,
                    vac_start_day,
                    vac_rate,
                    uptake_per,
                    num_vac_days,
                    vac_eff_i,
                    vac_eff_d):
    '''
    Given some model parameters, returns a time series of the different
    populations Uses seird_vac_model for vaccination.
    ARGS:
        - total_pop: the total population of that region at the start
        - mortality: for every 1 person infected, this many people die.
        - reproduction_value: how many people on average one infected person infects
        - avg_exposed_days: number of days on average a person is in the exposed category
        - avg_infected_days: number of days on average a person is in the infected category
        - vac_rate: the rate at which vaccines occur
        - vac_start_day: the date that vaccinations begin
        - uptake_per: the % of the population willing to be vaccinated
        - num_vac_days: number of days to model after the vaccinations begin
        - vac_eff_i: the vaccine efficacy at preventing infection
        - vac_eff_d: the vaccine efficacy at preventing death
    RETURNS:
        Two vectors
        - first vector represents the time points. Call it t. It will start
          at 0 and increment by 1 until it reaches vac_start_day + num_vac_days
        - second vector represents the number of people in each of the time
          points. Call it v. v[i] corresponds to the number of suceptible,
          exposed, infected, recovered, dead, and vaccinatied individuals at
          the date t[i]. v[i] is another array of length 6.
              v[i][0]: number suceptible individuals
              v[i][1]: number exposed individuals
              v[i][2]: number infected individuals
              v[i][3]: number dead individuals
              v[i][4]: number recovered individuals
              v[i][5]: number vaccinated individuals
    '''
    # converting parameters given by user into alpha, beta, eps, gamma
    eps = 1 / avg_exposed_days
    gamma = 1 / avg_infected_days
    alpha = mortality * gamma
    beta = reproduction_value * gamma
    
    # Modeling initial pandemic:
    # Initial number of infected, recovered, suceptible indivduals
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
    # get initial values
    if len(v1 > 0):
        s, e, i, r, d = v1[-1]
    else:
        s, e, i, r, d = x0
    # s_1, e_1, i_1, r_1, s_2, e_2, i_2, r_2, d, v
    non_uptake = 1 - uptake_per
    x0 = [s*non_uptake, e*non_uptake, i*non_uptake, r*non_uptake, d*non_uptake,
          s*uptake_per, e*uptake_per, i*uptake_per, r*uptake_per, d*uptake_per,
          0, 0, 0, 0, 0
         ]
    
    # new paramaeters
    k = k + [vac_rate, vac_eff_i, vac_eff_d]
    t2 = np.linspace(0, num_vac_days, num_vac_days)
    # simulating
    v2 = simulate(seird_vac_model, x0, t2, k)
    (s_1, e_1, i_1, r_1, d_1,
     s_2, e_2, i_2, r_2, d_2, 
     s_3, e_3, i_3, r_3, d_3) = v2.T
    
    # add all species together to get desired SEIRDV only
    v2 = np.array([s_1 + s_2,        # S (non-vaccinated)
                   e_1 + e_2 + e_3,  # E (all exposed)
                   i_1 + i_2 + i_3,  # I (all infected)
                   r_1 + r_2 + r_3,  # R (all recovered)
                   d_1 + d_2 + d_3,  # D (all dead)
                   s_3 + e_3 + i_3 + r_3]).T  # V (all living and vaccinated)
    
    # combining pre vaccination sim and post vacc sim
    v1 = np.insert(v1, v1.shape[1], 0, axis=1)
    result = np.concatenate((v1, v2), axis=0)
    total_days = vac_start_day + num_vac_days
    ts = np.linspace(0, total_days, total_days)
    return ts, result


def simulate_world(param_dict, num_sim_days):
    '''
    Given a parameter dictionary matching the format of the master-json file,
    will simulate for each of the given countries using those parameters.
    Returns a dictionary where the keys are the countries and the values are 
    a the result of calling simulate region for that country.
    '''
    ret_dict = dict()
    for country, params in param_dict.items():
        try:
            # pull out parameters to pass to model
            # some must be divided by 100 to be a value in between 0-1 instead
            # of 0-100 to work with the model.
            vac_start_day = int(params['vac_start'])
            vac_rate = float(params['vac_rate'])
            avg_exposed_days = float(params['avg_days_in_exposed'])
            reproduction_value = float(params['r'])
            uptake_per = float(params['vac_uptake']) / 100
            avg_infected_days = float(params['avg_days_in_infected'])
            mortality = float(params['mortality']) / 100
            total_pop = int(params['population'])
            num_vac_days = int(num_sim_days) - vac_start_day
            vac_eff_i = float(params["vac_efficacy"]) / 100
            # currently hardcoded as 0, needs to be added to master json
            # if we want it to be another value
            vac_eff_d = 0

            # simulate
            t, v = simulate_region(total_pop, mortality, reproduction_value,
                                   avg_exposed_days, avg_infected_days,
                                   vac_start_day, vac_rate, uptake_per,
                                   num_vac_days, vac_eff_i, vac_eff_d)

            # add results to the ret dict
            ret_dict[country] = (list(t), [list(i) for i in v])
        except:
            continue

    return ret_dict
