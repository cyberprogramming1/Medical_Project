from model.models import Patient
import pyodbc
from tabulate import tabulate

class PatientManagement:
    def __init__(self, connection):
        self.connection = connection

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

    def display_patients(self):
        patients = self.get_patients()
        if patients:
            headers = ["ID", "Name", "Surname", "Age", "Gender", "Problem"]
            table = [[patient.PatientID, patient.Patient_Name, patient.Patient_Surname, patient.Patient_Age, patient.Patient_Gender, patient.Patient_Problem] for patient in patients]
            print(tabulate(table, headers, tablefmt="grid"))
        else:
            print("No patients found.")
    
    def manual_add_patient(self):
        name = input("Enter patient's name: ")
        surname = input("Enter patient's surname: ")
        age = int(input("Enter patient's age: "))
        gender = input("Enter patient's gender: ")
        problem = input("Enter patient's problem: ")
        self.add_patient(name, surname, age, gender, problem)
    
    def manual_update_patient_problem(self):
        patient_id = int(input("Enter patient ID to update problem: "))
        new_problem = input("Enter new problem description: ")
        self.update_patient_problem(patient_id, new_problem)

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

    def filter_patients_by_name(self, name):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Patients WHERE Patient_Name LIKE ?", ('%' + name + '%',))
            patients = cursor.fetchall()
            cursor.close()
            if patients:
                headers = ["ID", "Name", "Surname", "Age", "Gender", "Problem"]
                table = [[patient.PatientID, patient.Patient_Name, patient.Patient_Surname, patient.Patient_Age, patient.Patient_Gender, patient.Patient_Problem] for patient in patients]
                print(tabulate(table, headers, tablefmt="grid"))
            else:
                print("No patients found with that name.")
        except pyodbc.Error as e:
            print(f"Error filtering patients: {e}")
