from pymongo import MongoClient
from bson.objectid import ObjectId


client=MongoClient()
db=client['mini_amazon']
def check_user(username):
	
	query = {"username":username}
	results= db['users'].find(query)
	print(results)
	if results.count()>0:
		return True
	return False

def create_user(user_info):
	db['users'].insert_one(user_info)

def log_user(username):
	query={"username":username}
	results= db['users'].find_one(query)
	print(results)
	return results

def check_product(name):
	query = {"name":name}
	results= db['products'].find(query)

	if results.count()>0:
		return True
	return False


def create_product(a):
	db['products'].insert_one(a)

def get_products():
	return db['products'].find({})

def seller_products(d):
	query= {"seller_name":d}
	results= db['products'].find(query)
	return results


def update_cart(username,product_id):
	db['users'].update({"username":username},{"$addToSet":{"cart":{"$each":[product_id]}}})

def remove_cart(username,product_id):
	db['users'].update({"username":username},{"$pull":{"cart":{"$in":[product_id]}}})


def remove1(username,prod_id):
	 db['products'].remove({"yourproduct":{"_id":[prod_id]}},1)
	# db.products.remove({"_id":prod_id})

def cart_page(username):
	query= {"username":username}
	results= db['users'].find_one(query)
	products_ids=results['cart']

	products=[]

	for product_id in products_ids:
		query={"_id":ObjectId(product_id)}
		results=db['products'].find_one(query)
		products.append(results)
	return products