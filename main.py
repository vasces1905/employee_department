import sqlite3
from unittest import result
import pandas as pd

DEPARTMENT_CSV = './departmentdata.csv'
EMPDATA_CSV = './empdata.csv'


# Define DBOperation class to manage all data into the database.
# Give a name of your choice to the database

class DBOperations:
    sql_create_table_firsttime = "DROP TABLE IF EXISTS Employees"
    sql_create_table_firsttime = "DROP TABLE IF EXISTS Department"

    # "create table if not exists "
    conn = sqlite3.connect ( 'company.db' )
    print ( "Database has been prepared for creation" )

    # Menu-1: Prepare the craeation of the table with this variable - Employees table
    sql_create_table1 = "CREATE TABLE Employees (Employee_Id INTEGER PRIMARY KEY, EmployeeName VARCHAR(30), Surname VARCHAR(40), EmployeeTitle VARCHAR(40),  UserName VARCHAR(30), Email VARCHAR(50), EmployeeSalary INTEGER, BirthDate DATE, Gender VARCHAR(5),Password VARCHAR(25))"
    print ( "Employees table has been prepared successfully" )

    # Menu-1: Prepare the craeation of the table with this variable - Department table
    sql_create_table2 = "CREATE TABLE Department (User_Id INTEGER PRIMARY KEY, DepartmentName VARCHAR(30), Location VARCHAR(20), Country VARCHAR(20), FOREIGN KEY(User_Id) REFERENCES Employees(Employee_Id))"
    print ( "Department table has been prepared successfully" )

    # Menu-2: Insert related values with these fields for Employees table
    sql_emp_insert = "INSERT INTO Employees (Employee_Id,EmployeeName,Surname,EmployeeTitle,UserName,Email,EmployeeSalary,BirthDate,Gender,Password)VALUES (?,?,?,?,?,?,?,?,?,?)"
    sql_dep_insert = "INSERT INTO Department (User_Id,DepartmentName,Location,Country)VALUES (?,?,?,?)"
    print ( "Sample department data has been inserted successfully" )

    # Menu-3: Select related values with these fields for Department table for all data
    sql_select_all_emp = "SELECT Employees.Employee_Id, Employees.UserName, Department.DepartmentName from Employees, Department WHERE Department.User_Id = Employees.Employee_Id"

    # Menu-4: Select related values with these fields for Department and Employees table for specific data
    sql_search = "SELECT Employee_Id, EmployeeName, Surname, EmployeeTitle, Email, EmployeeSalary, Gender from Employees where Employee_Id = ?"
    sql_search2 = "SELECT * from Employees where Employee_Id = ?"

    # Menu-5: Select related values with these fields for Department table for specific data
    sql_update_data = "UPDATE Employees SET EmployeeTitle = ?, EmployeeSalary = ?, Password = ? WHERE Employee_Id = ?"

    # Menu-6: Delete all values for Department/Employee table
    sql_delete_data_all_emp = "delete from Employees"
    sql_delete_data_all_dep = "delete from Department"

    sql_drop_table = ""

    def __init__(self):
        try:
            # Connection string to create the db file in sqlite3
            self.conn = sqlite3.connect ( "company.db" )
            self.cur = self.conn.cursor ()
            self.conn.commit ()
        except Exception as e:
            print ( e )
        finally:
            self.conn.close ()

    def get_connection(self):
        self.conn = sqlite3.connect ( "company.db" )
        self.cur = self.conn.cursor ()

    def create_table(self):  # use the variable has been taken from above for create table within this function
        try:
            self.get_connection ()
            self.cur.execute ( "DROP TABLE IF EXISTS Employees" )  # At first drop tables
            self.cur.execute ( "DROP TABLE IF EXISTS Department" )
            self.cur.execute ( self.sql_create_table1 )
            print ( "Employees table has been created successfully" )
            self.cur.execute ( self.sql_create_table2 )
            print ( "Department table has been created successfully" )
            self.conn.commit ()
            print ( "Tables have been created successfully" )
        except Exception as e:
            print ( e )
        finally:
            self.conn.close ()

    def insert_data(self):  # Insert data function - Use input string
        try:
            self.get_connection ()
            employee_id = int ( input ( "Enter your employee id: " ) )
            userID = employee_id
            employeename = str ( input ( "Enter your name: " ) )
            employee_surname = str ( input ( "Enter your surname: " ) )
            departmentname = str ( input ( "Enter your department name: " ) )
            employeeTitle = str ( input ( "Enter your title: " ) )
            employee_username = str ( input ( "Enter your username: " ) )
            Email = str ( input ( "Enter your Email Address: " ) )
            Salary = str ( input ( "Enter the Salary: " ) )
            Gender = str ( input ( "Male/Female: " ) )
            Password = str ( input ( "Enter your password: " ) )

            emp = Employee ( employeeID=employee_id, employeename=employeename, surname=employee_surname,
                             employeeTitle=employeeTitle, username=employee_username, email=Email, salary=Salary,
                             date='', gender=Gender, password=Password )
            dep = Department ( userID, departmentname, '', '' )
            self.cur.execute ( self.sql_emp_insert, emp.insert_statement () )
            self.cur.execute ( self.sql_dep_insert, dep.insert_statement () )
            self.conn.commit ()
            print ( "Related data inserted successfully" )
        except Exception as e:
            print ( e )
        finally:
            self.conn.close ()

    # use the variable has been taken from above for insert csv data into the table with this function
    def insert_from_csv(self):
        try:
            self.get_connection ()

            emp_df = pd.read_csv ( EMPDATA_CSV )  # Read of empdata.csv which is containing employee data.
            emp_df = emp_df.values.tolist ()

            for emp in emp_df[:]:
                emp_new = Employee ( *emp )  # empdata.csv execution process
                self.cur.execute ( self.sql_emp_insert, emp_new.insert_statement () )

            dep_df = pd.read_csv ( DEPARTMENT_CSV )  # Read of department.csv which is containing employee data.
            dep_df = dep_df.values.tolist ()

            for dep in dep_df[:]:
                dep_new = Department ( *dep )
                self.cur.execute ( self.sql_dep_insert, dep_new.insert_statement () )
            self.conn.commit ()
            print ( "Inserted data successfully" )
        except Exception as e:
            print ( e )
        finally:
            self.conn.close ()

    # use the variable has been taken from above for select all data has been imported or added later into the table with this function
    def select_all(self):
        try:
            self.get_connection ()
            self.cur.execute ( self.sql_select_all_emp )
            # self.cur.execute(self.sql_select_all_dep)
            # self.cur.execute("select * from employees")
            result = self.cur.fetchall ()
            print ( result )
            # Department(result[0][0])
            # think how you could develop this method to show the records

        except Exception as e:
            print ( e )
        finally:
            self.conn.close ()

    # use the variable has been taken from above for select specific employee id from the table with this function
    def search_data(self):
        try:
            self.get_connection ()
            Employee_Id = str ( input ( "Enter Employee ID: " ) )
            print ( "The person number", Employee_Id, "detailed as shown below.." )
            # Both execution has been used here to select employees and department data
            self.cur.execute ( self.sql_search, [Employee_Id] )
            self.cur.execute ( self.sql_search2, [Employee_Id] )

            result = self.cur.fetchone ()
            if type ( result ) == type ( tuple () ):
                print ( result )
                for index, detail in enumerate (
                        result ):  # index iteration method : tuple for example between  01-05, 1-20, 2-30"
                    if index == 0:
                        print ( "Employee_Id: " + str ( detail ) )
                    elif index == 1:
                        print ( "Employee Name: " + str ( detail ) )
                    elif index == 2:
                        print ( "Surname: " + str ( detail ) )
                    elif index == 3:
                        print ( "Employee Title: " + str ( detail ) )
                    elif index == 4:
                        print ( "Username: " + str ( detail ) )
                    elif index == 5:
                        print ( "Email address: " + str ( detail ) )
                    elif index == 6:
                        print ( "Salary: " + str ( detail ) )
                    elif index == 7:
                        print ( "Date: " + str ( detail ) )
                    elif index == 8:
                        print ( "Gender: " + str ( detail ) )
                    elif index == 9:
                        print ( "Password: " + str ( detail ) )
                    else:
                        print ( "" )
            else:
                print ( "No Record" )

        except Exception as e:
            print ( e )
        finally:
            self.conn.close ()

    # use the variable has been taken from above for update specific employee id into the table with this function
    def update_data(self):
        try:
            self.get_connection ()
            Employee_Id = str ( input ( "Enter Employee ID: " ) )

            employeeTitle = str ( input ( "Enter your new title: " ) )
            Salary = str ( input ( "Enter the new Salary: " ) )
            Password = str ( input ( "Enter your new password: " ) )

            self.cur.execute ( self.sql_update_data, [employeeTitle, Salary, Password, Employee_Id] )
            # result = self.cur.fetchone ()
            self.conn.commit ()
            print ( "The person number", Employee_Id, "updated" )
        except Exception as e:
            print ( e )
        finally:
            self.conn.close ()

    # use the variable has been taken from above to delete specific employee id from the table with this function
    def delete_data(self):
        try:
            self.get_connection ()
            d_employee_id = str ( input ( "Enter your employee id: " ) )
            sql_delete_data = "delete from Employees where Employee_Id="
            sql_delete_data = sql_delete_data + d_employee_id
            self.cur.execute ( sql_delete_data )
            self.conn.commit ()

            print ( "The person number", d_employee_id, "has been deleted from the list " )

        except Exception as e:
            print ( e )
        finally:
            self.conn.close ()

    # use the variable has been taken from above to delete all employee id/Department data from the table with this function
    def delete_data_all(self):
        try:
            self.get_connection ()
            self.cur.execute ( self.sql_delete_data_all_emp )
            self.cur.execute ( self.sql_delete_data_all_dep )
            self.conn.commit ()
            print ( "all records have been deleted..." )

        except Exception as e:
            print ( e )
        finally:
            self.conn.close ()


# Employee Class has been created as matched with csv columns and created table columns
class Employee:

    def __init__(self,
                 employeeID,
                 employeename,
                 surname,
                 employeeTitle,
                 username,
                 email,
                 salary,
                 date,
                 gender,
                 password):
        self.employeeID = employeeID
        self.employeename = employeename
        self.surname = surname
        self.employeeTitle = employeeTitle
        self.username = username
        self.email = email
        self.salary = salary
        self.date = date
        self.gender = gender
        self.password = password

    def insert_statement(self):
        return_list = []
        return_list.append ( self.employeeID )
        return_list.append ( self.employeename )
        return_list.append ( self.surname )
        return_list.append ( self.employeeTitle )
        return_list.append ( self.username )
        return_list.append ( self.email )
        return_list.append ( self.salary )
        return_list.append ( self.date )
        return_list.append ( self.gender )
        return_list.append ( self.password )
        return tuple ( return_list )


# Department class has been created as matched with csv columns and created table columns
class Department:

    def __init__(self,
                 userID,
                 department,
                 location,
                 country):
        self.userID = userID
        self.department = department
        self.location = location
        self.country = country

    def insert_statement(self):
        return_list = []
        return_list.append ( self.userID )
        return_list.append ( self.department )
        return_list.append ( self.location )
        return_list.append ( self.country )
        return tuple ( return_list )


# The main function will parse arguments.
# These argument will be definded by the users on the console.
# The user will select a choice from the menu to interact with the database.

# Menu design
while True:
    print ( "\n Menu:" )
    print ( "**********" )
    print ( " 1. Create table EmployeeUoB" )
    print ( " 2. Insert data into EmployeeUoB" )
    print ( " 3. Select all data into EmployeeUoB" )
    print ( " 4. Search an employee" )
    print ( " 5. Update data some records" )
    print ( " 6. Delete data some records" )
    print ( " 7. Delete all data" )
    print ( " 8. Load data from the files" )
    print ( " 9. Exit\n" )

    # For each numbered menu content we are going to the functions from here
    __choose_menu = int ( input ( "Enter your choice: " ) )
    db_ops = DBOperations ()
    if __choose_menu == 1:
        db_ops.create_table ()
    elif __choose_menu == 2:
        db_ops.insert_data ()
    elif __choose_menu == 3:
        db_ops.select_all ()
    elif __choose_menu == 4:
        db_ops.search_data ()
    elif __choose_menu == 5:
        db_ops.update_data ()
    elif __choose_menu == 6:
        db_ops.delete_data ()
    elif __choose_menu == 7:
        db_ops.delete_data_all ()
    elif __choose_menu == 8:
        db_ops.insert_from_csv ()
    elif __choose_menu == 9:
        exit ( 0 )
    else:
        print ( "Invalid Choice" )
