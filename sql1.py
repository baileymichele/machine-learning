import csv
import numpy as np
import pandas as pd
import sqlite3 as sql

def create_tables():
    """
    Creates the following SQL tables with the following columns:
        -- MajorInfo: MajorID (int), MajorName (string)
        -- CourseInfo: CourseID (int), CourseName (string)
    --------------------------------------------------------------
    Do not return anything.  Just create the designated tables.
    """
    db = sql.connect("sql1")
    cur = db.cursor()

    cur.execute("DROP TABLE IF EXISTS MajorInfo;")
    cur.execute("DROP TABLE IF EXISTS CourseInfo;")

    cur.execute('CREATE TABLE MajorInfo (MajorID INTEGER NOT NULL, MajorName TEXT);')
    cur.execute('CREATE TABLE CourseInfo (CourseID INTEGER NOT NULL, CourseName TEXT);')
    # cur.execute("PRAGMA table_info('CourseInfo')")
    # for info in cur:
    #     print info
    db.commit()
    db.close()

def create_tables2():
    """
    Creates the following SQL table with the following columns:
        -- ICD: ID_Number (int), Gender (string), Age (int) ICD_Code (string)
    --------------------------------------------------------------
    Do not return anything.  Just create the designated table.
    """
    db = sql.connect("sql2")
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS ICD;")
    cur.execute('CREATE TABLE ICD (ID_Number INTEGER NOT NULL, Gender TEXT, Age INTEGER NOT NULL, ICD_Code TEXT);')

    with open('icd9.csv', 'rb') as csvfile:
        rows = [row for row in csv.reader(csvfile, delimiter=',')]
    cur.executemany("INSERT INTO ICD VALUES (?, ?, ?, ?);", rows)
    # cur.execute("PRAGMA table_info('ICD')")
    # for info in cur:
    #     print info

    db.commit()
    db.close()

def create_tables3():
    """
    Creates the following SQL tables with the following columns:
        -- StudentInformation: StudentID (int), Name (string), MajorCode (int)
        -- StudentGrades: StudentID (int), ClassID (int), Grade (int)

    Populates these tables, as well as the tables from first function, with
        the necesary information.  Also, uses the column names for
        MajorInfo and CourseInfo given in func 1, NOT the column
        names given in func 2.
    ------------------------------------------------------------------------
    Do not return anything.  Just create the designated tables.
    """
    db = sql.connect("sql1")
    cur = db.cursor()

    cur.execute("DROP TABLE IF EXISTS MajorInfo;")
    cur.execute("DROP TABLE IF EXISTS CourseInfo;")
    cur.execute("DROP TABLE IF EXISTS StudentInformation;")
    cur.execute("DROP TABLE IF EXISTS StudentGrades;")

    cur.execute('CREATE TABLE MajorInfo (MajorID INTEGER NOT NULL, MajorName TEXT);')
    cur.execute('CREATE TABLE CourseInfo (CourseID INTEGER NOT NULL, CourseName TEXT);')
    cur.execute('CREATE TABLE StudentInformation (StudentID INTEGER NOT NULL, Name TEXT, MajorCode INTEGER NOT NULL);')
    cur.execute('CREATE TABLE StudentGrades (StudentID INTEGER NOT NULL, ClassID INTEGER NOT NULL, Grade INTEGER NOT NULL);')

    with open('major_info.csv', 'rb') as csvfile:
        major = [row for row in csv.reader(csvfile, delimiter=',')]
    with open('course_info.csv', 'rb') as csvfile:
        course = [row for row in csv.reader(csvfile, delimiter=',')]
    with open('student_info.csv', 'rb') as csvfile:
        studentInfo = [row for row in csv.reader(csvfile, delimiter=',')]
    with open('student_grades.csv', 'rb') as csvfile:
        studentGrade = [row for row in csv.reader(csvfile, delimiter=',')]

    cur.executemany("INSERT INTO MajorInfo VALUES (?, ?);", major)
    cur.executemany("INSERT INTO CourseInfo VALUES (?, ?);", course)
    cur.executemany("INSERT INTO StudentInformation VALUES (?, ?, ?);", studentInfo)
    cur.executemany("INSERT INTO StudentGrades VALUES (?, ?, ?);", studentGrade)

    # useful_test_function(db, 'SELECT * FROM MajorInfo')
    # useful_test_function(db, 'SELECT * FROM CourseInfo')
    # useful_test_function(db, 'SELECT * FROM StudentInformation')
    # useful_test_function(db, 'SELECT * FROM StudentGrades')

    # cur.execute('SELECT COUNT(*) StudentID, Name FROM StudentInformation WHERE MajorCode=1;')

    db.commit()
    db.close()

def query():
    """
    Finds the number of men and women, respectively, between ages 25 and 35
    (inclusive).
    ------------------------------------------------------------------------
    Returns:
        (n_men, n_women): A tuple containing number of men and number of women
                            (in that order)
    """
    db = sql.connect("sql2")
    cur = db.cursor()

    Male = 'SELECT COUNT(*) FROM ICD WHERE Gender="M" AND Age>=25 AND Age<=35;'
    Female = 'SELECT COUNT(*) FROM ICD WHERE Gender="F" AND Age>=25 AND Age<=35;'

    one = pd.read_sql_query(Male, db)
    two = pd.read_sql_query(Female, db)

    db.commit()
    db.close()

    one2 = np.array(one)
    two2 = np.array(two)
    return (one2[0][0],two2[0][0])

def useful_test_function(db, query):
    """
    Print out the results of a query in a nice format using pandas
    ------------------------------------------------------------------------
    Inputs:
        db: A sqlite3 database connection
        query: A string containing the SQL query you want to execute
    """
    print pd.read_sql_query(query, db)

