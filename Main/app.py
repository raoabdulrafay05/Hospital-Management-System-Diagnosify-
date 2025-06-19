from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime


app = Flask(__name__,template_folder="template")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1234@localhost:5432/Hospital_Management_System'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
metadata = MetaData()

with app.app_context():
    class Patient(db.Model):
        __table__ = db.Table('patients', metadata, autoload_with=db.engine)

    class Department(db.Model):
        __table__ = db.Table('departments', metadata, autoload_with=db.engine)

    class Doctor(db.Model):
        __table__ = db.Table('doctors', metadata, autoload_with=db.engine)

    class Appointment(db.Model):
        __table__ = db.Table('appointments', metadata, autoload_with=db.engine)

    class MedicalRecord(db.Model):
        __table__ = db.Table('medicalrecords', metadata, autoload_with=db.engine)

    class Bill(db.Model):
        __table__ = db.Table('bills', metadata, autoload_with=db.engine)

    class Test(db.Model):
        __table__ = db.Table('tests', metadata, autoload_with=db.engine)
        
    class Pharmacy(db.Model):
        __table__ = db.Table('pharmacy', metadata, autoload_with = db.engine)
    
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/patient_management')
def patient_management():
    return render_template('patient_management.html')

# Doctor Management
@app.route('/doctor_management')
def doctor_management():
    return render_template('doctor_management.html')

# Appointment Scheduling
@app.route('/appointment_scheduling')
def appointment_scheduling():
    return render_template('appointment_scheduling.html')

# Medical Records Management
@app.route('/medical_records_management')
def medical_records_management():
    return render_template('medical_records_management.html')

# Pharmacy Management
@app.route('/pharmacy_management')
def pharmacy_management():
    return render_template('pharmacy.html')

# Billing
@app.route('/billing')
def billing():
    return render_template('billing.html')

# Lab Tests
@app.route('/lab_tests')
def lab_tests():
    return render_template('lab_tests.html')

# Route to add a patient
# 
@app.route('/add_patient', methods=['POST'])
def add_patient():
    full_name = request.form['FullName']
    dob = request.form['DOB']
    gender = request.form['Gender']
    contactno = request.form['ContactNo']
    address = request.form['Address']
    bloodgroup = request.form['BloodGroup']
    medicalhistory = request.form['MedicalHistory']
    
    # Create new patient record
    new_patient = Patient(
        fullname=full_name,
        dob=dob,
        gender=gender,
        contactno=contactno,
        address=address,
        bloodgroup=bloodgroup,
        medicalhistory=medicalhistory
    )
    
    db.session.add(new_patient)
    db.session.commit()
    return redirect(url_for('patient_management'))

# Route to view all patients
@app.route('/view_all_patients')
def view_all_patients():
    patients = Patient.query.all()  # Fetching all patients from the database
    print(patients)  # Logs to the console to check the data being fetched
    return render_template('view_all_patients.html', patients=patients)

def get_patient_by_id(patient_id):
    return Patient.query.get(patient_id)

# Route to view specific patient details
@app.route('/view_patient_details', methods=['GET'])
def view_patient_details():
    patient_id = request.args.get('patient_id')  # Get Patient ID from the query string
    if patient_id:
        patient = get_patient_by_id(patient_id)  # Replace with your actual database query
        if patient:
            return render_template('view_patient_details.html', patient=patient)
        else:
            return "Patient not found", 404
    return render_template('patient_id_form.html')

@app.route('/edit_patient', methods=['GET', 'POST'])
def edit_patient():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        print("Received patient_id:", patient_id)

        if not patient_id or not patient_id.isdigit():
            return "Invalid Patient ID", 400

        patient = Patient.query.get(patient_id)

        if not patient:
            return "Patient not found", 404

        # Update fields
        patient.fullname = request.form['FullName']
        patient.dob = request.form['DOB']
        patient.gender = request.form['Gender']
        patient.contactno = request.form['ContactNo']
        patient.address = request.form['Address']
        patient.bloodgroup = request.form['BloodGroup']
        patient.medicalhistory = request.form['MedicalHistory']

        db.session.commit()

        return redirect(url_for('patient_management'))

    # On GET, just show the form
    return render_template('edit_patient.html')


# Route to delete patient
@app.route('/delete_patient', methods=['GET', 'POST'])
def delete_patient():
    if request.method == 'POST':
        # Get patient_id from the form
        patient_id = request.form['patient_id']
        
        # Get the patient object from the database, or return a 404 if not found
        patient = Patient.query.get_or_404(patient_id)
        
        # Delete the patient from the database
        db.session.delete(patient)
        db.session.commit()

        # Redirect to the 'view_all_patients' route (ensure this route exists)
        return redirect(url_for('view_all_patients'))  # Redirect to the patient list

    # If GET request, display the form
    return render_template('patient_delete_form.html')


# 
@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    fullname = request.form['fullname']
    specialization = request.form['specialization']
    phone_no = request.form['phoneno']
    email = request.form['Email']
    department_id = request.form['departmentid']
    doctor_fee = request.form['DoctorFee']
    salary = request.form['Salary']
    
    # Create new doctor record
    new_doctor = Doctor(
        fullname=fullname,
        specialization=specialization,
        phoneno=phone_no,
        email=email,
        departmentid=department_id,
        doctorfee=doctor_fee,
        doctorsalary=salary
    )
    
    db.session.add(new_doctor)
    db.session.commit()
    return redirect(url_for('doctor_management'))

@app.route('/view_all_doctors')
def view_all_doctors():
    # Fetching all doctors from the database
    doctors = Doctor.query.all()  # Assuming Doctor is your model for doctors
    
    # Render the HTML template with the list of doctors
    return render_template('view_all_doctor.html', doctors=doctors)


def get_doctor_by_id(doctor_id):
    return Doctor.query.get(doctor_id)
     

@app.route('/view_doctor_details', methods=['GET'])
def view_doctor_details():
    doctor_id = request.args.get('doctor_id')  # Get Doctor ID from the query string
    
    if doctor_id:
        # Replace with actual logic to query the doctor from your database
        doctor = get_doctor_by_id(doctor_id)  # Example function to fetch doctor details by ID
        
        if doctor:
            return render_template('view_doctor_details.html', doctor=doctor)
        else:
            return "Doctor not found", 404  # Handle the case where the doctor is not found
    
    # If no doctor_id is passed, render a form to enter the doctor_id
    return render_template('doctor_view_form.html')

@app.route('/edit_doctor', methods=['GET', 'POST'])
def edit_doctor():
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')  # Get the doctor ID from the form
        print("Received doctor_id:", doctor_id)

        if not doctor_id or not doctor_id.isdigit():  # Check for valid doctor ID
            return "Invalid Doctor ID", 400

        doctor = Doctor.query.get(doctor_id)  # Fetch the doctor from the database

        if not doctor:  # Check if doctor exists
            return "Doctor not found", 404

        # Update doctor fields with new data
        doctor.fullname = request.form['fullname']
        doctor.specialization = request.form['specialization']
        doctor.phoneno = request.form['phoneno']
        doctor.email = request.form['email']
        doctor.doctorfee = request.form['doctorfee']
        doctor.doctorsalary = request.form['doctorsalary']
        doctor.departmentid = request.form['departmentid']

        db.session.commit()  # Commit the changes to the database

        return redirect(url_for('view_all_doctors'))
    return render_template('edit_doctor.html')

@app.route('/delete_doctor', methods=['GET', 'POST'])
def delete_doctor():
    if request.method == 'POST':
        doctor_id = request.form['doctor_id']
        
        # Get the doctor object from the database
        doctor = Doctor.query.get(doctor_id)

        if not doctor:
            # If doctor not found, return a 404 error or message
            return "Doctor not found", 404

        try:
            # Delete the doctor from the database
            db.session.delete(doctor)
            db.session.commit()

            # Redirect to the doctor list
            return redirect(url_for('view_all_doctors'))  # Make sure this route exists

        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            return f"Error occurred while deleting doctor: {str(e)}", 500  # Display error message

    return render_template('doctor_delete_form.html')
# 

# 
@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    patient_id = request.form.get('patientid')
    doctor_id = request.form.get('doctorid')
    date = request.form.get('appointmentdate')
    time = request.form.get('timeslot')
    
    if not all([patient_id, doctor_id, date, time]):
        return jsonify({"error": "Missing form data"}), 400
    
    # Check if the patient exists
    patient = Patient.query.get(patient_id)
    if not patient:
        return render_template('app_patient_not_found.html')

    # Check if the doctor exists
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return render_template('app_doctor_not_found.html')  # You can create a page for doctor not found

    # Create the new appointment
    new_appointment = Appointment(
        patientid=patient_id,
        doctorid=doctor_id,
        appointmentdate=datetime.strptime(date, '%Y-%m-%d').date(),
        timeslot=datetime.strptime(time, '%H:%M').time(),
        status='scheduled'
    )

    db.session.add(new_appointment)
    db.session.commit()

    return redirect(url_for('appointment_scheduling'))


@app.route('/view_appointments', methods = ['GET'])
def view_appointments():
    Appointments = Appointment.query.all()
    
    return render_template('view_appointments.html', appointments = Appointments)

@app.route('/edit_appointment', methods=['GET', 'POST'])
def edit_appointment():
    if request.method == 'POST':
        # Get the appointment ID from the form
        appointment_id = request.form.get('appointment_id')
        print("Received appointment_id:", appointment_id)

        if not appointment_id or not appointment_id.isdigit():
            return "Invalid Appointment ID", 400

        # Fetch the appointment from the database using the ID
        appointment = Appointment.query.get(appointment_id)

        if not appointment:
            return "Appointment not found", 404

        # Update fields with the new data from the form
        appointment.patientid = request.form['patient_id']
        appointment.doctorid = request.form['doctor_id']
        appointment.appointmentdate = datetime.strptime(request.form['appointment_date'], '%Y-%m-%d')
        appointment.timeslot = datetime.strptime(request.form['appointment_time'], '%H:%M').time()
        appointment.status = request.form['status']

        # Commit the changes to the database
        db.session.commit()

        # Redirect to the appointments view page
        return redirect(url_for('view_appointments'))

    return render_template('edit_appointment.html')

def get_appointment_by_id(appointment_id):
    return Appointment.query.get(appointment_id)
     

@app.route('/view_appointment_details', methods=['GET'])
def view_appointment_details():
    appointment_id = request.args.get('appointment_id')  # Get Doctor ID from the query string
    
    if appointment_id:
        # Replace with actual logic to query the doctor from your database
        appointment = get_appointment_by_id(appointment_id)  # Example function to fetch doctor details by ID
        
        if appointment:
            return render_template('view_an_appointment.html', appointment=appointment)
        else:
            return "Appointment not found", 404  # Handle the case where the doctor is not found
    
    # If no doctor_id is passed, render a form to enter the doctor_id
    return render_template('appointment_id_form.html')

@app.route('/delete_appointment', methods=['GET', 'POST'])
def delete_appointment():
    if request.method == 'POST':
        appointment_id = request.form['appointment_id']
        
        # Get the doctor object from the database
        appointment = get_appointment_by_id(appointment_id)

        if not appointment:
            # If doctor not found, return a 404 error or message
            return "Appointment not found", 404

        try:
            # Delete the doctor from the database
            db.session.delete(appointment)
            db.session.commit()
            print("DELETED")
            # Redirect to the doctor list
            return   redirect(url_for('view_appointments'))
        
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            return f"Error occurred while deleting appointment: {str(e)}", 500  # Display error message

    return render_template('appointment_delete_id_form.html')

@app.route('/add_medical_record', methods=['POST'])
def add_add_medical_record():
    patient_id = request.form['patient_id']
    doctor_id = request.form['doctor_id']
    diagnosis = request.form['diagnosis']
    prescription = request.form['prescription']
    date = request.form['date']
    
    
    # Create new patient record
    new_MedicalRecord = MedicalRecord(
        patientid=patient_id,
        doctorid=doctor_id,
        diagnosis=diagnosis,
        prescription=prescription,
        date=date,
    )
    
    db.session.add(new_MedicalRecord)
    db.session.commit()
    return redirect(url_for('medical_records_management'))

@app.route('/view_all_medical_records', methods = ['GET'])
def view_all_medical_records():
    MedicalRecords = MedicalRecord.query.all()
    
    return render_template('view_medical_records.html', MedicalRecords = MedicalRecords)

@app.route('/enter_medical_record_id', methods=['GET', 'POST'])
def enter_medical_record_id():
    if request.method == 'POST':
        # Get the medical record ID from the form
        medical_record_id = request.form.get('medical_record_id')
        print("Received medical_record_id:", medical_record_id)

        # Validate the medical record ID
        if not medical_record_id or not medical_record_id.isdigit():
            return "Invalid Medical Record ID", 400

        # Fetch the medical record from the database
        medical_record = MedicalRecord.query.get(medical_record_id)

        if not medical_record:
            return "Medical Record not found", 404

        # Redirect to the second step for updating the record
        return redirect(url_for('edit_medical_record', medical_record_id=medical_record_id))

    # Render the form to enter the medical record ID
    return render_template('edit_medical_record.html')

@app.route('/edit_medical_record/<int:medical_record_id>', methods=['GET','POST'])
def edit_medical_record(medical_record_id):
    medical_record = MedicalRecord.query.get(medical_record_id)
    print(medical_record_id)

    if not medical_record:
        return "Medical Record not found", 404

    if request.method == 'POST':
        print("nfjnfvjnvjn ifvunfuinefviunvuifnvfuinvfuinnevfiu")
        # Update the fields of the medical record with new data
        medical_record.patient_id = request.form['PatientID']
        medical_record.doctor_id = request.form['DoctorID']
        medical_record.diagnosis = request.form['Diagnosis']
        medical_record.prescription = request.form['Prescription']
        medical_record.date = request.form['Date']

        # Commit the changes to the database
        db.session.commit()

        return redirect(url_for('medical_records_management'))

    # Render the form with the existing medical record's details
    return render_template(
    'edit_medical_record_form.html',
    medical_record=medical_record,
    medical_record_id=medical_record_id
    )
    
@app.route('/view_medical_record_details', methods=['GET'])
def view_medical_record_details():
    MedicalRecordID = request.args.get('medical_record_id')  # Get Doctor ID from the query string
    
    if MedicalRecordID:
        # Replace with actual logic to query the doctor from your database
        medical_record = MedicalRecord.query.get(MedicalRecordID)
        
        if medical_record:
            return render_template('view_an_medical_record.html', medical_record=medical_record)
        else:
            return "Medical Record not found", 404  # Handle the case where the doctor is not found
    
    # If no doctor_id is passed, render a form to enter the doctor_id
    return render_template('view_an_medical_record_form.html')

@app.route('/delete_medical_record', methods=['GET', 'POST'])
def delete_medical_record():
    if request.method == 'POST':
        medical_record_id = request.form['medical_record_id']
        
        # Get the doctor object from the database
        record = MedicalRecord.query.get(medical_record_id)

        if not record:
            # If doctor not found, return a 404 error or message
            return "Medical Record not found", 404

        try:
            # Delete the doctor from the database
            db.session.delete(record)
            db.session.commit()
            # Redirect to the doctor list
            return   redirect(url_for('view_all_medical_records'))
        
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            return f"Error occurred while deleting Medical Records: {str(e)}", 500  # Display error message

    return render_template('medical_record_delete_form.html')

###
@app.route('/add_medicine', methods=['POST'])
def add_medicine():
    medicine_name = request.form['medicine_name']
    quantity = request.form['quantity']
    price_per_unit = request.form['price_per_unit']
    patientid = request.form['patient_id']

    
    # Create new patient record
    new_medicine = Pharmacy(
        medicinename=medicine_name,
        quantity=quantity,
        priceperunit=price_per_unit,
        patientid=patientid,
    )
    
    db.session.add(new_medicine)
    db.session.commit()
    return redirect(url_for('pharmacy_management'))

###

@app.route('/add_lab_test', methods=['POST'])
def add_lab_test():
    try:
        patient_id = request.form.get('patient_id')
        testtype = request.form.get('test_type')
        testresult = request.form.get('test_result')
        testdate = request.form.get('test_date')
        testprice = request.form.get('price')
        
        if not all([patient_id, testtype, testprice]):
            return jsonify({"error": "Missing form data"}), 400
        
        new_test = Test(
            patientid=patient_id,
            testdate=datetime.strptime(testdate, '%Y-%m-%d').date(),
            testtype=testtype,
            testresult = testresult,
            testprice = testprice
        )
        db.session.add(new_test)
        db.session.commit()
        return redirect(url_for('lab_tests'))
    except Exception as e:
        db.session.rollback()
        # return render_template('app_patient_not_found.html')
        return redirect(url_for('lab_tests'))
    
    
@app.route('/view_all_lab_tests', methods = ['GET'])
def view_all_lab_tests():
    tests = Test.query.all()
    
    return render_template('view_all_test.html', tests = tests)

@app.route('/enter_test_id', methods=['GET', 'POST'])
def enter_test_id():
    if request.method == 'POST':
        # Get the test ID from the form
        test_id = request.form.get('test_id')
        print("Received test_id:", test_id)

        # Validate the test ID
        if not test_id or not test_id.isdigit():
            return "Invalid Test Record ID", 400

        # Fetch the test record from the database
        test = Test.query.get(test_id)

        if not test:
            return "Test Record not found", 404

        # Redirect to the edit page for updating the record
        return redirect(url_for('edit_test_record', test_record_id=test_id))

    # Render the form to enter the test ID
    return render_template('edit_test_form.html')

@app.route('/edit_test_record/<int:test_record_id>', methods=['GET', 'POST'])
def edit_test_record(test_record_id):
    # Fetch the test record by test_record_id
    test_record = Test.query.get(test_record_id)

    if not test_record:
        return "Test Record not found", 404

    if request.method == 'POST':
        # Update the fields of the test record with new data from the form
        test_record.patientid = request.form['patientid']
        test_record.testtype = request.form['testtype']
        test_record.testresult = request.form['testresult']
        test_record.testdate = request.form['testdate']
        test_record.testprice = request.form['testprice']

        # Commit the changes to the database
        db.session.commit()

        # Redirect to view all lab tests after updating
        return redirect(url_for('view_all_lab_tests'))

    # Render the form to edit the test record
    return render_template('edit_test_record.html', test_record_id=test_record_id)

@app.route('/search_lab_test', methods=['GET'])
def search_lab_test():
    testid = request.args.get('test_id')  # Get Doctor ID from the query string
    
    if testid:
        # Replace with actual logic to query the doctor from your database
        test_record = Test.query.get(testid)
        
        if test_record:
            return render_template('view_an_test_record.html', test_record=test_record)
        else:
            return "Test Record not found", 404  # Handle the case where the doctor is not found
    
    # If no doctor_id is passed, render a form to enter the doctor_id
    return render_template('view_an_test_record_form.html')

@app.route('/delete_lab_test', methods=['GET', 'POST'])
def delete_lab_test():
    if request.method == 'POST':
        testid = request.form['test_id']
        
        # Get the doctor object from the database
        test = Test.query.get(testid)

        if not test:
            # If doctor not found, return a 404 error or message
            return "Test Record not found", 404

        try:
            # Delete the doctor from the database
            db.session.delete(test)
            db.session.commit()
            # Redirect to the doctor list
            return   redirect(url_for('view_all_lab_tests'))
        
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            return f"Error occurred while deleting Test Records: {str(e)}", 500  # Display error message

    return render_template('lab_record_delete_form.html')


def calculate_patient_bill(appointment_id, pharmacy_id, test_id):
    # Fetch the doctor's fee via appointment → doctor
    doctor_fee = db.session.query(Doctor.doctorfee).join(Appointment, Doctor.doctorid == Appointment.doctorid)\
        .filter(Appointment.appointmentid == appointment_id).scalar() or 0

    # Fetch the medicine fee using the pharmacy ID
    medicine_fee = db.session.query(
        db.func.sum(Pharmacy.quantity * Pharmacy.priceperunit)
    ).filter(Pharmacy.pharmacy_id == pharmacy_id).scalar() or 0

    # Fetch the lab test fee using the test ID
    lab_fee = db.session.query(Test.testprice)\
        .filter(Test.testid == test_id).scalar() or 0

    print(doctor_fee)
    print(lab_fee)
    print(medicine_fee)

    # Calculate the total bill
    total_amount = doctor_fee + medicine_fee + lab_fee
    print(total_amount)
    return total_amount



@app.route('/add_bill', methods=['POST'])
def add_bill():
    # Get data from a POSTed HTML form (not URL and not JSON)
    appointment_id = request.form.get('appointment_id')
    pharmacy_id = request.form.get('pharmacy_id')
    test_id = request.form.get('lab_test_id')
    patient_id = request.form.get('patient_id')
    bill_date = request.form.get('bill_date')

    # Validate required fields
    if not all([appointment_id, pharmacy_id, test_id, patient_id, bill_date]):
        return "Missing required fields", 400

    # Calculate the total bill
    total = calculate_patient_bill(appointment_id, pharmacy_id, test_id)
    print(total)
    # Create and save the bill
    new_bill = Bill(
        patientid=patient_id,
        billdate=bill_date,
        paymentstatus="unpaid",
        expenses=total
    )

    db.session.add(new_bill)
    db.session.commit()

    # Silent success (or change this line as needed)
    return redirect(url_for('billing'))

@app.route('/view_pharmcay', methods = ['GET'])
def view_pharmcay():
    medicines_history = Pharmacy.query.all()
    
    return render_template('view_all_medicine_details.html', medicines_history = medicines_history)

@app.route('/view_all_bills', methods = ['GET'])
def view_all_bills():
    bill = Bill.query.all()
    
    return render_template('view_all_bills.html', bills = bill)


@app.route('/enter_bill_id', methods=['GET', 'POST'])
def enter_bill_id():
    if request.method == 'POST':
        bill_id = request.form.get('bill_id')
        if not bill_id or not bill_id.isdigit():
            return "Invalid Bill ID", 400

        bill = Bill.query.get(int(bill_id))
        if not bill:
            return "Bill not found", 404

        return redirect(url_for('edit_bill', bill_id=bill_id))

    return render_template('enter_bill_id.html')

@app.route('/edit_bill/<int:bill_id>', methods=['GET', 'POST'])
def edit_bill(bill_id):
    bill = Bill.query.get(bill_id)
    if not bill:
        return "Bill not found", 404

    if request.method == 'POST':
        bill.patientid = request.form['patientid']
        appointment_id = request.form['appointmentid']
        pharmacy_id = request.form['pharmacyid']
        test_id = request.form['lab_test_id']

        # Recalculate the total bill
        bill.expenses = calculate_patient_bill(appointment_id, pharmacy_id, test_id)
        bill.appointmentid = appointment_id
        bill.pharmacyid = pharmacy_id
        bill.lab_test_id = test_id
        bill.paymentstatus = request.form['paymentstatus']
        bill.billdate = request.form['billdate']

        db.session.commit()
        return redirect(url_for('view_all_bills'))

    return render_template('edit_bill.html', bill=bill)

@app.route('/find_bill', methods=['GET'])
def find_bill():
    bill_id = request.args.get('bill_id')  # Get Bill ID from the query string
    
    if bill_id:
        # Replace with actual logic to query the bill from your database
        bill_record = Bill.query.get(bill_id)
        
        if bill_record:
            return render_template('view_a_bill_record.html', bill_record=bill_record)
        else:
            return "Bill Record not found", 404  # Handle the case where the bill is not found
    
    # If no bill_id is passed, render a form to enter the bill_id
    return render_template('view_a_bill_record_form.html')

@app.route('/delete_bill', methods=['GET', 'POST'])
def delete_bill():
    if request.method == 'POST':
        bill_id = request.form['bill_id']
        
        # Fetch bill from database
        bill = Bill.query.get(bill_id)

        if not bill:
            return "Bill Record not found", 404

        try:
            db.session.delete(bill)
            db.session.commit()
            return redirect(url_for('view_all_bills'))  # Update with your actual view
        except Exception as e:
            db.session.rollback()
            return f"Error occurred while deleting Bill Record: {str(e)}", 500

    return render_template('bill_record_delete_form.html')

       
if __name__ == '__main__':
    app.run(debug=True)

