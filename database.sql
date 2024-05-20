CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Username NVARCHAR(50) UNIQUE,
    Password NVARCHAR(100) -- Adjust length as needed
);


create table Patients(
PatientID int primary key identity(1,1),
Patient_Name varchar(50) ,
Patient_Surname varchar(50),
Patient_Age int ,
Patient_Gender varchar(50),
Patient_Problem varchar(50)
);

create table Doctors(
DoctorID int primary key identity(1,1),
Doctor_Name varchar(50),
Doctor_Surname varchar(50),
Doctor_work varchar(50)
);

create table Appointment (
	AppointmentID INT PRIMARY KEY identity(1,1),
    PatientID INT,
    DoctorID INT,
    AppointmentDate DATE,
    AppointmentTime TIME,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID)

);

ALTER TABLE Appointment
DROP CONSTRAINT FK__Appointme__Docto__00200768;

ALTER TABLE Appointment
ADD CONSTRAINT FK__Appointme__Docto__00200768
FOREIGN KEY (DoctorID)
REFERENCES Doctors(DoctorID)
ON DELETE CASCADE;


select * from Patients;
select * from Doctors;
select * from Appointment;
select * from Users;

delete Appointment;
delete Patients;
delete Doctors;
delete Users;





DBCC CHECKIDENT ('Patients', RESEED, 0);
DBCC CHECKIDENT ('Doctors', RESEED, 0);
DBCC CHECKIDENT ('Appointment', RESEED, 0);
DBCC CHECKIDENT ('Users', RESEED, 0);
