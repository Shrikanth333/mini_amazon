from flask import Flask,render_template,request,redirect,url_for,session,flash
from model import check_user,create_user,log_user,check_product,create_product,get_products,seller_products,update_cart,cart_page,remove_cart,remove1


app = Flask(__name__)

app.config['SECRET_KEY']='hello'

@app.route("/")

def home():
	if session.get('username'):
		return render_template('home.html',user = session['username'])
	else:
		return render_template('home.html')

@app.route('/welcome')
def welcome():

	return render_template('welcome.html')


@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=='POST':
		
		username=request.form['username']
		password=request.form['password']	
		result=log_user(username)
		
		if password==result['password']:
			
			session['username']=result['username']
			session['c_type']=result['c_type']
		
		
			return render_template('welcome.html')
		flash('password does not match')
		return render_template('home.html')
		
	return render_template('home.html')

@app.route('/signup',methods=['GET','POST'])
def signup():

	if request.method=='POST':
		user_info={}
		user_info['username']=request.form['username']
		user_info['emailid']=request.form['emailid']
		user_info['password']=request.form['password']
		rpassword=request.form['rpassword']
		user_info['c_type']=request.form['type']
		if user_info['c_type']=='buyer':
			user_info['cart']=[]

		if check_user(user_info['username']) is False:
			if rpassword==user_info['password']:
			 	create_user(user_info)
			else:
				flash('password does not match')
				return render_template('shrikanth.html')

		else:
			flash('user already exists')
			return render_template('shrikanth.html')

	return redirect(url_for('home'))
@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for("home"))
@app.route('/register')
def register():
	return render_template('shrikanth.html')


@app.route('/add_products',methods=['GET','POST'])
def add_products():
	if request.method=='POST':
		product_info={}
		product_info['name']=request.form['name']
		product_info['description']=request.form['description']
		product_info['price']=int(request.form['price'])
		product_info['seller_name']=session['username']

		if check_product(product_info['name']):
			return "product already exists"

		create_product(product_info)
		return(redirect(url_for('welcome')))


	return render_template('add_products.html')

@app.route("/productslist")
def getprod():
	products = get_products()
	return render_template("products.html", products=products)

@app.route("/yourproduct")
def yourproduct():
	prods=seller_products(session['username'])
	return render_template("products.html", prods=prods)
	
@app.route('/add_cart', methods=['POST'])
def add_cart():
	product_id=request.form['product_id']
	update_cart(session['username'],product_id)
	return(redirect(url_for('welcome')))

@app.route('/remove_cart', methods=['POST'])
def rem_cart():
	product_id=request.form['product_id']
	remove_cart(session['username'],product_id)
	return(redirect(url_for('welcome')))

@app.route('/remove_item', methods=['POST'])
def remov():
	prod_id=request.form['prod_id']
	remove1(session['username'],prod_id)
	return(redirect(url_for('welcome')))




@app.route('/cart')
def cart():
	#import pdb;pdb.set_trace()
	products=cart_page(session['username'])
	return render_template("cart_page.html", products=products)
	


app.run(debug=True)