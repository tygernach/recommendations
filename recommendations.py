from math import sqrt

critics = {'first':{'Mappets':4.5,'Superman':2.0, 'Lady in the water':4.5,'Titanic':5.0},
            'second':{'Mappets':4.0,'Superman':3.0,'Lady in the water':3.6},
            'third':{'Mappets':3.3,'Superman':4.7,'Alone in the dark':5.0},
            'forth':{'Superman':3.8,'Titanic':3.1,'Alone in the dark':4.7},
            'stranger':{'Mappets':3.8,'Star Wars':3.1,'Looney Tunes':4.7},
            'tyger':{'Superman':4.8,'Titanic':3.0,'Alone in the dark':5.0}}

def sim_distance(prefs, person1, person2):
    #Euclidian distance
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
           si[item] = 1
           break

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

#top person matches for person
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs,person,other),other) for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[:n]

#get recommendations for person
def getRecommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simSum = {}
    for other in prefs:
        #no reason to compare me with myself
        if other == person: continue
        sim = similarity(prefs, person, other)

        #ignore nulls and negatives
        if sim <= 0: continue
    for item in prefs[other]:
        #rate only unwatched movies
        if item not in prefs[person] or prefs[person][item] == 0:
            #similarity rate * movie rate
            totals.setdefault(item,0)
            totals[item] += prefs[other][item]*sim
            #sim rates sum
            simSum.setdefault(item,0)
            simSum[item] += sim
    #normalize list
    rankings = [(total/simSum[item], item) for item, total in totals.items() if simSum[item] != 0]

    #sort list
    rankings.sort()
    rankings.reverse()
    return rankings

#revert persons and items
def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            result[item][person] = prefs[person][item]
    return result
    