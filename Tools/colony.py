import time
import random

import numpy as np

from itertools import accumulate


def len_path(path):
    return sum([dist(path[i],path[i+1]) for i in range(len(path)-1)])


def dist(i,j):
    return np.sqrt((cities[i,0]-cities[j,0])**2 + (cities[i,1]-cities[j,1])**2)


def ind_prob(tab_p):
    cum_p=np.array(list(accumulate(tab_p)))
    return np.sum(np.heaviside(random.random()-cum_p,0)).astype(int)


def ac_next(i, togo):
    p =np.array([fero[i, j]**alpha/dis_tab[i, j]**beta for j in togo])
    su=np.sum(p)
    p=p/su
    return togo[ind_prob(p)]


def ac_one(pop, sc): 
    lm=10**10
    global fero2
    fero2=np.array([[0. for _ in range(n)] for _ in range(n)])
    for _ in range(pop):
        pos=random.randint(0,n-1)
        route=[pos]
        to_v=[i for i in range(0,pos)]+[i for i in range(pos+1,n)]
        for _ in range(n-1):
            pos=ac_next(pos,to_v)
            route.append(pos)
            to_v.remove(pos)
        route.append(route[0])        
        lr=len_path(route)
        if lr<lm:
            lm=lr
            r_opt=route
    for i in range(n):
        fero2[r_opt[i],r_opt[i+1]]=fero2[r_opt[i],r_opt[i+1]]+sc/lm
        fero2[r_opt[i+1],r_opt[i]]=fero2[r_opt[i+1],r_opt[i]]+sc/lm
    return lm, r_opt


def ant_colony(cities_, iter_=3000, alpha_=1.1, beta_=1.1, h_=0.005, popsize_=15):

    # Pure laziness
    global cities
    global n
    global dis_tab
    global alpha
    global beta
    global fero
    global ite
    global h
    global popsize
    n = len(cities_)
    h = h_
    popsize = popsize_
    ite = iter_
    cities = cities_
    sc = n/popsize_
    alpha = alpha_
    beta = beta_

    start = time.time()

    dis_tab=np.array([[dist(i,j) for i in range(n)] for j in range(n)])
    min_l=10**10
    fero=np.array([[1. for _ in range(n)] for _ in range(n)])-np.identity(n) 
    for k in range(ite):
        opt=ac_one(popsize, sc)
        if opt[0]<min_l:
            min_l=opt[0]
            best_route=opt[1]
        fero=(1-h)*fero+h*fero2

    end = time.time()
    exec_time = end - start

    return best_route, min_l, exec_time, np.round(fero,2)























































