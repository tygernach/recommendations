from math import sqrt

critics = {'first':{'Mappets':4.5,'Superman':2.0, 'Lady in the water':4.5,'Titanic':5.0},
            'second':{'Mappets':1.5,'Superman':4.0,'Lady in the water':2.6},
            'third':{'Mappets':3.3,'Superman':4.7,'Alone in the dark':5.0},
            'forth':{'Superman':3.8,'Titanic':3.1,'Alone in the dark':4.7}}

def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        for item in prefs[person2]:
           si[item] = 1
    
    if len(si) == 0: return 0
    total_sum = sum([pow(prefs[person1][item] - prefs[person2][item],2) for item in prefs[person1] if item in prefs[person2]])
    return 1 / (1 + sqrt(total_sum))