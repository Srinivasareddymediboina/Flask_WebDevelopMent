from flask import Flask,redirect,url_for
from flask import render_template,request
import os #perform operation on file using path
# Create Instance for Flask App

# importing required classes from 'db_create' 
from db_create import User, Item,Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from flask import session as login_session
from functools import wraps

#create session Instance for perform operations in 
#                            database file
engine= create_engine("sqlite:///mydb.db")
Base.metadata.bind=engine
session=scoped_session(sessionmaker(bind=engine))

app=Flask(__name__)
"""
def login_required(f):
	@wraps(f)
	def x(*args,**kwargs):
		if 'email' not in login_session:
			return redirect(url_for('login'))
		return f(*args,**kwargs)
	return x"""

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'email' in login_session:
            return f(*args, **kwargs)
        else:
            #flash("You need to login first")
            return redirect(url_for('login_page'))

    return wrap

# HINT--> SHOULD BE FOLLOW Python INTENDATION
# Hint--> url build should be starts with '/'
@app.route("/")
def home():
	return render_template("home.html")

# Create Url for 'Registration' Page 
#                    using Python Decorator '@'
@app.route('/register',methods=["GET","POST"])
def register():
	if request.method=="POST":
		name= request.form["name"]
		email= request.form["email"]
		password= request.form["password"]
		image= request.files["file"]
		path=os.getcwd()+"\\static\\images\\"
		image.save(path+image.filename)
		new_user=User(name=name,
			email=email,
			password=password,
			image=(path+image.filename))
		session.add(new_user)
		session.commit()
		#return "Successfully Registered..."
		return render_template("regsuccess.html")
	else:
		return render_template("register.html")


@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=="POST":
		email=request.form['email']
		password=request.form['password']
		owner=session.query(User).filter_by(email=email,
			password=password).one_or_none()
		if owner==None:
			#flash("Invalid Credentials....!",'danger')
			return redirect(url_for('login'))
		login_session['email']=email
		login_session['name']=owner.name
		#flash('Welcome'+str(owner.name),'success')
		return redirect(url_for('items'))
	return render_template('login.html')

# Create Url for "newitem.html"
@app.route('/newitem', methods=["GET","POST"])
@login_required
def newitem():
	if request.method=="POST":
		brand=request.form['brand']
		model=request.form['model']
		image=request.form['image']
		cost=request.form['cost']
		description=request.form['description']
		user_id=1
		new_item=Item(brand=brand,model=model,
			url=image,cost=cost,
			description=description,
			user_id=user_id)
		session.add(new_item)
		session.commit()
		return render_template('newitemsuccess.html')
		#return "Item Successfully Saved"
	else:
		return render_template("newitem.html")

@app.route("/items")
@login_required
def items():
	items=session.query(Item).all()
	return render_template("items.html",items=items)

@app.route('/Item/<int:item_id>/delete')
def deleteitem(item_id):
	item=session.query(Item).filter_by(id=item_id).one_or_none()
	session.delete(item)
	session.commit()
	return "Successfully Deleted.."
	#return redirect(url_for('home'))
		
@app.route('/Item/<int:item_id>/edit', methods=["GET","POST"])
def edititem(item_id):
	if request.method=="POST":
		brand=request.form['brand']
		model=request.form['model']
		image=request.form['image']
		cost=request.form['cost']
		description=request.form['description']
		item=session.query(Item).filter_by(id=item_id).one_or_none()
		item.brand=brand
		item.image=image
		item.model=model
		item.cost=cost
		item.description=description
		session.add(item)
		session.commit()
		return "<h1>Updated Successfully...<h1>"

	else:
		item=session.query(Item).filter_by(id=item_id).one_or_none()
		return render_template('edititem.html',item=item)


		# Check This Python file run by user or not
# using __name__=="__main__" 
# if condition is True then server running 
# is startrd other wise server is not run 

if __name__=="__main__":
	app.secret_key="12344JHGYUG"
	app.run(debug=True)








	
