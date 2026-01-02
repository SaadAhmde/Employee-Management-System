# Employee-Management-System
# Employee Management System (Python + Tkinter + MySQL)

This is a desktop-based Employee Management System built using Python, Tkinter, and MySQL.

## Features
- Add employee
- Update employee
- Delete employee
- Search employee by ID or Name
- View all employees

## Technologies Used
- Python
- Tkinter (GUI)
- MySQL
- PyMySQL

## Database Schema

```sql
CREATE DATABASE emp_db;
USE emp_db;

CREATE TABLE emp (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    designation VARCHAR(50),
    gender VARCHAR(50),
    address VARCHAR(50)
);

CREATE TABLE salary (
    emp_id INT PRIMARY KEY,
    salary INT,
    FOREIGN KEY (emp_id) REFERENCES emp(id)
);
