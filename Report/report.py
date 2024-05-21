from tabulate import tabulate
import os
import pyodbc
class ReportGeneration:
    def __init__(self, connection):
        self.connection = connection

    def generate_patient_report(self, filename="patient_report.txt"):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Patients")
            patients = cursor.fetchall()
            cursor.close()

            headers = ["ID", "Name", "Surname", "Age", "Gender", "Problem"]
            table = [[patient.PatientID, patient.Patient_Name, patient.Patient_Surname, patient.Patient_Age, patient.Patient_Gender, patient.Patient_Problem] for patient in patients]
            report_content = tabulate(table, headers, tablefmt="grid")

            with open(filename, 'w') as file:
                file.write(report_content)

            print(f"Patient report generated successfully and saved to {filename}.")
        except Exception as e:
            print(f"Error generating patient report: {e}")

    def generate_doctor_report(self, filename="doctor_report.txt"):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Doctors")
            doctors = cursor.fetchall()
            cursor.close()

            headers = ["ID", "Name", "Surname", "Work"]
            table = [[doctor.DoctorID, doctor.Doctor_Name, doctor.Doctor_Surname, doctor.Doctor_work] for doctor in doctors]
            report_content = tabulate(table, headers, tablefmt="grid")

            with open(filename, 'w') as file:
                file.write(report_content)

            print(f"Doctor report generated successfully and saved to {filename}.")
        except Exception as e:
            print(f"Error generating doctor report: {e}")

    def generate_appointment_report(self, filename="appointment_report.txt"):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Appointment")
            appointments = cursor.fetchall()
            cursor.close()

            headers = ["ID", "Patient ID", "Doctor ID", "Date", "Time"]
            table = [[appointment.AppointmentID, appointment.PatientID, appointment.DoctorID, appointment.AppointmentDate, appointment.AppointmentTime] for appointment in appointments]
            report_content = tabulate(table, headers, tablefmt="grid")

            with open(filename, 'w') as file:
                file.write(report_content)

            print(f"Appointment report generated successfully and saved to {filename}.")
        except Exception as e:
            print(f"Error generating appointment report: {e}")
    


    # calculates the number of patients accepted by a doctor

    def count_patients_accepted_by_doctor_in_month(self, doctor_id, start_date, end_date):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM Appointment 
                WHERE DoctorID = ? 
                AND AppointmentDate >= ? 
                AND AppointmentDate <= ?
            """, (doctor_id, start_date, end_date))
            count = cursor.fetchone()[0]
            cursor.close()

            return count
        except pyodbc.Error as e:
            print(f"Error counting patients: {e}")
            return None
    
