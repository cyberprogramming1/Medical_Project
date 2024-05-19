import pyodbc
import hashlib
from datetime import datetime
from database import Database
from models import Patient, Doctor, Appointment
from utils import parse_date, parse_time

class MedicalAppointmentSystem(Database):
    def __init__(self, server, database):
        super().__init__(server, database)
        self.logged_in_user = None

    def register_user(self, username, password):
        try:
            # Hash the password before storing it in the database
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)",
                           (username, hashed_password))
            self.connection.commit()
            cursor.close()
            print("User registered successfully.")
        except pyodbc.Error as e:
            print(f"Error registering user: {e}")

    def login_user(self, username, password):
        try:
            # Hash the provided password to compare it with the stored hash
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            cursor = self.connection.cursor()
            cursor.execute("SELECT Password FROM Users WHERE Username = ?", (username,))
            stored_password = cursor.fetchone()

            if stored_password and hashed_password == stored_password[0]:
                print("Login successful.")
                self.logged_in_user = username  # Set the logged-in user
                return True
            else:
                print("Invalid username or password.")
                return False
        except pyodbc.Error as e:
            print(f"Error logging in: {e}")

    def is_authenticated(self):
        return self.logged_in_user is not None

    
    def add_patient(self, name, surname, age, gender, problem):
        if self.connection is None:
            print("No database connection. Please connect to the database first.")
            return
        
        patient = Patient(name, surname, age, gender, problem)
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Patients (Patient_Name, Patient_Surname, Patient_Age, Patient_Gender, Patient_Problem) VALUES (?, ?, ?, ?, ?)",
                           (patient.name, patient.surname, patient.age, patient.gender, patient.problem))
            self.connection.commit()
            cursor.close()
            print("Patient added successfully.")
        except pyodbc.Error as e:
            print(f"Error adding patient: {e}")

    def add_doctor(self, name, surname, work):
        doctor = Doctor(name, surname, work)
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Doctors (Doctor_Name, Doctor_Surname, Doctor_work) VALUES (?, ?, ?)",
                           (doctor.name, doctor.surname, doctor.work))
            self.connection.commit()
            cursor.close()
            print("Doctor added successfully.")
        except pyodbc.Error as e:
            print(f"Error adding doctor: {e}")

    def update_patient_problem(self, patient_id, new_problem):
        try:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE Patients SET Patient_Problem = ? WHERE PatientID = ?",
                           (new_problem, patient_id))
            self.connection.commit()
            cursor.close()
            print("Patient problem updated successfully.")
        except pyodbc.Error as e:
            print(f"Error updating patient problem: {e}")

    def delete_doctor(self, doctor_id):
        try:
            cursor = self.connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM Appointment WHERE DoctorID = ?", (doctor_id,))
            appointment_count = cursor.fetchone()[0]

            if appointment_count > 0:
                print(f"Error: Doctor has {appointment_count} associated appointments. Please delete appointments first.")
            else:
                cursor.execute("DELETE FROM Doctors WHERE DoctorID = ?", (doctor_id,))
                self.connection.commit()
                print("Doctor deleted successfully.")

            cursor.close()
        except pyodbc.Error as e:
            print(f"Error deleting doctor: {e}")

    def delete_appointment(self, appointment_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM Appointment WHERE AppointmentID = ?", (appointment_id,))
            self.connection.commit()
            print("Appointment deleted successfully.")
            cursor.close()
        except pyodbc.Error as e:
            print(f"Error deleting appointment: {e}")

    def add_appointment(self, patient_id, doctor_id, appointment_date, appointment_time):
        appointment = Appointment(patient_id, doctor_id, appointment_date, appointment_time)
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Appointment (PatientID, DoctorID, AppointmentDate, AppointmentTime) VALUES (?, ?, ?, ?)",
                           (appointment.patient_id, appointment.doctor_id, appointment.appointment_date, appointment.appointment_time))
            self.connection.commit()
            cursor.close()
            print("Appointment added successfully.")
        except pyodbc.Error as e:
            print(f"Error adding appointment: {e}")

    def manual_add_patient(self):
        name = input("Enter patient's name: ")
        surname = input("Enter patient's surname: ")
        age = int(input("Enter patient's age: "))
        gender = input("Enter patient's gender: ")
        problem = input("Enter patient's problem: ")
        self.add_patient(name, surname, age, gender, problem)

    def manual_add_doctor(self):
        name = input("Enter doctor's name: ")
        surname = input("Enter doctor's surname: ")
        work = input("Enter doctor's work/hospital: ")
        self.add_doctor(name, surname, work)

    def manual_update_patient_problem(self):
        patient_id = int(input("Enter patient ID to update problem: "))
        new_problem = input("Enter new problem description: ")
        self.update_patient_problem(patient_id, new_problem)

    def manual_delete_doctor(self):
        doctor_id = int(input("Enter doctor ID to delete: "))
        self.delete_doctor(doctor_id)

    def manual_delete_appointment(self):
        appointment_id = int(input("Enter Appointment ID to delete: "))
        self.delete_appointment(appointment_id)

    def manual_add_appointment(self):
        try:
            patient_id = int(input("Enter Patient ID for the appointment: "))
            doctor_id = int(input("Enter Doctor ID for the appointment: "))
            appointment_date_str = input("Enter Appointment Date (YYYY-MM-DD): ")
            appointment_time_str = input("Enter Appointment Time (HH:MM:SS): ")
            appointment_date = parse_date(appointment_date_str)
            appointment_time = parse_time(appointment_time_str)

            self.add_appointment(patient_id, doctor_id, appointment_date, appointment_time)
        except ValueError as ve:
            print(f"Error: Invalid input format. {ve}")
        except pyodbc.Error as e:
            print(f"Error adding appointment: {e}")    

    def display_doctors(self):
        doctors = self.get_doctors()
        if doctors:
            print("Doctors:")
            for doctor in doctors:
                print(f"ID: {doctor.DoctorID}, Name: {doctor.Doctor_Name}, Surname: {doctor.Doctor_Surname}, Work: {doctor.Doctor_work}")
        else:
            print("No doctors found.")

    def display_patients(self):
        patients = self.get_patients()
        if patients:
            print("Patients:")
            for patient in patients:
                print(f"ID: {patient.PatientID}, Name: {patient.Patient_Name}, Surname: {patient.Patient_Surname}, Age: {patient.Patient_Age}, Gender: {patient.Patient_Gender}, Problem: {patient.Patient_Problem}")
        else:
            print("No patients found.")
    
    def display_appointments(self):
        appointments = self.get_appointments()
        if appointments:
            print("Appointments:")
            for appointment in appointments:
                print(f"ID: {appointment.AppointmentID}, Patient ID: {appointment.PatientID}, Doctor ID: {appointment.DoctorID}, Date: {appointment.AppointmentDate}, Time: {appointment.AppointmentTime}")
        else:
            print("No appointments found.")

    def get_doctors(self):
        doctors = []
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Doctors")
            doctors = cursor.fetchall()
            cursor.close()
        except pyodbc.Error as e:
            print(f"Error fetching doctors: {e}")
        return doctors

    def get_patients(self):
        patients = []
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Patients")
            patients = cursor.fetchall()
            cursor.close()
        except pyodbc.Error as e:
            print(f"Error fetching patients: {e}")
        return patients

    def get_appointments(self):
        appointments = []
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Appointment")
            appointments = cursor.fetchall()
            cursor.close()
        except pyodbc.Error as e:
            print(f"Error fetching appointments: {e}")
        return appointments
