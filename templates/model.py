from pymongo import MongoClient


client=MongoClient()
db=client['mini_amazon']
def check_user(username);
	
	query = {"username":username}
	results= db{'users'}.find(query)
	print(results)
	if result.count()>0
		return True
	return False
def create_user(user_info);
	db['users'].insert_one(user_info)