-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS feedback_system;
USE feedback_system;

-- Create students table
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create admins table
CREATE TABLE IF NOT EXISTS admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create courses table
CREATE TABLE IF NOT EXISTS courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    faculty_name VARCHAR(255) NOT NULL
);

-- Create feedback table
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_student FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_course FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    UNIQUE KEY unique_feedback (student_id, course_id)
);

-- Insert example courses (if table is empty)
INSERT INTO courses (course_name, faculty_name)
SELECT * FROM (SELECT 'Data Structures', 'Dr. A') AS tmp
WHERE NOT EXISTS (
    SELECT course_id FROM courses WHERE course_name = 'Data Structures' AND faculty_name = 'Dr. A'
)
LIMIT 1;

INSERT INTO courses (course_name, faculty_name)
SELECT * FROM (SELECT 'Digital Electronics', 'Prof. B') AS tmp
WHERE NOT EXISTS (
    SELECT course_id FROM courses WHERE course_name = 'Digital Electronics' AND faculty_name = 'Prof. B'
)
LIMIT 1;

-- Insert default admin (you should hash passwords in production!)
INSERT INTO admins (username, password)
SELECT * FROM (SELECT 'admin', 'adminpass') AS tmp
WHERE NOT EXISTS (
    SELECT admin_id FROM admins WHERE username = 'admin'
)
LIMIT 1;
