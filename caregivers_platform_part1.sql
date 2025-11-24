DROP TABLE IF EXISTS JOB_APPLICATION CASCADE;
DROP TABLE IF EXISTS APPOINTMENT CASCADE;
DROP TABLE IF EXISTS JOB CASCADE;
DROP TABLE IF EXISTS ADDRESS CASCADE;
DROP TABLE IF EXISTS MEMBER CASCADE;
DROP TABLE IF EXISTS CAREGIVER CASCADE;
DROP TABLE IF EXISTS "USER" CASCADE;

CREATE TABLE "USER" (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    given_name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    profile_description TEXT,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE CAREGIVER (
    caregiver_user_id INTEGER PRIMARY KEY,
    photo VARCHAR(500),
    gender VARCHAR(20) NOT NULL,
    caregiving_type VARCHAR(50) NOT NULL,
    hourly_rate DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (caregiver_user_id) REFERENCES "USER"(user_id) ON DELETE CASCADE
);

CREATE TABLE MEMBER (
    member_user_id INTEGER PRIMARY KEY,
    house_rules TEXT,
    dependent_description TEXT,
    FOREIGN KEY (member_user_id) REFERENCES "USER"(user_id) ON DELETE CASCADE
);

CREATE TABLE ADDRESS (
    member_user_id INTEGER PRIMARY KEY,
    house_number VARCHAR(20) NOT NULL,
    street VARCHAR(200) NOT NULL,
    town VARCHAR(100) NOT NULL,
    FOREIGN KEY (member_user_id) REFERENCES MEMBER(member_user_id) ON DELETE CASCADE
);

CREATE TABLE JOB (
    job_id SERIAL PRIMARY KEY,
    member_user_id INTEGER NOT NULL,
    required_caregiving_type VARCHAR(50) NOT NULL,
    other_requirements TEXT,
    date_posted DATE NOT NULL,
    FOREIGN KEY (member_user_id) REFERENCES MEMBER(member_user_id) ON DELETE CASCADE
);

CREATE TABLE JOB_APPLICATION (
    caregiver_user_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    date_applied DATE NOT NULL,
    PRIMARY KEY (caregiver_user_id, job_id),
    FOREIGN KEY (caregiver_user_id) REFERENCES CAREGIVER(caregiver_user_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES JOB(job_id) ON DELETE CASCADE
);

CREATE TABLE APPOINTMENT (
    appointment_id SERIAL PRIMARY KEY,
    caregiver_user_id INTEGER NOT NULL,
    member_user_id INTEGER NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    work_hours INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'accepted', 'declined', 'completed')),
    FOREIGN KEY (caregiver_user_id) REFERENCES CAREGIVER(caregiver_user_id) ON DELETE CASCADE,
    FOREIGN KEY (member_user_id) REFERENCES MEMBER(member_user_id) ON DELETE CASCADE
);

INSERT INTO "USER" (email, given_name, surname, city, phone_number, profile_description, password) VALUES
('arman.armanov@example.com', 'Arman', 'Armanov', 'Astana', '+77771234567', 'Experienced babysitter with 5 years of experience. Love working with children.', 'password123'),
('sara.sarikova@example.com', 'Sara', 'Sarikova', 'Astana', '+77771234568', 'Professional elderly caregiver. Certified nurse with gentle approach.', 'password123'),
('dana.dankova@example.com', 'Dana', 'Dankova', 'Almaty', '+77771234569', 'Energetic playmate for children. Arts and crafts specialist.', 'password123'),
('murat.muratov@example.com', 'Murat', 'Muratov', 'Astana', '+77771234570', 'Patient elderly caregiver with medical background.', 'password123'),
('aisha.aishanova@example.com', 'Aisha', 'Aishanova', 'Almaty', '+77771234571', 'Loving babysitter. Early childhood education degree.', 'password123'),
('nurzhan.nurzhanuly@example.com', 'Nurzhan', 'Nurzhanuly', 'Astana', '+77771234572', 'Playmate for children. Sports and outdoor activities enthusiast.', 'password123'),
('gulmira.gulmirova@example.com', 'Gulmira', 'Gulmirova', 'Shymkent', '+77771234573', 'Experienced elderly caregiver. Soft-spoken and compassionate.', 'password123'),
('yerlan.yerlanov@example.com', 'Yerlan', 'Yerlanov', 'Astana', '+77771234574', 'Professional babysitter. CPR certified.', 'password123'),
('azamat.azamatov@example.com', 'Azamat', 'Azamatov', 'Almaty', '+77771234575', 'Elderly care specialist with 10 years experience.', 'password123'),
('madina.madinova@example.com', 'Madina', 'Madinova', 'Astana', '+77771234576', 'Child playmate. Creative and fun activities.', 'password123'),
('amina.aminova@example.com', 'Amina', 'Aminova', 'Astana', '+77779876543', 'Mother of two looking for reliable childcare.', 'password456'),
('kanat.kanatov@example.com', 'Kanat', 'Kanatov', 'Astana', '+77779876544', 'Need elderly care for my mother.', 'password456'),
('laura.laurova@example.com', 'Laura', 'Laurova', 'Almaty', '+77779876545', 'Looking for weekend babysitter.', 'password456'),
('timur.timurov@example.com', 'Timur', 'Timurov', 'Astana', '+77779876546', 'Seeking elderly caregiver for father.', 'password456'),
('diana.dianova@example.com', 'Diana', 'Dianova', 'Shymkent', '+77779876547', 'Need playmate for 6-year-old son.', 'password456'),
('asset.assetov@example.com', 'Asset', 'Assetov', 'Astana', '+77779876548', 'Looking for after-school care.', 'password456'),
('zhanna.zhannova@example.com', 'Zhanna', 'Zhannova', 'Almaty', '+77779876549', 'Need elderly care specialist.', 'password456'),
('bolat.bolatov@example.com', 'Bolat', 'Bolatov', 'Astana', '+77779876550', 'Seeking babysitter for infant.', 'password456'),
('aida.aidanova@example.com', 'Aida', 'Aidanova', 'Astana', '+77779876551', 'Looking for elderly caregiver.', 'password456'),
('ruslan.ruslanov@example.com', 'Ruslan', 'Ruslanov', 'Almaty', '+77779876552', 'Need childcare for toddler.', 'password456');

INSERT INTO CAREGIVER (caregiver_user_id, photo, gender, caregiving_type, hourly_rate) VALUES
(1, 'https://example.com/photos/arman.jpg', 'Male', 'Babysitter', 8.50),
(2, 'https://example.com/photos/sara.jpg', 'Female', 'Elderly Care', 12.00),
(3, 'https://example.com/photos/dana.jpg', 'Female', 'Playmate', 7.00),
(4, 'https://example.com/photos/murat.jpg', 'Male', 'Elderly Care', 11.50),
(5, 'https://example.com/photos/aisha.jpg', 'Female', 'Babysitter', 9.00),
(6, 'https://example.com/photos/nurzhan.jpg', 'Male', 'Playmate', 8.00),
(7, 'https://example.com/photos/gulmira.jpg', 'Female', 'Elderly Care', 10.50),
(8, 'https://example.com/photos/yerlan.jpg', 'Male', 'Babysitter', 9.50),
(9, 'https://example.com/photos/azamat.jpg', 'Male', 'Elderly Care', 13.00),
(10, 'https://example.com/photos/madina.jpg', 'Female', 'Playmate', 7.50);

INSERT INTO MEMBER (member_user_id, house_rules, dependent_description) VALUES
(11, 'No smoking. Please remove shoes at entrance.', 'I have a 5-year-old daughter who loves painting and drawing.'),
(12, 'No pets. Punctuality is important.', 'My 78-year-old mother needs assistance with daily activities.'),
(13, 'Please be punctual. No phone use during work.', 'Twin boys aged 3, very active and energetic.'),
(14, 'No pets. Quiet environment preferred.', 'Father, 82 years old, needs gentle elderly care.'),
(15, 'Clean environment important. No smoking.', '6-year-old son who enjoys outdoor activities and sports.'),
(16, 'No smoking. Healthy meals only.', '8-year-old daughter needs help with homework.'),
(17, 'No pets. Experience with dementia required.', 'Mother, 75, with early-stage dementia.'),
(18, 'Sterile environment. Medical knowledge preferred.', '6-month-old infant, first-time parents.'),
(19, 'No pets. Patient and soft-spoken caregiver needed.', 'Grandmother, 80, recovering from surgery.'),
(20, 'No allergies. Organic food only.', '2-year-old toddler with food allergies.');

INSERT INTO ADDRESS (member_user_id, house_number, street, town) VALUES
(11, '45', 'Kabanbay Batyr', 'Esil District'),
(12, '12', 'Respublika Avenue', 'Saryarka District'),
(13, '78', 'Mangilik El', 'Esil District'),
(14, '23', 'Kabanbay Batyr', 'Almaty District'),
(15, '56', 'Turan Avenue', 'Saryarka District'),
(16, '34', 'Dostyk Street', 'Esil District'),
(17, '89', 'Abay Avenue', 'Saryarka District'),
(18, '67', 'Kabanbay Batyr', 'Esil District'),
(19, '15', 'Kenesary Street', 'Almaty District'),
(20, '90', 'Samal Street', 'Esil District');

INSERT INTO JOB (member_user_id, required_caregiving_type, other_requirements, date_posted) VALUES
(11, 'Babysitter', 'Must be patient and creative. Experience with arts and crafts preferred.', '2024-11-01'),
(12, 'Elderly Care', 'Should be soft-spoken and gentle. Medical background required.', '2024-11-02'),
(13, 'Playmate', 'High energy required. Experience with multiple children.', '2024-11-03'),
(14, 'Elderly Care', 'Patient and caring. No pets. Experience with mobility issues.', '2024-11-04'),
(15, 'Playmate', 'Outdoor activities enthusiast. Sports background preferred.', '2024-11-05'),
(16, 'Babysitter', 'Help with homework. Tutoring experience a plus.', '2024-11-06'),
(17, 'Elderly Care', 'Experience with dementia patients. Soft-spoken and patient.', '2024-11-07'),
(18, 'Babysitter', 'Infant care experience required. CPR certified.', '2024-11-08'),
(19, 'Elderly Care', 'Post-surgery care. Medical knowledge required. Must be soft-spoken.', '2024-11-09'),
(20, 'Babysitter', 'Knowledge of food allergies. Experience with toddlers.', '2024-11-10');

INSERT INTO JOB_APPLICATION (caregiver_user_id, job_id, date_applied) VALUES
(1, 1, '2024-11-02'),
(5, 1, '2024-11-03'),
(8, 1, '2024-11-04'),
(2, 2, '2024-11-03'),
(4, 2, '2024-11-04'),
(3, 3, '2024-11-04'),
(6, 3, '2024-11-05'),
(10, 3, '2024-11-05'),
(2, 4, '2024-11-05'),
(4, 4, '2024-11-06'),
(9, 4, '2024-11-06'),
(6, 5, '2024-11-06'),
(10, 5, '2024-11-07'),
(1, 6, '2024-11-07'),
(5, 6, '2024-11-08'),
(7, 7, '2024-11-08'),
(9, 7, '2024-11-09'),
(8, 8, '2024-11-09'),
(7, 9, '2024-11-10'),
(2, 9, '2024-11-11');

INSERT INTO APPOINTMENT (caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status) VALUES
(1, 11, '2024-11-15', '09:00:00', 4, 'accepted'),
(2, 12, '2024-11-16', '10:00:00', 6, 'accepted'),
(3, 13, '2024-11-17', '14:00:00', 3, 'accepted'),
(4, 14, '2024-11-18', '08:00:00', 8, 'accepted'),
(5, 15, '2024-11-19', '15:00:00', 2, 'pending'),
(6, 16, '2024-11-20', '16:00:00', 3, 'accepted'),
(7, 17, '2024-11-21', '09:00:00', 5, 'accepted'),
(8, 18, '2024-11-22', '11:00:00', 4, 'declined'),
(9, 19, '2024-11-23', '10:00:00', 6, 'accepted'),
(10, 20, '2024-11-24', '13:00:00', 2, 'accepted');

SELECT 'USER' as table_name, COUNT(*) as record_count FROM "USER"
UNION ALL
SELECT 'CAREGIVER', COUNT(*) FROM CAREGIVER
UNION ALL
SELECT 'MEMBER', COUNT(*) FROM MEMBER
UNION ALL
SELECT 'ADDRESS', COUNT(*) FROM ADDRESS
UNION ALL
SELECT 'JOB', COUNT(*) FROM JOB
UNION ALL
SELECT 'JOB_APPLICATION', COUNT(*) FROM JOB_APPLICATION
UNION ALL
SELECT 'APPOINTMENT', COUNT(*) FROM APPOINTMENT;

SELECT '=== Verification for Part 2 Queries ===' as info;

SELECT 'Arman Armanov found:', given_name, surname, phone_number 
FROM "USER" 
WHERE given_name = 'Arman' AND surname = 'Armanov';

SELECT 'Amina Aminova found:', given_name, surname 
FROM "USER" 
WHERE given_name = 'Amina' AND surname = 'Aminova';

SELECT 'Kabanbay Batyr addresses:', COUNT(*) 
FROM ADDRESS 
WHERE street = 'Kabanbay Batyr';

SELECT 'Jobs with soft-spoken:', COUNT(*) 
FROM JOB 
WHERE other_requirements ILIKE '%soft-spoken%';

SELECT 'Astana Elderly Care (No pets):', COUNT(*) 
FROM MEMBER m
JOIN "USER" u ON m.member_user_id = u.user_id
JOIN JOB j ON m.member_user_id = j.member_user_id
WHERE u.city = 'Astana' 
AND j.required_caregiving_type = 'Elderly Care'
AND m.house_rules ILIKE '%No pets%';

SELECT 'Accepted appointments:', COUNT(*) 
FROM APPOINTMENT 
WHERE status = 'accepted';

SELECT 'Babysitter appointments:', COUNT(*)
FROM APPOINTMENT a
JOIN CAREGIVER c ON a.caregiver_user_id = c.caregiver_user_id
WHERE c.caregiving_type = 'Babysitter';

SELECT '=== Database setup complete! ===' as info;
