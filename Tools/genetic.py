import numpy as np

# liczby losowe
import random

import time

# odleglość euklidesowa między miastami pośrednimi i oraz j
def dist(i,j):
    return np.sqrt((cities[i,0]-cities[j,0])**2 
                   + (cities[i,1]-cities[j,1])**2)

# odległość miasta i od miasta startowego
def dist_s(i):
    return np.sqrt((cities[i,0]-start[0])**2 + 
                   (cities[i,1]-start[1])**2)


def len_path(path):
    return dtab_s[path[0]]+sum(dtab[path[i],path[i+1]] 
                               for i in range(n-2))+dtab_s[path[n-2]]


# losowy chromosom/osobnik jako losowa permutacja (ciąg miast pośrednich)
def person():
    return np.random.permutation(n-1)  


def swap(list, p1, p2): 
    list[p1], list[p2] = list[p2], list[p1] 
    return list


# selekcja liczby n_best najlepszych osobników z populacji popu

def select(popu,n_best): # populacja, liczba pozostawionych najlepszych osobników
    
    le=len(popu) # liczebność populacji
    popu_len=np.array([len_path(pers) for pers in popu]) # znalezienie długości dróg 
    
    com=np.array([[popu[i], popu_len[i]] for i in range(len(popu_len))],dtype=object)
                               # tablica z dołączonymi długościami dróg
        
    popu_c=sorted(com, key=lambda x: x[1]) # sortowanie wg długości drogi
    
    p_c=[x[0] for x in popu_c] # posortowana tablica dróg bez długości
    
    # tworzenie nowej populacji
    sel=np.array([p_c[0]])     # dodanie najkrótszej drogi do nowej populacji sel
    k=1 # aktualna liczba dróg w populacji sel
    
    for i in range(1,le): # pętla po osobnikach
                          # osobnik [0] już dodany, zaczynamy od [1]
        
        if not np.array_equal(p_c[i],sel[-1]): # dodaj tylko innego osobnika
            k=k+1 # aktualna liczba dróg w populacji sel
            sel=np.append(sel,p_c[i]) # dodanie osobnika do nowej populacji sel
            
        sel=np.reshape(sel,[k,n-1]) # przeformatowanie tablicy zob. poniżej
        if k==n_best: # skończ, jeśli masz już n_best osobników
            break
    return sel    # nowa populacja


def breed(papa, mama):
    cut=random.randint(1,n-2)   
    chp=np.delete(papa, np.arange(cut, n-1, 1))
    chm=np.delete(mama, np.arange(0,cut, 1))
    if random.random() > 0.5:
        chm=np.flip(chm)
    child=np.concatenate((chp,chm),axis=0)
    repeated=np.intersect1d(chp,chm)
    missed=np.setdiff1d(papa, child)
    random.shuffle(missed)
    for i in range(len(repeated)):
        icor=np.where(child==repeated[i])[0]
        child[random.choice(icor)]=missed[i]
        
    for _ in range(nummut):
        if random.random()<mut:
            swap(child, random.randint(0,n-2),random.randint(0,n-2))
    return child


def generation():

    children=np.array([breed(popul[random.randint(0,npop-1)],\
                             popul[random.randint(0,npop-1)]) for _ in range(nchil)]) 
                              # spłodzenie dzieci
    
    al=np.concatenate((popul,children)) # dodanie dzieci do populacji rodziców
    
    return select(al,npop)  # selekcja npop najlepszych osobników z połączonej populacji


def genetic_algorythm(start_, cities_, POPULATION=3, CHILDREN=3, MUTATION=0.6, N_MUTATION=15):

    # Pure laziness
    global start
    global cities
    global n
    global npop
    global nchil
    global mut
    global nummut
    global popul
    global dtab
    global dtab_s
    
    n=len(cities_)+1 # liczba wszystkich miast
    start=start_
    cities=cities_
    
    # *************************
    npop = POPULATION * n       # liczba osobników w populacji
    nchil = CHILDREN * npop     # liczba dzieci
    mut = MUTATION              # prawdopodobieństwo mutacji
    nummut = n // N_MUTATION    # liczba mutacji
    # *************************
    
    startt = time.time()

    # losowa populacja początkowa
    popul=np.array([person() for _ in range(npop)])


    # można zrobić kilka iteracji tej komórki
    dtab=np.array([[dist(i,j) for i in range(n-1)] for j in range(n-1)]) # ...pośrednimi
    dtab_s=np.array([dist_s(i) for i in range(n-1)]) # ...od miasta startowego

    for _ in range(500):

        popul=generation()

    #print('zakres długości: ',len_path(popul[0]),' - ',len_path(popul[npop-1]))
    #print(np.array([len_path(pers) for pers in popul]))

    tmin=popul[0]
    # print(tmin)

    tourmin=np.array([cities[i] for i in tmin])
    tourmin=np.reshape(np.append(np.insert(tourmin,0,start),start),[n+1,2])
    # print(tourmin)
    
    endd = time.time()
    exec_time = endd - startt
    
    return tourmin, len_path(popul[0]), exec_time