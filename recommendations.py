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

def calculateSimilarItems(prefs, n=10):
    #create dict with si,ilar items for every item
    result = {}

    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        #renew for big datasets
        c+=1
        if c%100 == 0: print "%d / %d" % (c, len(itemPrefs))
        #find most similar items for current
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
        result[item] = scores

    return result

def getRecommendedItems(prefs,itemMatch,user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}

    #for items rated by user
    for (item,rating) in userRatings.items():
        #for items similar to current
        for (similarity, item2) in itemMatch[item]:
            #skip already rated
            if item2 in userRatings: continue
            #weighted sum of rates
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating

            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity

    rankings = [(score / totalSim[item], item) for item, score in scores.items() if totalSim[item] != 0]

    rankings.sort()
    rankings.reverse()
    return rankings

def loadMovieLens(path=u'ml-100k'):
    #get movies titles
    movies = {}
    for line in open(path+u'/u.item'):
        (id, title) = line.split('|')[:2]
        movies[id] = title

    #load data
    prefs = {}
    for line in open(path+u'/u.data'):
        (user, movie_id, rating, ts) = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movies[movie_id]] = float(rating)
    return prefs

def prepare_for_tanimoto(prefs):
    result = {}
    for person in prefs:
        result.setdefault(person,{})
        for item in prefs[person]:
            result[person][item] = (0,1)[prefs[person][item] > 3]

    return result
    
def sim_tanimoto(prefs, p1, p2, prepare = False):
    if prepare: prefs = prepare_for_tanimoto(prefs)
    
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2] and prefs[p2][item] == prefs[p1][item]:
           si[item] = 1
    
    c = len(si)
    
    if c == 0: return 0
    
    return float(c) / (len(prefs[p1]) + len(prefs[p2]) - c)
    
    