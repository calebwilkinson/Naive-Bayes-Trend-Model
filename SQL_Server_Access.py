import pyodbc

def Access_Server():
    server = 'DESKTOP-4A1MPI2\SQLEXPRESS'
    database = 'master'
    username = 'caleb'
    password = 'Wsnoopy811'
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=DESKTOP-4A1MPI2\SQLEXPRESS;"
                          "Database=master;"
                          "Trusted_Connection=yes;")

    cursor = cnxn.cursor()

    return cursor


