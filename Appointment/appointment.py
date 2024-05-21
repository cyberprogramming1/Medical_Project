from model.models import Appointment
from Date.time.utils import parse_date, parse_time
import pyodbc
from tabulate import tabulate
from datetime import datetime

class AppointmentManagement:
    def __init__(self, connection):
        self.connection = connection

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

    def delete_appointment(self, appointment_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM Appointment WHERE AppointmentID = ?", (appointment_id,))
            self.connection.commit()
            print("Appointment deleted successfully.")
            cursor.close()
        except pyodbc.Error as e:
            print(f"Error deleting appointment: {e}")

    def display_appointments(self):
        appointments = self.get_appointments()
        if appointments:
            headers = ["ID", "Patient ID", "Doctor ID", "Date", "Time"]
            table = [[appointment.AppointmentID, appointment.PatientID, appointment.DoctorID, appointment.AppointmentDate, appointment.AppointmentTime] for appointment in appointments]
            print(tabulate(table, headers, tablefmt="grid"))
        else:
            print("No appointments found.")

            
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
    
    def filter_appointments_by_date(self, date):
        try:
            # Convert date string to datetime object
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Appointment WHERE AppointmentDate = ?", (date_obj,))
            appointments = cursor.fetchall()
            cursor.close()

            if appointments:
                headers = ["ID", "Patient ID", "Doctor ID", "Date", "Time"]
                table = [[appointment.AppointmentID, appointment.PatientID, appointment.DoctorID, appointment.AppointmentDate, appointment.AppointmentTime] for appointment in appointments]
                print(tabulate(table, headers, tablefmt="grid"))
            else:
                print("No appointments found for the specified date.")
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
        except pyodbc.Error as e:
            print(f"Error filtering appointments: {e}")
