DROP TABLE Departments CASCADE CONSTRAINTS;
DROP TABLE Patients CASCADE CONSTRAINTS;
DROP TABLE Doctors CASCADE CONSTRAINTS;
DROP TABLE Appointments CASCADE CONSTRAINTS;
DROP TABLE Treatments CASCADE CONSTRAINTS;
DROP TABLE MedicalRecords CASCADE CONSTRAINTS;
DROP TABLE Staff CASCADE CONSTRAINTS;
DROP TABLE Billing CASCADE CONSTRAINTS;
DROP TABLE Rooms CASCADE CONSTRAINTS;
DROP TABLE PatientRooms CASCADE CONSTRAINTS;
DROP TABLE Prescriptions CASCADE CONSTRAINTS;

-- Create the Departments table
CREATE TABLE Departments (
    DepartmentID INT PRIMARY KEY,
    DepartmentName VARCHAR2(100) NOT NULL
);

-- Create the Patients table
CREATE TABLE Patients (
    PatientID INT PRIMARY KEY,
    PatientName VARCHAR2(100) NOT NULL,
    PatientDOB DATE NOT NULL,
    PatientGender CHAR(1) NOT NULL
);

-- Create the Doctors table
CREATE TABLE Doctors (
    DoctorID INT PRIMARY KEY,
    DoctorName VARCHAR2(100) NOT NULL,
    DepartmentID INT,
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

-- Create the Appointments table
CREATE TABLE Appointments (
    AppointmentID INT PRIMARY KEY,
    PatientID INT,
    DoctorID INT,
    AppointmentDate DATE NOT NULL,
    AppointmentReason VARCHAR2(255),
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID)
);

-- Create the Treatments table
CREATE TABLE Treatments (
    TreatmentID INT PRIMARY KEY,
    AppointmentID INT,
    TreatmentDetails VARCHAR2(255),
    FOREIGN KEY (AppointmentID) REFERENCES Appointments(AppointmentID)
);

-- Create the MedicalRecords table
CREATE TABLE MedicalRecords (
    MedicalRecordID INT PRIMARY KEY,
    PatientID INT,
    MedicalRecordDetails VARCHAR2(255),
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);

-- Create the Staff table
CREATE TABLE Staff (
    StaffID INT PRIMARY KEY,
    StaffName VARCHAR2(100) NOT NULL,
    DepartmentID INT,
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

-- Create the Billing table
CREATE TABLE Billing (
    BillID INT PRIMARY KEY,
    PatientID INT,
    BillAmount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);

-- Create the Rooms table
CREATE TABLE Rooms (
    RoomID INT PRIMARY KEY,
    RoomNumber VARCHAR2(10) NOT NULL
);

-- Create the PatientRooms table
CREATE TABLE PatientRooms (
    PatientID INT,
    RoomID INT,
    AdmissionDate DATE NOT NULL,
    DischargeDate DATE,
    PRIMARY KEY (PatientID, RoomID),
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID)
);

-- Create the Prescriptions table
CREATE TABLE Prescriptions (
    PrescriptionID INT PRIMARY KEY,
    TreatmentID INT,
    PrescriptionDetails VARCHAR2(255),
    FOREIGN KEY (TreatmentID) REFERENCES Treatments(TreatmentID)
);

-- Insert into Departments
INSERT INTO Departments (DepartmentID, DepartmentName) VALUES (1, 'Cardiology');
INSERT INTO Departments (DepartmentID, DepartmentName) VALUES (2, 'Neurology');
INSERT INTO Departments (DepartmentID, DepartmentName) VALUES (3, 'Pediatrics');
INSERT INTO Departments (DepartmentID, DepartmentName) VALUES (4, 'Orthopedics');
INSERT INTO Departments (DepartmentID, DepartmentName) VALUES (5, 'Dermatology');
INSERT INTO Departments (DepartmentID, DepartmentName) VALUES (6, 'Oncology');
INSERT INTO Departments (DepartmentID, DepartmentName) VALUES (7, 'Gastroenterology');

-- Insert into Patients
INSERT INTO Patients (PatientID, PatientName, PatientDOB, PatientGender) VALUES (1, 'Ayesha Khan', TO_DATE('1985-05-15', 'YYYY-MM-DD'), 'F');
INSERT INTO Patients (PatientID, PatientName, PatientDOB, PatientGender) VALUES (2, 'Ali Raza', TO_DATE('1990-08-22', 'YYYY-MM-DD'), 'M');
INSERT INTO Patients (PatientID, PatientName, PatientDOB, PatientGender) VALUES (3, 'Fatima Bibi', TO_DATE('2002-12-01', 'YYYY-MM-DD'), 'F');
INSERT INTO Patients (PatientID, PatientName, PatientDOB, PatientGender) VALUES (4, 'Bilal Ahmed', TO_DATE('1975-07-30', 'YYYY-MM-DD'), 'M');
INSERT INTO Patients (PatientID, PatientName, PatientDOB, PatientGender) VALUES (5, 'Sana Tariq', TO_DATE('1995-03-12', 'YYYY-MM-DD'), 'F');
INSERT INTO Patients (PatientID, PatientName, PatientDOB, PatientGender) VALUES (6, 'Hassan Shah', TO_DATE('1988-11-20', 'YYYY-MM-DD'), 'M');
INSERT INTO Patients (PatientID, PatientName, PatientDOB, PatientGender) VALUES (7, 'Zainab Farooq', TO_DATE('2000-02-25', 'YYYY-MM-DD'), 'F');

-- Insert into Doctors
INSERT INTO Doctors (DoctorID, DoctorName, DepartmentID) VALUES (1, 'Dr. Ahmed Malik', 1);
INSERT INTO Doctors (DoctorID, DoctorName, DepartmentID) VALUES (2, 'Dr. Sara Rehman', 2);
INSERT INTO Doctors (DoctorID, DoctorName, DepartmentID) VALUES (3, 'Dr. Usman Tariq', 3);
INSERT INTO Doctors (DoctorID, DoctorName, DepartmentID) VALUES (4, 'Dr. Nadia Saeed', 4);
INSERT INTO Doctors (DoctorID, DoctorName, DepartmentID) VALUES (5, 'Dr. Faisal Khan', 5);
INSERT INTO Doctors (DoctorID, DoctorName, DepartmentID) VALUES (6, 'Dr. Asma Qureshi', 6);
INSERT INTO Doctors (DoctorID, DoctorName, DepartmentID) VALUES (7, 'Dr. Imran Ali', 7);

-- Insert into Appointments
INSERT INTO Appointments (AppointmentID, PatientID, DoctorID, AppointmentDate, AppointmentReason) VALUES (1, 1, 1, TO_DATE('2024-05-20', 'YYYY-MM-DD'), 'Routine Checkup');
INSERT INTO Appointments (AppointmentID, PatientID, DoctorID, AppointmentDate, AppointmentReason) VALUES (2, 2, 2, TO_DATE('2024-06-01', 'YYYY-MM-DD'), 'Headache');
INSERT INTO Appointments (AppointmentID, PatientID, DoctorID, AppointmentDate, AppointmentReason) VALUES (3, 3, 3, TO_DATE('2024-06-10', 'YYYY-MM-DD'), 'Fever');
INSERT INTO Appointments (AppointmentID, PatientID, DoctorID, AppointmentDate, AppointmentReason) VALUES (4, 4, 4, TO_DATE('2024-06-15', 'YYYY-MM-DD'), 'Knee Pain');
INSERT INTO Appointments (AppointmentID, PatientID, DoctorID, AppointmentDate, AppointmentReason) VALUES (5, 5, 5, TO_DATE('2024-06-20', 'YYYY-MM-DD'), 'Skin Rash');
INSERT INTO Appointments (AppointmentID, PatientID, DoctorID, AppointmentDate, AppointmentReason) VALUES (6, 6, 6, TO_DATE('2024-06-25', 'YYYY-MM-DD'), 'Routine Cancer Screening');
INSERT INTO Appointments (AppointmentID, PatientID, DoctorID, AppointmentDate, AppointmentReason) VALUES (7, 7, 7, TO_DATE('2024-06-30', 'YYYY-MM-DD'), 'Stomach Ache');

-- Insert into Treatments
INSERT INTO Treatments (TreatmentID, AppointmentID, TreatmentDetails) VALUES (1, 1, 'Blood Test');
INSERT INTO Treatments (TreatmentID, AppointmentID, TreatmentDetails) VALUES (2, 2, 'MRI Scan');
INSERT INTO Treatments (TreatmentID, AppointmentID, TreatmentDetails) VALUES (3, 3, 'Prescribed Paracetamol');
INSERT INTO Treatments (TreatmentID, AppointmentID, TreatmentDetails) VALUES (4, 4, 'X-Ray');
INSERT INTO Treatments (TreatmentID, AppointmentID, TreatmentDetails) VALUES (5, 5, 'Skin Biopsy');
INSERT INTO Treatments (TreatmentID, AppointmentID, TreatmentDetails) VALUES (6, 6, 'CT Scan');
INSERT INTO Treatments (TreatmentID, AppointmentID, TreatmentDetails) VALUES (7, 7, 'Endoscopy');

-- Insert into MedicalRecords
INSERT INTO MedicalRecords (MedicalRecordID, PatientID, MedicalRecordDetails) VALUES (1, 1, 'No significant past medical history');
INSERT INTO MedicalRecords (MedicalRecordID, PatientID, MedicalRecordDetails) VALUES (2, 2, 'History of migraines');
INSERT INTO MedicalRecords (MedicalRecordID, PatientID, MedicalRecordDetails) VALUES (3, 3, 'No known allergies');
INSERT INTO MedicalRecords (MedicalRecordID, PatientID, MedicalRecordDetails) VALUES (4, 4, 'History of arthritis');
INSERT INTO MedicalRecords (MedicalRecordID, PatientID, MedicalRecordDetails) VALUES (5, 5, 'Eczema');
INSERT INTO MedicalRecords (MedicalRecordID, PatientID, MedicalRecordDetails) VALUES (6, 6, 'Family history of cancer');
INSERT INTO MedicalRecords (MedicalRecordID, PatientID, MedicalRecordDetails) VALUES (7, 7, 'No significant past medical history');

-- Insert into Staff
INSERT INTO Staff (StaffID, StaffName, DepartmentID) VALUES (1, 'Nurse Maria', 1);
INSERT INTO Staff (StaffID, StaffName, DepartmentID) VALUES (2, 'Technician Bilal', 2);
INSERT INTO Staff (StaffID, StaffName, DepartmentID) VALUES (3, 'Clerk Sana', 3);
INSERT INTO Staff (StaffID, StaffName, DepartmentID) VALUES (4, 'Receptionist Ahmed', 4);
INSERT INTO Staff (StaffID, StaffName, DepartmentID) VALUES (5, 'Janitor Adeel', 5);
INSERT INTO Staff (StaffID, StaffName, DepartmentID) VALUES (6, 'Pharmacist Farah', 6);
INSERT INTO Staff (StaffID, StaffName, DepartmentID) VALUES (7, 'Assistant Tariq', 7);

-- Insert into Billing
INSERT INTO Billing (BillID, PatientID, BillAmount) VALUES (1, 1, 5000.00);
INSERT INTO Billing (BillID, PatientID, BillAmount) VALUES (2, 2, 15000.00);
INSERT INTO Billing (BillID, PatientID, BillAmount) VALUES (3, 3, 2000.00);
INSERT INTO Billing (BillID, PatientID, BillAmount) VALUES (4, 4, 3000.00);
INSERT INTO Billing (BillID, PatientID, BillAmount) VALUES (5, 5, 8000.00);
INSERT INTO Billing (BillID, PatientID, BillAmount) VALUES (6, 6, 12000.00);
INSERT INTO Billing (BillID, PatientID, BillAmount) VALUES (7, 7, 4000.00);

-- Insert into Rooms
INSERT INTO Rooms (RoomID, RoomNumber) VALUES (1, '101');
INSERT INTO Rooms (RoomID, RoomNumber) VALUES (2, '102');
INSERT INTO Rooms (RoomID, RoomNumber) VALUES (3, '103');
INSERT INTO Rooms (RoomID, RoomNumber) VALUES (4, '104');
INSERT INTO Rooms (RoomID, RoomNumber) VALUES (5, '105');
INSERT INTO Rooms (RoomID, RoomNumber) VALUES (6, '106');
INSERT INTO Rooms (RoomID, RoomNumber) VALUES (7, '107');

-- Insert into PatientRooms
INSERT INTO PatientRooms (PatientID, RoomID, AdmissionDate, DischargeDate) VALUES (1, 1, TO_DATE('2024-05-20', 'YYYY-MM-DD'), TO_DATE('2024-05-21', 'YYYY-MM-DD'));
INSERT INTO PatientRooms (PatientID, RoomID, AdmissionDate, DischargeDate) VALUES (2, 2, TO_DATE('2024-06-01', 'YYYY-MM-DD'), TO_DATE('2024-06-02', 'YYYY-MM-DD'));
INSERT INTO PatientRooms (PatientID, RoomID, AdmissionDate, DischargeDate) VALUES (3, 3, TO_DATE('2024-06-10', 'YYYY-MM-DD'), TO_DATE('2024-06-11', 'YYYY-MM-DD'));
INSERT INTO PatientRooms (PatientID, RoomID, AdmissionDate, DischargeDate) VALUES (4, 4, TO_DATE('2024-06-15', 'YYYY-MM-DD'), TO_DATE('2024-06-16', 'YYYY-MM-DD'));
INSERT INTO PatientRooms (PatientID, RoomID, AdmissionDate, DischargeDate) VALUES (5, 5, TO_DATE('2024-06-20', 'YYYY-MM-DD'), TO_DATE('2024-06-21', 'YYYY-MM-DD'));
INSERT INTO PatientRooms (PatientID, RoomID, AdmissionDate, DischargeDate) VALUES (6, 6, TO_DATE('2024-06-25', 'YYYY-MM-DD'), TO_DATE('2024-06-26', 'YYYY-MM-DD'));
INSERT INTO PatientRooms (PatientID, RoomID, AdmissionDate, DischargeDate) VALUES (7, 7, TO_DATE('2024-06-30', 'YYYY-MM-DD'), TO_DATE('2024-07-01', 'YYYY-MM-DD'));

-- Insert into Prescriptions
INSERT INTO Prescriptions (PrescriptionID, TreatmentID, PrescriptionDetails) VALUES (1, 1, 'Vitamin D Supplement');
INSERT INTO Prescriptions (PrescriptionID, TreatmentID, PrescriptionDetails) VALUES (2, 2, 'Painkillers');
INSERT INTO Prescriptions (PrescriptionID, TreatmentID, PrescriptionDetails) VALUES (3, 3, 'Paracetamol 500mg');
INSERT INTO Prescriptions (PrescriptionID, TreatmentID, PrescriptionDetails) VALUES (4, 4, 'Ibuprofen');
INSERT INTO Prescriptions (PrescriptionID, TreatmentID, PrescriptionDetails) VALUES (5, 5, 'Antifungal Cream');
INSERT INTO Prescriptions (PrescriptionID, TreatmentID, PrescriptionDetails) VALUES (6, 6, 'Chemotherapy Drugs');
INSERT INTO Prescriptions (PrescriptionID, TreatmentID, PrescriptionDetails) VALUES (7, 7, 'Antacid');
COMMIT;
