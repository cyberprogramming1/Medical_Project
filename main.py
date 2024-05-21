from database import Database
from Patient.patient import PatientManagement
from Doctor.doctor import DoctorManagement
from Appointment.appointment import AppointmentManagement
from authentication.login import LoginSystem
from authentication.register import RegisterSystem
from Report.report import ReportGeneration
from datetime import datetime

def main():
    server = 'DESKTOP-VIKK52P'
    database = 'ProjectPySql'
    db = Database(server, database)
    db.connect()

    patient_management = PatientManagement(db.connection)
    doctor_management = DoctorManagement(db.connection)
    appointment_management = AppointmentManagement(db.connection)
    login_system = LoginSystem(db.connection)
    register_system = RegisterSystem(db.connection)
    report_generation = ReportGeneration(db.connection)

    while True:
        print("\n=== Medical Appointment System Menu ===")
        print("1. Register")
        print("2. Login")

        choice = input("Enter your choice (1-2): ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_system.register_user(username, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if login_system.login_user(username, password):
                while True:
                    print("\n=== Authenticated Menu ===")
                    print("1.Add Patient")
                    print("2.Add Doctor")
                    print("3.Update Patient Problem")
                    print("4.Delete Doctor")
                    print("5.Delete Appointment")
                    print("6.Add Appointment")
                    print("7.Display Doctors")
                    print("8.Display Patients")
                    print("9.Display Appointments")
                    print("10.Filter Patients by Name")
                    print("11.Filter Doctors by Name")
                    print("12.Filter Appointments by Date")
                    print("13.Generate Patient Report")
                    print("14.Generate Doctor Report")
                    print("15.Generate Appointment Report")
                    print("16. Count Patients Accepted by Doctor in Month")
                    print("17.Logout")
                    
                    authenticated_choice = input("Enter your choice: ")

                    if authenticated_choice == '1':
                        patient_management.manual_add_patient()
                    elif authenticated_choice == '2':
                        doctor_management.manual_add_doctor()
                    elif authenticated_choice == '3':
                        patient_management.manual_update_patient_problem()
                    elif authenticated_choice == '4':
                        doctor_management.manual_delete_doctor()
                    elif authenticated_choice == '5':
                        appointment_management.manual_delete_appointment()
                    elif authenticated_choice == '6':
                        appointment_management.manual_add_appointment()
                    elif authenticated_choice == '7':
                        doctor_management.display_doctors()
                    elif authenticated_choice == '8':
                        patient_management.display_patients()
                    elif authenticated_choice == '9':
                        appointment_management.display_appointments()
                    elif authenticated_choice == '10':
                        name = input("Enter patient name to filter: ")
                        patient_management.filter_patients_by_name(name)
                    elif authenticated_choice == '11':
                        name = input("Enter doctor name to filter: ")
                        doctor_management.filter_doctors_by_name(name)
                    elif authenticated_choice == '12':
                        date = input("Enter appointment date to filter (YYYY-MM-DD): ")
                        appointment_management.filter_appointments_by_date(date)
                    
                    elif authenticated_choice == '13':
                        filename = input("Enter the filename for the patient report (default: patient_report.txt): ")
                        filename = filename if filename else "patient_report.txt"
                        report_generation.generate_patient_report(filename)
                    elif authenticated_choice == '14':
                        filename = input("Enter the filename for the doctor report (default: doctor_report.txt): ")
                        filename = filename if filename else "doctor_report.txt"
                        report_generation.generate_doctor_report(filename)
                    elif authenticated_choice == '15':
                        filename = input("Enter the filename for the appointment report (default: appointment_report.txt): ")
                        filename = filename if filename else "appointment_report.txt"
                        report_generation.generate_appointment_report(filename)
                    
                    elif authenticated_choice == '16':
                        doctor_id = int(input("Enter the doctor ID: "))
                        start_date = input("Enter the start date (YYYY-MM-DD): ")
                        end_date = input("Enter the end date (YYYY-MM-DD): ")
                        start_date = datetime.strptime(start_date, "%Y-%m-%d")
                        end_date = datetime.strptime(end_date, "%Y-%m-%d")
                        count = report_generation.count_patients_accepted_by_doctor_in_month(doctor_id, start_date, end_date)
                        if count is not None:
                            print(f"Doctor ID {doctor_id} accepted {count} patients between {start_date.strftime('%Y-%m-%d')} and {end_date.strftime('%Y-%m-%d')}.")
                        else:
                            print("Error occurred while counting patients.")

                    elif authenticated_choice == '17':
                        login_system.logout()
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Login failed.")
        else:
            print("Invalid choice. Please try again.")

    db.disconnect()

if __name__ == "__main__":
    main()
