from flask import Flask, render_template,request,redirect,url_for
from pymongo import MongoClient
from fuzzywuzzy import fuzz
from datetime import datetime
import os
from dotenv import load_dotenv
# from bson import ObjectId
load_dotenv()
app = Flask(__name__)
mc = os.environ.get('mongoClient')
client = MongoClient(mc)
db=client.get_database('Hacknitr')
collection = db['Login']
lawyercollection = db['Lawyer Login']
bookingcollection = db['Booking Details']

UPLOAD_FOLDER = os.path.join('static', 'LawyerImages')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = collection.find_one({'email': email, 'password': password})
        
        if existing_user:
            return redirect(url_for('list'))
        else:
            return render_template('login.html', message='Invalid email or password. Please try again.')
            
    return render_template('login.html') 

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        password = request.form['password']
        
        existing_user = collection.find_one({'email': email})
        if existing_user:
            message = "User already exists. Please login."
            return render_template('login.html', message=message)
        else:
            logindata={
                'name': name,
                'phone': phone,
                'address':address,
                'email': email, 
                'password': password
            }
            collection.insert_one(logindata)
            print(f"Name: {name}, Phone: {phone}, Email: {email}, Password: {password},Address: {address}")
            return render_template('login.html', message="Register go for log in")
    
    return render_template('register.html')

'''@app.route('/lawyerreg',methods=['POST','GET'])
def lawyerregister():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address=request.form['address']
        password = request.form['password']
        
        existing_user = lawyercollection.find_one({'email': email})
        if existing_user:
            message = "User already exists. Please login."
            return render_template('lawyerreg.html', message=message)
        else:
            logindata={
                'name': name,
                'phone': phone,
                'address':address,
                'email': email, 
                'password': password
    
            }
            lawyercollection.insert_one(logindata)
            return redirect(url_for('lawyerlogin'))
    
    return render_template('lawyerreg.html') 

'''
def lawyerregister():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']
        
        # Handle image upload
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                filename = image.filename
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
            else:
                filename = None
        else:
            filename = None
        
        existing_user = lawyercollection.find_one({'email': email})
        if existing_user:
            message = "User already exists. Please login."
            return render_template('lawyerreg.html', message=message)
            
        else:
            logindata = {
                'name': name,
                'phone': phone,
                'address': address,
                'email': email,
                'password': password,
                'image': filename  # Store the image filename in MongoDB
            }
            lawyercollection.insert_one(logindata)
            return redirect(url_for('lawyerlogin'))

    return render_template('lawyerreg.html')
@app.route('/lawyerlogin', methods=['POST','GET'])
def lawyerlogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = lawyercollection.find_one({'email': email, 'password': password})
        
        if existing_user:
            return redirect(url_for('lawyermainpage',email=email))
        else:
            return render_template('lawyerlogin.html', message='Invalid email or password. Please try again.')
            
    return render_template('lawyerlogin.html') 

@app.route('/list',methods=['POST',"GET"])
def list():
    return render_template('list.html')

if __name__ == '__main__':
    app.run(debug=True)