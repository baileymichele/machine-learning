# -*- coding: utf-8 -*-
import csv
import numpy as np
import pandas as pd
import sqlite3 as sql

def relationships():
    """
    Specify relationships between columns in given sql tables.
    """
    print "One-to-one relationships:"
    # Put print statements specifying one-to-one relationships between table
    # columns.
    print "5.1 StudentID to Name"
    print "5.1 StudentID to MajorCode"
    print "5.1 StudentID to MinorCode"
    print "5.1 Name to StudentID"
    print "5.1 Name to MajorCode"
    print "5.1 Name to MinorCode"
    print "5.2 ID to Name"
    print "5.2 Name to ID"
    print "5.4 ClassID to Name"
    print "5.4 Name to ClassID"

    print "**************************"
    print "One-to-many relationships:"
    # Put print statements specifying one-to-many relationships between table
    # columns.
    print "5.1 MajorCode to StudentID"
    print "5.1 MajorCode to Name"
    print "5.1 MajorCode to MinorCode"
    print "5.1 MinorCode to StudentID"
    print "5.1 MinorCode to Name"
    print "5.1 MinorCode to MinorCode"


    print "***************************"
    print "Many-to-Many relationships:"
    # Put print statements specifying many-to-many relationships between table
    # columns.
    print "5.3 StudentID to ClassID"
    print "5.3 StudentID to Grade"

def query1():
    """
    SQL query that will output how many students belong to each major,
    including students who don't have a major.

    Return: A table indicating how many students belong to each major.
    """
    #Build your tables and/or query here
    db = sql.connect("sql3")
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS students;")
    cur.execute("DROP TABLE IF EXISTS fields;")
    cur.execute("DROP TABLE IF EXISTS grades;")
    cur.execute("DROP TABLE IF EXISTS classes;")

    cur.execute('CREATE TABLE students (StudentID INTEGER NOT NULL, Name TEXT, MajorCode INTEGER, MinorCode INTEGER);')
    cur.execute('CREATE TABLE fields (ID INTEGER NOT NULL, Name TEXT);')
    cur.execute('CREATE TABLE grades (StudentID INTEGER NOT NULL, ClassID INTEGER NOT NULL, Grade TEXT);')
    cur.execute('CREATE TABLE classes (ClassID INTEGER NOT NULL, Name TEXT);')

    with open('students.csv', 'rb') as csvfile:
        students = [row for row in csv.reader(csvfile, delimiter=',')]
    with open('fields.csv', 'rb') as csvfile:
        fields = [row for row in csv.reader(csvfile, delimiter=',')]
    with open('grades.csv', 'rb') as csvfile:
        grades = [row for row in csv.reader(csvfile, delimiter=',')]
    with open('classes.csv', 'rb') as csvfile:
        classes = [row for row in csv.reader(csvfile, delimiter=',')]

    cur.executemany("INSERT INTO students VALUES (?, ?, ?, ?);", students)
    cur.executemany("INSERT INTO fields VALUES (?, ?);", fields)
    cur.executemany("INSERT INTO grades VALUES (?, ?, ?);", grades)
    cur.executemany("INSERT INTO classes VALUES (?, ?);", classes)

    query = 'SELECT fields.Name, COUNT(StudentID) FROM students LEFT OUTER JOIN fields ON students.MajorCode=fields.ID GROUP BY fields.Name;'


    # This line will make a pretty table with the results of your query.
        ### query is a string containing your sql query
        ### db is a sql database connection
    result =  pd.read_sql_query(query, db)

    db.commit()
    db.close()
    return result


def query2():
    """
    Select students who received two or more non-Null grades in their classes.

    Return: A table of the students' names and the grades each received.
    """
    #Build your tables and/or query here
    db = sql.connect("sql3")
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS students;")
    cur.execute("DROP TABLE IF EXISTS fields;")
    cur.execute("DROP TABLE IF EXISTS grades;")
    cur.execute("DROP TABLE IF EXISTS classes;")

    cur.execute('CREATE TABLE students (StudentID INTEGER NOT NULL, Name TEXT, MajorCode INTEGER, MinorCode INTEGER);')
    cur.execute('CREATE TABLE fields (ID INTEGER NOT NULL, Name TEXT);')
    cur.execute('CREATE TABLE grades (StudentID INTEGER NOT NULL, ClassID INTEGER NOT NULL, Grade TEXT);')
    cur.execute('CREATE TABLE classes (ClassID INTEGER NOT NULL, Name TEXT);')

    with open('students.csv', 'rb') as csvfile:
        students = [row for row in csv.reader(csvfile, delimiter=',')]
    with open('fields.csv', 'rb') as csvfile:
        fields = [row for row in csv.reader(csvfile, delimiter=',')]
    with open('grades.csv', 'rb') as csvfile:
        grades = [row for row in csv.reader(csvfile, delimiter=',')]
    with open('classes.csv', 'rb') as csvfile:
        classes = [row for row in csv.reader(csvfile, delimiter=',')]

    cur.executemany("INSERT INTO students VALUES (?, ?, ?, ?);", students)
    cur.executemany("INSERT INTO fields VALUES (?, ?);", fields)
    cur.executemany("INSERT INTO grades VALUES (?, ?, ?);", grades)
    cur.executemany("INSERT INTO classes VALUES (?, ?);", classes)

    # query = 'SELECT grades.StudentID, COUNT(StudentID) FROM grades JOIN students.StudentID=grades.StudentID'
    query = 'SELECT students.Name, COUNT(*) FROM grades LEFT OUTER JOIN students ON students.StudentID=grades.StudentID WHERE grades.Grade!="NULL" GROUP BY students.Name HAVING COUNT(*)>2'

    # This line will make a pretty table with the results of your query.
        ### query is a string containing your sql query
        ### db is a sql database connection
    result =  pd.read_sql_query(query, db)

    db.commit()
    db.close()
    return result


def query3():
    """
    Get the average GPA at the school using the given tables.

    Return: A float representing the average GPA, rounded to 2 decimal places.
    """
    db = sql.connect("sql3")
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS students;")
    cur.execute("DROP TABLE IF EXISTS fields;")
    cur.execute("DROP TABLE IF EXISTS grades;")
    cur.execute("DROP TABLE IF EXISTS classes;")

    cur.execute('CREATE TABLE students (StudentID INTEGER NOT NULL, Name TEXT, MajorCode INTEGER, MinorCode INTEGER);')
    cur.execute('CREATE TABLE fields (ID INTEGER NOT NULL, Name TEXT);')
    cur.execute('CREATE TABLE grades (StudentID INTEGER NOT NULL, ClassID INTEGER NOT NULL, Grade TEXT);')
    cur.execute('CREATE TABLE classes (ClassID INTEGER NOT NULL, Name TEXT);')

    with open('students.csv', 'rb') as csvfile:
        students = [row for row in csv.reader(csvfile, delimiter=',')]
    with open('fields.csv', 'rb') as csvfile:
        fields = [row for row in csv.reader(csvfile, delimiter=',')]
    with open('grades.csv', 'rb') as csvfile:
        grades = [row for row in csv.reader(csvfile, delimiter=',')]
    with open('classes.csv', 'rb') as csvfile:
        classes = [row for row in csv.reader(csvfile, delimiter=',')]

    cur.executemany("INSERT INTO students VALUES (?, ?, ?, ?);", students)
    cur.executemany("INSERT INTO fields VALUES (?, ?);", fields)
    cur.executemany("INSERT INTO grades VALUES (?, ?, ?);", grades)
    cur.executemany("INSERT INTO classes VALUES (?, ?);", classes)

    query = "SELECT ROUND(AVG( \
    CASE Grade \
        WHEN 'A' THEN 4.0\
        WHEN 'A-' THEN 4.0\
        WHEN 'A+' THEN 4.0\
        WHEN 'B' THEN 3.0\
        WHEN 'B-' THEN 3.0\
        WHEN 'B+' THEN 3.0\
        WHEN 'C' THEN 2.0\
        WHEN 'C-' THEN 2.0\
        WHEN 'C+' THEN 2.0\
        WHEN 'D-' THEN 1.0\
        WHEN 'D+' THEN 1.0\
        WHEN 'D' THEN 1.0\
        END),2) \
    FROM grades;"

    result =  np.array(pd.read_sql_query(query, db))

    db.commit()
    db.close()
    return result[0][0]

def query4():
    """
    Find all students whose last name begins with 'C' and their majors.

    Return: A table containing the names of the students and their majors.
    """
    #Build your tables and/or query here
    db = sql.connect("sql3")
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS students;")
    cur.execute("DROP TABLE IF EXISTS fields;")
    cur.execute("DROP TABLE IF EXISTS grades;")
    cur.execute("DROP TABLE IF EXISTS classes;")

    cur.execute('CREATE TABLE students (StudentID INTEGER NOT NULL, Name TEXT, MajorCode INTEGER, MinorCode INTEGER);')
    cur.execute('CREATE TABLE fields (ID INTEGER NOT NULL, Name TEXT);')
    cur.execute('CREATE TABLE grades (StudentID INTEGER NOT NULL, ClassID INTEGER NOT NULL, Grade TEXT);')
    cur.execute('CREATE TABLE classes (ClassID INTEGER NOT NULL, Name TEXT);')

    with open('students.csv', 'rb') as csvfile:
        students = [row for row in csv.reader(csvfile, delimiter=',')]
    with open('fields.csv', 'rb') as csvfile:
        fields = [row for row in csv.reader(csvfile, delimiter=',')]
    with open('grades.csv', 'rb') as csvfile:
        grades = [row for row in csv.reader(csvfile, delimiter=',')]
    with open('classes.csv', 'rb') as csvfile:
        classes = [row for row in csv.reader(csvfile, delimiter=',')]

    cur.executemany("INSERT INTO students VALUES (?, ?, ?, ?);", students)
    cur.executemany("INSERT INTO fields VALUES (?, ?);", fields)
    cur.executemany("INSERT INTO grades VALUES (?, ?, ?);", grades)
    cur.executemany("INSERT INTO classes VALUES (?, ?);", classes)

    query = 'SELECT students.Name, fields.Name FROM students LEFT OUTER JOIN fields ON students.MajorCode=fields.ID WHERE students.Name LIKE "% C%";'

    # This line will make a pretty table with the results of your query.
        ### query is a string containing your sql query
        ### db is a sql database connection
    result =  pd.read_sql_query(query, db)

    db.commit()
    db.close()
    return result

if __name__ == '__main__':
    print relationships()
    print query1()
    print query2()
    print query3()
    print query4()
