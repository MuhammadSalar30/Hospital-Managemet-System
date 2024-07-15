import tkinter as tk
from tkinter import messagebox, ttk
import cx_Oracle
import threading

# Function to connect to the Oracle database
def connect_to_db():
    TNS_ALIAS = "<alias>"
    USERNAME = "Sys"
    PASSWORD = "Sal321"
    try:
        connection = cx_Oracle.connect(f"{USERNAME}/{PASSWORD}@{TNS_ALIAS}", mode=cx_Oracle.SYSDBA)
        return connection
    except cx_Oracle.Error as error:
        messagebox.showerror("Connection Error", f"Error connecting to Oracle database: {error}")
        return None

# Function to check if a record exists in a table
def record_exists(table, column, value):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {column} = :1", (value,))
            result = cursor.fetchone()
            return result[0] > 0
        except cx_Oracle.Error as error:
            messagebox.showerror("Query Error", f"Error checking record existence: {error}")
            return False
        finally:
            cursor.close()
            connection.close()
    return False

# Function to execute the SQL file
def execute_sql_file():
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            with open('Hospital Management System.sql', 'r') as file:
                sql_commands = file.read().split(';')
                for command in sql_commands:
                    if command.strip():
                        cursor.execute(command)
            connection.commit()
            messagebox.showinfo("Success", "Database setup successfully")
        except cx_Oracle.Error as error:
            messagebox.showerror("SQL Execution Error", f"Error executing SQL file: {error}")
        finally:
            cursor.close()
            connection.close()

# Function for inserting records with detailed error messages
def insert_record(table, entries):
    def run_insert():
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            try:
                if table == "Patients":
                    patient_id = int(entries['PatientID'].get())
                    patient_name = entries['PatientName'].get()
                    patient_dob = entries['PatientDOB'].get()
                    patient_gender = entries['PatientGender'].get()

                    cursor.execute("INSERT INTO Patients (PatientID, PatientName, PatientDOB, PatientGender) VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4)",
                                   (patient_id, patient_name, patient_dob, patient_gender))
                elif table == "Appointments":
                    appointment_id = int(entries['AppointmentID'].get())
                    patient_id = int(entries['PatientID'].get())
                    doctor_id = int(entries['DoctorID'].get())
                    appointment_date = entries['AppointmentDate'].get()
                    appointment_reason = entries['AppointmentReason'].get()

                    if not record_exists("Patients", "PatientID", patient_id):
                        messagebox.showerror("Insert Error", f"PatientID {patient_id} does not exist in Patients table.")
                        return
                    if not record_exists("Doctors", "DoctorID", doctor_id):
                        messagebox.showerror("Insert Error", f"DoctorID {doctor_id} does not exist in Doctors table.")
                        return

                    cursor.execute("INSERT INTO Appointments (AppointmentID, PatientID, DoctorID, AppointmentDate, AppointmentReason) VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5)",
                                   (appointment_id, patient_id, doctor_id, appointment_date, appointment_reason))
                elif table == "MedicalRecords":
                    medical_record_id = int(entries['MedicalRecordID'].get())
                    patient_id = int(entries['PatientID'].get())
                    medical_record_details = entries['MedicalRecordDetails'].get()

                    cursor.execute("INSERT INTO MedicalRecords (MedicalRecordID, PatientID, MedicalRecordDetails) VALUES (:1, :2, :3)",
                                   (medical_record_id, patient_id, medical_record_details))
                elif table == "Billing":
                    bill_id = int(entries['BillID'].get())
                    patient_id = int(entries['PatientID'].get())
                    bill_amount = float(entries['BillAmount'].get())

                    cursor.execute("INSERT INTO Billing (BillID, PatientID, BillAmount) VALUES (:1, :2, :3)",
                                   (bill_id, patient_id, bill_amount))
                elif table == "PatientRooms":
                    patient_id = int(entries['PatientID'].get())
                    room_id = int(entries['RoomID'].get())
                    admission_date = entries['AdmissionDate'].get()
                    discharge_date = entries['DischargeDate'].get()

                    cursor.execute("INSERT INTO PatientRooms (PatientID, RoomID, AdmissionDate, DischargeDate) VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), TO_DATE(:4, 'YYYY-MM-DD'))",
                                   (patient_id, room_id, admission_date, discharge_date))
                elif table == "Departments":
                    department_id = int(entries['DepartmentID'].get())
                    department_name = entries['DepartmentName'].get()

                    cursor.execute("INSERT INTO Departments (DepartmentID, DepartmentName) VALUES (:1, :2)",
                                   (department_id, department_name))
                elif table == "Doctors":
                    doctor_id = int(entries['DoctorID'].get())
                    doctor_name = entries['DoctorName'].get()
                    department_id = int(entries['DepartmentID'].get())

                    if not record_exists("Departments", "DepartmentID", department_id):
                        messagebox.showerror("Insert Error", f"DepartmentID {department_id} does not exist in Departments table.")
                        return

                    cursor.execute("INSERT INTO Doctors (DoctorID, DoctorName, DepartmentID) VALUES (:1, :2, :3)",
                                   (doctor_id, doctor_name, department_id))
                elif table == "Treatments":
                    treatment_id = int(entries['TreatmentID'].get())
                    appointment_id = int(entries['AppointmentID'].get())
                    treatment_details = entries['TreatmentDetails'].get()

                    if not record_exists("Appointments", "AppointmentID", appointment_id):
                        messagebox.showerror("Insert Error", f"AppointmentID {appointment_id} does not exist in Appointments table.")
                        return

                    cursor.execute("INSERT INTO Treatments (TreatmentID, AppointmentID, TreatmentDetails) VALUES (:1, :2, :3)",
                                   (treatment_id, appointment_id, treatment_details))
                elif table == "Staff":
                    staff_id = int(entries['StaffID'].get())
                    staff_name = entries['StaffName'].get()
                    department_id = int(entries['DepartmentID'].get())

                    if not record_exists("Departments", "DepartmentID", department_id):
                        messagebox.showerror("Insert Error", f"DepartmentID {department_id} does not exist in Departments table.")
                        return

                    cursor.execute("INSERT INTO Staff (StaffID, StaffName, DepartmentID) VALUES (:1, :2, :3)",
                                   (staff_id, staff_name, department_id))
                elif table == "Rooms":
                    room_id = int(entries['RoomID'].get())
                    room_number = entries['RoomNumber'].get()

                    cursor.execute("INSERT INTO Rooms (RoomID, RoomNumber) VALUES (:1, :2)",
                                   (room_id, room_number))
                elif table == "Prescriptions":
                    prescription_id = int(entries['PrescriptionID'].get())
                    treatment_id = int(entries['TreatmentID'].get())
                    prescription_details = entries['PrescriptionDetails'].get()

                    cursor.execute("INSERT INTO Prescriptions (PrescriptionID, TreatmentID, PrescriptionDetails) VALUES (:1, :2, :3)",
                                   (prescription_id, treatment_id, prescription_details))
                # Add similar logic for other tables

                connection.commit()
                messagebox.showinfo("Success", "Record inserted successfully")
            except cx_Oracle.Error as error:
                messagebox.showerror("Insert Error", f"Error inserting record: {error}")
            except Exception as e:
                messagebox.showerror("Insert Error", f"An unexpected error occurred: {str(e)}")
            finally:
                cursor.close()
                connection.close()

    threading.Thread(target=run_insert).start()

# Function for updating records
def update_record(table, entries):
    def run_update():
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            try:
                if table == "Patients":
                    patient_id = int(entries['PatientID'].get())
                    patient_name = entries['PatientName'].get()
                    patient_dob = entries['PatientDOB'].get()
                    patient_gender = entries['PatientGender'].get()

                    cursor.execute("UPDATE Patients SET PatientName = :1, PatientDOB = TO_DATE(:2, 'YYYY-MM-DD'), PatientGender = :3 WHERE PatientID = :4",
                                   (patient_name, patient_dob, patient_gender, patient_id))
                elif table == "Appointments":
                    appointment_id = int(entries['AppointmentID'].get())
                    patient_id = int(entries['PatientID'].get())
                    doctor_id = int(entries['DoctorID'].get())
                    appointment_date = entries['AppointmentDate'].get()
                    appointment_reason = entries['AppointmentReason'].get()

                    if not record_exists("Patients", "PatientID", patient_id):
                        messagebox.showerror("Update Error", f"PatientID {patient_id} does not exist in Patients table.")
                        return
                    if not record_exists("Doctors", "DoctorID", doctor_id):
                        messagebox.showerror("Update Error", f"DoctorID {doctor_id} does not exist in Doctors table.")
                        return

                    cursor.execute("UPDATE Appointments SET PatientID = :1, DoctorID = :2, AppointmentDate = TO_DATE(:3, 'YYYY-MM-DD'), AppointmentReason = :4 WHERE AppointmentID = :5",
                                   (patient_id, doctor_id, appointment_date, appointment_reason, appointment_id))
                elif table == "MedicalRecords":
                    medical_record_id = int(entries['MedicalRecordID'].get())
                    patient_id = int(entries['PatientID'].get())
                    medical_record_details = entries['MedicalRecordDetails'].get()

                    cursor.execute("UPDATE MedicalRecords SET PatientID = :1, MedicalRecordDetails = :2 WHERE MedicalRecordID = :3",
                                   (patient_id, medical_record_details, medical_record_id))
                elif table == "Billing":
                    bill_id = int(entries['BillID'].get())
                    patient_id = int(entries['PatientID'].get())
                    bill_amount = float(entries['BillAmount'].get())

                    cursor.execute("UPDATE Billing SET PatientID = :1, BillAmount = :2 WHERE BillID = :3",
                                   (patient_id, bill_amount, bill_id))
                elif table == "PatientRooms":
                    patient_id = int(entries['PatientID'].get())
                    room_id = int(entries['RoomID'].get())
                    admission_date = entries['AdmissionDate'].get()
                    discharge_date = entries['DischargeDate'].get()

                    cursor.execute("UPDATE PatientRooms SET RoomID = :1, AdmissionDate = TO_DATE(:2, 'YYYY-MM-DD'), DischargeDate = TO_DATE(:3, 'YYYY-MM-DD') WHERE PatientID = :4",
                                   (room_id, admission_date, discharge_date, patient_id))
                elif table == "Departments":
                    department_id = int(entries['DepartmentID'].get())
                    department_name = entries['DepartmentName'].get()

                    cursor.execute("UPDATE Departments SET DepartmentName = :1 WHERE DepartmentID = :2",
                                   (department_name, department_id))
                elif table == "Doctors":
                    doctor_id = int(entries['DoctorID'].get())
                    doctor_name = entries['DoctorName'].get()
                    department_id = int(entries['DepartmentID'].get())

                    if not record_exists("Departments", "DepartmentID", department_id):
                        messagebox.showerror("Update Error", f"DepartmentID {department_id} does not exist in Departments table.")
                        return

                    cursor.execute("UPDATE Doctors SET DoctorName = :1, DepartmentID = :2 WHERE DoctorID = :3",
                                   (doctor_name, department_id, doctor_id))
                elif table == "Treatments":
                    treatment_id = int(entries['TreatmentID'].get())
                    appointment_id = int(entries['AppointmentID'].get())
                    treatment_details = entries['TreatmentDetails'].get()

                    if not record_exists("Appointments", "AppointmentID", appointment_id):
                        messagebox.showerror("Update Error", f"AppointmentID {appointment_id} does not exist in Appointments table.")
                        return

                    cursor.execute("UPDATE Treatments SET AppointmentID = :1, TreatmentDetails = :2 WHERE TreatmentID = :3",
                                   (appointment_id, treatment_details, treatment_id))
                elif table == "Staff":
                    staff_id = int(entries['StaffID'].get())
                    staff_name = entries['StaffName'].get()
                    department_id = int(entries['DepartmentID'].get())

                    if not record_exists("Departments", "DepartmentID", department_id):
                        messagebox.showerror("Update Error", f"DepartmentID {department_id} does not exist in Departments table.")
                        return

                    cursor.execute("UPDATE Staff SET StaffName = :1, DepartmentID = :2 WHERE StaffID = :3",
                                   (staff_name, department_id, staff_id))
                elif table == "Rooms":
                    room_id = int(entries['RoomID'].get())
                    room_number = entries['RoomNumber'].get()

                    cursor.execute("UPDATE Rooms SET RoomNumber = :1 WHERE RoomID = :2",
                                   (room_number, room_id))
                elif table == "Prescriptions":
                    prescription_id = int(entries['PrescriptionID'].get())
                    treatment_id = int(entries['TreatmentID'].get())
                    prescription_details = entries['PrescriptionDetails'].get()

                    cursor.execute("UPDATE Prescriptions SET TreatmentID = :1, PrescriptionDetails = :2 WHERE PrescriptionID = :3",
                                   (treatment_id, prescription_details, prescription_id))
                # Add similar logic for other tables

                connection.commit()
                messagebox.showinfo("Success", "Record updated successfully")
            except cx_Oracle.Error as error:
                messagebox.showerror("Update Error", f"Error updating record: {error}")
            finally:
                cursor.close()
                connection.close()

    threading.Thread(target=run_update).start()

# Function for deleting records
def delete_record(table, entries):
    def run_delete():
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            try:
                if table == "Patients":
                    patient_id = int(entries['PatientID'].get())

                    cursor.execute("DELETE FROM Appointments WHERE PatientID = :1", (patient_id,))
                    cursor.execute("DELETE FROM MedicalRecords WHERE PatientID = :1", (patient_id,))
                    cursor.execute("DELETE FROM Billing WHERE PatientID = :1", (patient_id,))
                    cursor.execute("DELETE FROM PatientRooms WHERE PatientID = :1", (patient_id,))
                    cursor.execute("DELETE FROM Patients WHERE PatientID = :1", (patient_id,))
                elif table == "Appointments":
                    appointment_id = int(entries['AppointmentID'].get())

                    cursor.execute("DELETE FROM Treatments WHERE AppointmentID = :1", (appointment_id,))
                    cursor.execute("DELETE FROM Prescriptions WHERE AppointmentID = :1", (appointment_id,))
                    cursor.execute("DELETE FROM Appointments WHERE AppointmentID = :1", (appointment_id,))
                elif table == "MedicalRecords":
                    medical_record_id = int(entries['MedicalRecordID'].get())

                    cursor.execute("DELETE FROM MedicalRecords WHERE MedicalRecordID = :1", (medical_record_id,))
                elif table == "Billing":
                    bill_id = int(entries['BillID'].get())

                    cursor.execute("DELETE FROM Billing WHERE BillID = :1", (bill_id,))
                elif table == "PatientRooms":
                    patient_id = int(entries['PatientID'].get())
                    room_id = int(entries['RoomID'].get())

                    cursor.execute("DELETE FROM PatientRooms WHERE PatientID = :1 AND RoomID = :2", (patient_id, room_id))
                elif table == "Departments":
                    department_id = int(entries['DepartmentID'].get())

                    cursor.execute("DELETE FROM Departments WHERE DepartmentID = :1", (department_id,))
                elif table == "Doctors":
                    doctor_id = int(entries['DoctorID'].get())

                    cursor.execute("DELETE FROM Doctors WHERE DoctorID = :1", (doctor_id,))
                elif table == "Treatments":
                    treatment_id = int(entries['TreatmentID'].get())

                    cursor.execute("DELETE FROM Treatments WHERE TreatmentID = :1", (treatment_id,))
                elif table == "Staff":
                    staff_id = int(entries['StaffID'].get())

                    cursor.execute("DELETE FROM Staff WHERE StaffID = :1", (staff_id,))
                elif table == "Rooms":
                    room_id = int(entries['RoomID'].get())

                    cursor.execute("DELETE FROM Rooms WHERE RoomID = :1", (room_id,))
                elif table == "Prescriptions":
                    prescription_id = int(entries['PrescriptionID'].get())

                    cursor.execute("DELETE FROM Prescriptions WHERE PrescriptionID = :1", (prescription_id,))
                # Add similar logic for other tables

                connection.commit()
                messagebox.showinfo("Success", "Record deleted successfully")
            except cx_Oracle.Error as error:
                messagebox.showerror("Delete Error", f"Error deleting record: {error}")
            finally:
                cursor.close()
                connection.close()

    threading.Thread(target=run_delete).start()

# Function for searching records
def search_record(table, entries):
    def run_search():
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            try:
                if table == "Patients":
                    patient_id = int(entries['PatientID'].get())

                    cursor.execute("SELECT * FROM Patients WHERE PatientID = :1", (patient_id,))
                    result = cursor.fetchone()
                    if result:
                        messagebox.showinfo("Search Result", f"Record found: {result}")
                    else:
                        messagebox.showinfo("Search Result", "No record found")
                elif table == "Appointments":
                    appointment_id = int(entries['AppointmentID'].get())

                    cursor.execute("SELECT * FROM Appointments WHERE AppointmentID = :1", (appointment_id,))
                    result = cursor.fetchone()
                    if result:
                        messagebox.showinfo("Search Result", f"Record found: {result}")
                    else:
                        messagebox.showinfo("Search Result", "No record found")
                elif table == "MedicalRecords":
                    medical_record_id = int(entries['MedicalRecordID'].get())

                    cursor.execute("SELECT * FROM MedicalRecords WHERE MedicalRecordID = :1", (medical_record_id,))
                    result = cursor.fetchone()
                    if result:
                        messagebox.showinfo("Search Result", f"Record found: {result}")
                    else:
                        messagebox.showinfo("Search Result", "No record found")
                elif table == "Billing":
                    bill_id = int(entries['BillID'].get())

                    cursor.execute("SELECT * FROM Billing WHERE BillID = :1", (bill_id,))
                    result = cursor.fetchone()
                    if result:
                        messagebox.showinfo("Search Result", f"Record found: {result}")
                    else:
                        messagebox.showinfo("Search Result", "No record found")
                elif table == "PatientRooms":
                    patient_id = int(entries['PatientID'].get())
                    room_id = int(entries['RoomID'].get())

                    cursor.execute("SELECT * FROM PatientRooms WHERE PatientID = :1 AND RoomID = :2", (patient_id, room_id))
                    result = cursor.fetchone()
                    if result:
                        messagebox.showinfo("Search Result", f"Record found: {result}")
                    else:
                        messagebox.showinfo("Search Result", "No record found")
                elif table == "Departments":
                    department_id = int(entries['DepartmentID'].get())

                    cursor.execute("SELECT * FROM Departments WHERE DepartmentID = :1", (department_id,))
                    result = cursor.fetchone()
                    if result:
                        messagebox.showinfo("Search Result", f"Record found: {result}")
                    else:
                        messagebox.showinfo("Search Result", "No record found")
                elif table == "Doctors":
                    doctor_id = int(entries['DoctorID'].get())

                    cursor.execute("SELECT * FROM Doctors WHERE DoctorID = :1", (doctor_id,))
                    result = cursor.fetchone()
                    if result:
                        messagebox.showinfo("Search Result", f"Record found: {result}")
                    else:
                        messagebox.showinfo("Search Result", "No record found")
                elif table == "Treatments":
                    treatment_id = int(entries['TreatmentID'].get())

                    cursor.execute("SELECT * FROM Treatments WHERE TreatmentID = :1", (treatment_id,))
                    result = cursor.fetchone()
                    if result:
                        messagebox.showinfo("Search Result", f"Record found: {result}")
                    else:
                        messagebox.showinfo("Search Result", "No record found")
                elif table == "Staff":
                    staff_id = int(entries['StaffID'].get())

                    cursor.execute("SELECT * FROM Staff WHERE StaffID = :1", (staff_id,))
                    result = cursor.fetchone()
                    if result:
                        messagebox.showinfo("Search Result", f"Record found: {result}")
                    else:
                        messagebox.showinfo("Search Result", "No record found")
                elif table == "Rooms":
                    room_id = int(entries['RoomID'].get())

                    cursor.execute("SELECT * FROM Rooms WHERE RoomID = :1", (room_id,))
                    result = cursor.fetchone()
                    if result:
                        messagebox.showinfo("Search Result", f"Record found: {result}")
                    else:
                        messagebox.showinfo("Search Result", "No record found")
                elif table == "Prescriptions":
                    prescription_id = int(entries['PrescriptionID'].get())

                    cursor.execute("SELECT * FROM Prescriptions WHERE PrescriptionID = :1", (prescription_id,))
                    result = cursor.fetchone()
                    if result:
                        messagebox.showinfo("Search Result", f"Record found: {result}")
                    else:
                        messagebox.showinfo("Search Result", "No record found")
                # Add similar logic for other tables
            except cx_Oracle.Error as error:
                messagebox.showerror("Search Error", f"Error searching record: {error}")
            finally:
                cursor.close()
                connection.close()

    threading.Thread(target=run_search).start()

# Function to display all records from a specified table in a Treeview widget
def show_all_records(table):
    def run_show():
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            try:
                # Fetch column names for the selected table
                cursor.execute(f"SELECT COLUMN_NAME FROM ALL_TAB_COLUMNS WHERE TABLE_NAME = UPPER('{table}')")
                columns = [row[0] for row in cursor.fetchall()]

                # Clear the existing columns
                tree["columns"] = columns
                tree.delete(*tree.get_children())

                # Create column headers dynamically
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, anchor=tk.CENTER)

                # Fetch and display the records
                cursor.execute(f"SELECT * FROM {table}")
                records = cursor.fetchall()

                for record in records:
                    tree.insert('', 'end', values=record)

            except cx_Oracle.Error as error:
                messagebox.showerror("Display Error", f"Error displaying records: {error}")
            finally:
                cursor.close()
                connection.close()

    threading.Thread(target=run_show).start()

# Function to create CRUD operation fields dynamically
def create_crud_fields(table):
    for widget in crud_frame.winfo_children():
        widget.destroy()

    entries = {}
    row_num = 0

    if table == "Patients":
        entries['PatientID'] = create_label_and_entry(crud_frame, "Patient ID", row_num, 0)
        entries['PatientName'] = create_label_and_entry(crud_frame, "Patient Name", row_num+1, 0)
        entries['PatientDOB'] = create_label_and_entry(crud_frame, "Patient DOB (YYYY-MM-DD)", row_num+2, 0)
        entries['PatientGender'] = create_label_and_entry(crud_frame, "Patient Gender", row_num+3, 0)
        row_num += 4
    elif table == "Appointments":
        entries['AppointmentID'] = create_label_and_entry(crud_frame, "Appointment ID", row_num, 0)
        entries['PatientID'] = create_label_and_entry(crud_frame, "Patient ID", row_num+1, 0)
        entries['DoctorID'] = create_label_and_entry(crud_frame, "Doctor ID", row_num+2, 0)
        entries['AppointmentDate'] = create_label_and_entry(crud_frame, "Appointment Date (YYYY-MM-DD)", row_num+3, 0)
        entries['AppointmentReason'] = create_label_and_entry(crud_frame, "Appointment Reason", row_num+4, 0)
        row_num += 5
    elif table == "MedicalRecords":
        entries['MedicalRecordID'] = create_label_and_entry(crud_frame, "Medical Record ID", row_num, 0)
        entries['PatientID'] = create_label_and_entry(crud_frame, "Patient ID", row_num+1, 0)
        entries['MedicalRecordDetails'] = create_label_and_entry(crud_frame, "Medical Record Details", row_num+2, 0)
        row_num += 3
    elif table == "Billing":
        entries['BillID'] = create_label_and_entry(crud_frame, "Bill ID", row_num, 0)
        entries['PatientID'] = create_label_and_entry(crud_frame, "Patient ID", row_num+1, 0)
        entries['BillAmount'] = create_label_and_entry(crud_frame, "Bill Amount", row_num+2, 0)
        row_num += 3
    elif table == "PatientRooms":
        entries['PatientID'] = create_label_and_entry(crud_frame, "Patient ID", row_num, 0)
        entries['RoomID'] = create_label_and_entry(crud_frame, "Room ID", row_num+1, 0)
        entries['AdmissionDate'] = create_label_and_entry(crud_frame, "Admission Date (YYYY-MM-DD)", row_num+2, 0)
        entries['DischargeDate'] = create_label_and_entry(crud_frame, "Discharge Date (YYYY-MM-DD)", row_num+3, 0)
        row_num += 4
    elif table == "Departments":
        entries['DepartmentID'] = create_label_and_entry(crud_frame, "Department ID", row_num, 0)
        entries['DepartmentName'] = create_label_and_entry(crud_frame, "Department Name", row_num+1, 0)
        row_num += 2
    elif table == "Doctors":
        entries['DoctorID'] = create_label_and_entry(crud_frame, "Doctor ID", row_num, 0)
        entries['DoctorName'] = create_label_and_entry(crud_frame, "Doctor Name", row_num+1, 0)
        entries['DepartmentID'] = create_label_and_entry(crud_frame, "Department ID", row_num+2, 0)
        row_num += 3
    elif table == "Treatments":
        entries['TreatmentID'] = create_label_and_entry(crud_frame, "Treatment ID", row_num, 0)
        entries['AppointmentID'] = create_label_and_entry(crud_frame, "Appointment ID", row_num+1, 0)
        entries['TreatmentDetails'] = create_label_and_entry(crud_frame, "Treatment Details", row_num+2, 0)
        row_num += 3
    elif table == "Staff":
        entries['StaffID'] = create_label_and_entry(crud_frame, "Staff ID", row_num, 0)
        entries['StaffName'] = create_label_and_entry(crud_frame, "Staff Name", row_num+1, 0)
        entries['DepartmentID'] = create_label_and_entry(crud_frame, "Department ID", row_num+2, 0)
        row_num += 3
    elif table == "Rooms":
        entries['RoomID'] = create_label_and_entry(crud_frame, "Room ID", row_num, 0)
        entries['RoomNumber'] = create_label_and_entry(crud_frame, "Room Number", row_num+1, 0)
        row_num += 2
    elif table == "Prescriptions":
        entries['PrescriptionID'] = create_label_and_entry(crud_frame, "Prescription ID", row_num, 0)
        entries['TreatmentID'] = create_label_and_entry(crud_frame, "Treatment ID", row_num+1, 0)
        entries['PrescriptionDetails'] = create_label_and_entry(crud_frame, "Prescription Details", row_num+2, 0)
        row_num += 3
    # Add fields for other tables similarly

    button_font = ("Arial", 14)
    tk.Button(crud_frame, text="Insert", font=button_font, command=lambda: insert_record(table, entries)).grid(row=row_num, column=0, padx=5, pady=10)
    tk.Button(crud_frame, text="Update", font=button_font, command=lambda: update_record(table, entries)).grid(row=row_num, column=1, padx=5, pady=10)
    tk.Button(crud_frame, text="Delete", font=button_font, command=lambda: delete_record(table, entries)).grid(row=row_num, column=2, padx=5, pady=10)
    tk.Button(crud_frame, text="Search", font=button_font, command=lambda: search_record(table, entries)).grid(row=row_num, column=3, padx=5, pady=10)
    tk.Button(crud_frame, text="Show All", font=button_font, command=lambda: show_all_records(table)).grid(row=row_num, column=4, padx=5, pady=10)

# Function to create a label and entry widget
def create_label_and_entry(frame, text, row, column):
    label = tk.Label(frame, text=text, font=("Arial", 12))
    label.grid(row=row, column=column, padx=5, pady=5, sticky=tk.W)
    entry = tk.Entry(frame, font=("Arial", 12))
    entry.grid(row=row, column=column+1, padx=5, pady=5, sticky=tk.W)
    return entry

# Setup the GUI
root = tk.Tk()
root.title("Hospital Management System")

# Create the main title
title_label = tk.Label(root, text="HOSPITAL MANAGEMENT SYSTEM", font=("Arial", 24, "bold"))
title_label.pack(pady=20)

# Frame for the dropdown and CRUD operations
dropdown_frame = tk.Frame(root)
dropdown_frame.pack(pady=20)

# Dropdown menu for table selection
table_var = tk.StringVar()
table_var.set("Select a Table")
tables = ["Patients", "Appointments", "MedicalRecords", "Billing", "PatientRooms", "Departments", "Doctors", "Treatments", "Staff", "Rooms", "Prescriptions"]
dropdown_menu = tk.OptionMenu(dropdown_frame, table_var, *tables, command=create_crud_fields)
dropdown_menu.config(font=("Arial", 14))
dropdown_menu.pack()

# Frame for CRUD operations
crud_frame = tk.Frame(root)
crud_frame.pack(pady=20)

# Frame for displaying records
display_frame = tk.Frame(root)
display_frame.pack(pady=20)

# Create a Treeview widget for displaying records
tree = ttk.Treeview(display_frame, show="headings")
tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a button to setup the database
setup_button = tk.Button(root, text="Setup Database", font=("Arial", 14), command=execute_sql_file)
setup_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
