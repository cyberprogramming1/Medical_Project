
class Patient:
    def __init__(self, name, surname, age, gender, problem):
        self.name = name
        self.surname = surname
        self.age = age
        self.gender = gender
        self.problem = problem

class Doctor:
    def __init__(self, name, surname, work):
        self.name = name
        self.surname = surname
        self.work = work

class Appointment:
    def __init__(self, patient_id, doctor_id, appointment_date, appointment_time):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
