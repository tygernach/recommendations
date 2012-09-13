from math import sqrt

critics = {'first':{'Mappets':4.5,'Superman':2.0, 'Lady in the water':4.5,'Titanic':5.0},
            'second':{'Mappets':4.5,'Superman':3.0,'Lady in the water':3.6},
            'third':{'Mappets':3.3,'Superman':4.7,'Alone in the dark':5.0},
            'forth':{'Superman':3.8,'Titanic':3.1,'Alone in the dark':4.7}}

def sim_distance(prefs, person1, person2):
    #Euclidian distance
    si = {}
    for item in prefs[person1]:
        for item in prefs[person2]:
           si[item] = 1
    
    if len(si) == 0: return 0
    total_sum = sum([pow(prefs[person1][item] - prefs[person2][item],2) for item in prefs[person1] if item in prefs[person2]])
    return 1 / (1 + sqrt(total_sum))
    
def sim_pearson(prefs, p1, p2):
    #Pearson distance
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item] = 1
        
    n = len(si)
    
    #no mutual rates
    if n == 0: return 0
    
    #sum of all rates
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    
    #sum of squares
    sum1sq = sum([pow(prefs[p1][it],2) for it in si])
    sum2sq = sum([pow(prefs[p2][it],2) for it in si])
    
    #sum of products
    psum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
    
    #here there be Pearson
    num = psum - (sum1*sum2/n)
    den = sqrt((sum1sq-pow(sum1,2)/n)*(sum2sq-pow(sum2,2)/n))
    if den == 0: return 0
    
    return num/den