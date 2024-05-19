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
                print("Login successful.")
                break
            else:
                print("Login failed. Try again.")
        else:
            print("Invalid choice. Please try again.")

    while system.is_authenticated():
        print("\n=== Medical Appointment System Menu ===")
        print("3. Add Patient")
        print("4. Add Doctor")
        print("5. Update Patient Problem")
        print("6. Delete Doctor")
        print("7. Add Appointment")
        print("8. Display Doctors")
        print("9. Display Patients")
        print("10. Display Appointments")
        print("11. Delete Appointment")
        print("12. Exit")

        choice = input("Enter your choice (3-12): ")

        if choice == '3':
            system.manual_add_patient()
        elif choice == '4':
            system.manual_add_doctor()
        elif choice == '5':
            system.manual_update_patient_problem()
        elif choice == '6':
            system.manual_delete_doctor()
        elif choice == '7':
            system.manual_add_appointment()
        elif choice == '8':
            system.display_doctors()
        elif choice == '9':
            system.display_patients()
        elif choice == '10':
            system.display_appointments()
        elif choice == '11':
            system.manual_delete_appointment()
        elif choice == '12':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

    system.disconnect()

if __name__ == "__main__":
    main()
