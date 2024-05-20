from system import MedicalAppointmentSystem

def main():
    system = MedicalAppointmentSystem(server='DESKTOP-VIKK52P', database='ProjectPySql')
    system.connect()

    while True:
        print("\n=== Medical Appointment System Menu ===")
        print("1. Register")
        print("2. Login")

        choice = input("Enter your choice (1-2): ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            system.register_user(username, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if system.login_user(username, password):
                while True:
                    print("\n=== Authenticated Menu ===")
                    print("1. Add Patient")
                    print("2. Add Doctor")
                    print("3. Update Patient Problem")
                    print("4. Delete Doctor")
                    print("5. Delete Appointment")
                    print("6. Add Appointment")
                    print("7. Display Doctors")
                    print("8. Display Patients")
                    print("9. Display Appointments")
                    print("10. Filter Patients by Name")
                    print("11. Filter Doctors by Name")
                    print("12. Logout")
                    
                    authenticated_choice = input("Enter your choice: ")

                    if authenticated_choice == '1':
                        system.manual_add_patient()
                    elif authenticated_choice == '2':
                        system.manual_add_doctor()
                    elif authenticated_choice == '3':
                        system.manual_update_patient_problem()
                    elif authenticated_choice == '4':
                        system.manual_delete_doctor()
                    elif authenticated_choice == '5':
                        system.manual_delete_appointment()
                    elif authenticated_choice == '6':
                        system.manual_add_appointment()
                    elif authenticated_choice == '7':
                        system.display_doctors()
                    elif authenticated_choice == '8':
                        system.display_patients()
                    elif authenticated_choice == '9':
                        system.display_appointments()
                    elif authenticated_choice == '10':
                        name = input("Enter patient name to filter: ")
                        system.filter_patients_by_name(name)
                    elif authenticated_choice == '11':
                        name = input("Enter doctor name to filter: ")
                        system.filter_doctors_by_name(name)
                    elif authenticated_choice == '12':
                        system.logged_in_user = None
                        
                        print("Logged out successfully.")
                        
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Login failed.")
        else:
            print("Invalid choice. Please try again.")

        
if __name__ == "__main__":
    main()
