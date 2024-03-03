from flask import Flask, render_template,request,redirect,url_for, session, jsonify, send_file
from pymongo import MongoClient
import uuid
import PyPDF2
from fuzzywuzzy import fuzz
from datetime import datetime
import os
from dotenv import load_dotenv
from bson import ObjectId
import uuid
import webbrowser
import PyPDF2
import openai
from fpdf import FPDF
import io

load_dotenv()
app = Flask(__name__)
opAPI = os.environ.get("openAI")
openai.api_key = opAPI
mc = os.environ.get('mongoClient')
client = MongoClient(mc)
db=client.get_database('Hacknitr')
collection = db['Login']
lawyercollection = db['Lawyer Login']
bookingcollection = db['Booking Details']
app.config['secret_key']  = 'asfiabfasbfj'

@app.route('/')
def index():
    return render_template('index.html')


def chat_gpt(prompt):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
     
        messages = [{"role" : "user", "content":prompt}]
    )
    return response.choices[0].message.content.strip()

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Set left margin (adjust as needed)
    pdf.set_left_margin(10)

    # Split the text into lines
    lines = text.split('\n')

    for line in lines:
        # Use MultiCell for automatic word wrapping
        pdf.multi_cell(0, 10, txt=line)  # '0' means auto width, '10' is line height

    pdf_output = pdf.output(dest='S').encode('latin1')
    return io.BytesIO(pdf_output)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    types = ["Contracts & Agreements", "Real Estate Plannings & Commercial Transactions", "Regulatory Compliance & Financial Documents", "Intellectual Properties", "Formation & Governance"]

    data = request.get_json()
    received_string = data['string']
    print(received_string)
    for char in received_string:
    # Check if the character is numeric
        if char.isdigit():
            # Extract the first numeric character
            index = int(char)
            break
    

    Btype = types[index-1]
    print(f"Received string: {received_string}")
    # You can now process the received string as needed
    prompt = f'''
    Write  a formal and professional Contract of type: {Btype} with the details that i will provide.
    Details are: 
    [{received_string}]

    your reply should strictly be the contract.'''

    FinalContract = chat_gpt(prompt)
    print(FinalContract)
    pdf_buffer = create_pdf(FinalContract)
    # return jsonify({'message': 'String received successfully'})
    return send_file(
        pdf_buffer,
        download_name='Generated_Contract.pdf',
        as_attachment=True,
        mimetype='application/pdf'
    )

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

@app.route('/list',methods=['POST',"GET"])
def list():
    return render_template('list.html')


def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)

    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    return text


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    try:
        file = request.files['pdfFile']
        if file:
            session_id = str(uuid.uuid4())
            file_path = f'temporary/{session_id}.pdf'
            file.save(file_path)
            print(extract_text_from_pdf(file))
            data = extract_text_from_pdf(file)

            # Perform PDF processing logic (extract text, etc.)
            # For simplicity, let's just print a success message
            print("PDF uploaded successfully")
            session['pdfPath'] = file_path
            
            return jsonify({'success': True, 'message': 'PDF uploaded successfully', 'pdfName': file_path, 'data': data})
        
        else:
            return jsonify({'success': False, 'message': 'No file uploaded'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


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
    
    return render_template('login.html')

@app.route('/lawyerreg',methods=['POST','GET'])
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
@app.route('/lawyerreg',methods=['POST','GET'])
def lawyerregister():
    if request.method == 'POST':
        # imagen = request.files['image']
        # print(imagen)
        image = request.files['image']
        lawyer_data = {
            'name': request.form['name'],
            'phone': request.form['phone'],
            'email': request.form['email'],
            'address': request.form['address'],
            'department': request.form['department'],
            'password': request.form['password'],
            'image': str(uuid.uuid4()) + '.' + image.filename.rsplit('.', 1)[1].lower()
        }
        
        # image.save('static/' + image)

        
        existing_user = lawyercollection.find_one({'email': lawyer_data['email']})
        if existing_user:
            message = "User already exists. Please login."
            return render_template('lawyerlogin.html', message=message)
            
        else:
            lawyercollection.insert_one(lawyer_data)
            image.save(os.path.join("static", lawyer_data['image']))
            # print("image save")
            return redirect(url_for('lawyerlogin'))

    return render_template('lawyerlogin.html')
'''

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

@app.route('/findlawyer', methods=['POST','GET'])
def findlawyer():
    results = []
    
    if request.method == 'POST':
        # Check if it's a search request
        query = request.form.get('query')
        if query:
            for lawyer in lawyercollection.find():
                name_ratio = fuzz.partial_ratio(query.lower(), lawyer['name'].lower())
                address_ratio = fuzz.partial_ratio(query.lower(), lawyer['address'].lower())
                if name_ratio >= 80 or address_ratio >= 80:
                    results.append(lawyer)
            print(results)
        else:
            # It's a booking request
            client_name = request.form.get('clientName')
            client_email = request.form.get('clientEmail')
            client_phone = request.form.get('clientPhone')
            lawyer_name = request.form.get('lawyerName')
            lawyer_email = request.form.get('lawyerEmail')
            lawyer_phone = request.form.get('lawyerPhone')

            current_datetime = datetime.now()

            # Convert date object to datetime object
            appointment_date = current_datetime

            booking_details = {
                'client_name': client_name,
                'client_email': client_email,
                'client_phone': client_phone,
                'lawyer_name': lawyer_name,
                'lawyer_email': lawyer_email,
                'lawyer_phone': lawyer_phone,
                'appointment_datetime': appointment_date,
                'active': "1",
            }
            print(booking_details)
            bookingcollection.insert_one(booking_details)

    return render_template('findlawyer.html', results=results)

@app.route('/lawyermainpage',methods=['POST',"GET"])
def lawyermainpage():
    if request.method == 'GET':
        email = request.args.get('email')
        lawyer_data = bookingcollection.find({'lawyer_email': email})
        return render_template('lawyermainpage.html', email=email, lawyer_data=lawyer_data)

    elif request.method == 'POST':
        case_id = request.form.get('caseId')
        email = request.form.get('email')
        print(case_id)
        bookingcollection.update_one({'_id': ObjectId(case_id)}, {'$set': {'active': "0"}})

        lawyer_data = bookingcollection.find({'lawyer_email': email})
        return render_template('lawyermainpage.html', email=email, lawyer_data=lawyer_data)
    return render_template('lawyermainpage.html')

if __name__ == '__main__':
    app.run()
