from pydelicious import get_popular, get_userposts, get_urlposts, getrss

def initializeUserDict(tag, count=5):
    user_dict={}
    #get count most popular links
    for p1 in get_popular(tag=tag)[0:count]:
	#find all users saved this link
	for p2 in get_urlposts(p1['url']):
	    user = p2['user']
	    user_dict[user] = {}

    return user_dict

def fillItems(user_dict):
    all_items = {}
    #find links saved by all users
    for user in user_dict:
	for i in range(3):
	    try:
		posts = get_userposts(user)
		break
	    except:
		print u'Error for user '+user+u', trying one more time'
		time.sleep(4)
	for post in posts:
	    url = post['url']
	    user_dict[user][url] = 1.0
	    all_items[url] = 1

    #instead of empty elements write 0
    for ratings in user_dict.values():
	for item in all_items:
	    if item not in ratings:
		ratings[item] = 0.0

def getTags():
    user_dict = initializeUserDict('curious')
    all_items = {}
    tags_dict = {}
    #find links saved by all users
    for user in user_dict:
	for i in range(3):
	    try:
		posts = get_userposts(user)
		break
	    except:
		print u'Error for user '+user+u', trying one more time'
		time.sleep(4)
	for post in posts:
	    url = post['url']
	    tag = post['tags']
	    tags_dict.setdefault(tag,{})
	    tags_dict[tag][url] = 1.0
	    all_items[url] = 1

    #instead of empty elements write 0
    for ratings in tags_dict.values():
	for item in all_items:
	    if item not in ratings:
		ratings[item] = 0.0
    return tags_dict