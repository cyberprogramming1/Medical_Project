from model.models import Doctor
import pyodbc
from tabulate import tabulate


class DoctorManagement:
    def __init__(self, connection):
        self.connection = connection

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

    def manual_add_doctor(self):
        name = input("Enter doctor's name: ")
        surname = input("Enter doctor's surname: ")
        work = input("Enter doctor's work/hospital: ")
        self.add_doctor(name, surname, work)
    
    def manual_delete_doctor(self):
        doctor_id = int(input("Enter doctor ID to delete: "))
        self.delete_doctor(doctor_id)

    def display_doctors(self):
        doctors = self.get_doctors()
        if doctors:
            headers = ["ID", "Name", "Surname", "Work"]
            table = [[doctor.DoctorID, doctor.Doctor_Name, doctor.Doctor_Surname, doctor.Doctor_work] for doctor in doctors]
            print(tabulate(table, headers, tablefmt="grid"))
        else:
            print("No doctors found.")

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

    def filter_doctors_by_name(self, name):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Doctors WHERE Doctor_Name LIKE ?", ('%' + name + '%',))
            doctors = cursor.fetchall()
            cursor.close()
            if doctors:
                headers = ["ID", "Name", "Surname", "Work"]
                table = [[doctor.DoctorID, doctor.Doctor_Name, doctor.Doctor_Surname, doctor.Doctor_work] for doctor in doctors]
                print(tabulate(table, headers, tablefmt="grid"))
            else:
                print("No doctors found with that name.")
        except pyodbc.Error as e:
            print(f"Error filtering doctors: {e}")
