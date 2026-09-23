-- TraceMate database (MySQL / MariaDB). Import in phpMyAdmin.
CREATE DATABASE IF NOT EXISTS tracemate CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tracemate;

CREATE TABLE users (
  user_id       INT AUTO_INCREMENT PRIMARY KEY,
  name          VARCHAR(100) NOT NULL,
  email         VARCHAR(150) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role          ENUM('specialist','parent') NOT NULL,
  created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE students (
  student_id        INT AUTO_INCREMENT PRIMARY KEY,
  name              VARCHAR(100) NOT NULL,
  parent_id         INT NOT NULL,
  specialist_id     INT NOT NULL,
  baseline_accuracy DECIMAL(5,2) NULL,
  FOREIGN KEY (parent_id)     REFERENCES users(user_id),
  FOREIGN KEY (specialist_id) REFERENCES users(user_id)
);

CREATE TABLE devices (
  device_id  INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL UNIQUE,
  api_key    VARCHAR(64) NOT NULL UNIQUE,
  last_sync  DATETIME NULL,
  FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE letter_templates (
  template_id  INT AUTO_INCREMENT PRIMARY KEY,
  letter       VARCHAR(5)  NOT NULL,
  name         VARCHAR(30) NOT NULL UNIQUE,
  strokes_json JSON NOT NULL,
  tolerance    DECIMAL(4,3) NOT NULL DEFAULT 0.050
);

CREATE TABLE sessions (
  session_id     INT AUTO_INCREMENT PRIMARY KEY,
  student_id     INT NOT NULL,
  specialist_id  INT NOT NULL,
  scheduled_date DATE NOT NULL,
  status         ENUM('scheduled','in_progress','completed') NOT NULL DEFAULT 'scheduled',
  FOREIGN KEY (student_id)    REFERENCES students(student_id),
  FOREIGN KEY (specialist_id) REFERENCES users(user_id)
);

CREATE TABLE session_letters (
  session_id  INT NOT NULL,
  position    TINYINT NOT NULL,
  template_id INT NOT NULL,
  PRIMARY KEY (session_id, position),
  FOREIGN KEY (session_id)  REFERENCES sessions(session_id) ON DELETE CASCADE,
  FOREIGN KEY (template_id) REFERENCES letter_templates(template_id)
);

CREATE TABLE attempts (
  attempt_id  INT AUTO_INCREMENT PRIMARY KEY,
  session_id  INT NOT NULL,
  template_id INT NOT NULL,
  attempt_no  TINYINT NOT NULL,
  score       DECIMAL(5,2) NOT NULL,
  passed      BOOLEAN NOT NULL,
  points_json JSON NULL,
  created_at  DATETIME NOT NULL,
  FOREIGN KEY (session_id)  REFERENCES sessions(session_id),
  FOREIGN KEY (template_id) REFERENCES letter_templates(template_id)
);

CREATE TABLE alerts (
  alert_id   INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  reason     VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_read    BOOLEAN NOT NULL DEFAULT FALSE,
  FOREIGN KEY (student_id) REFERENCES students(student_id)
);
