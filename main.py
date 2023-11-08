import sqlite3
import csv
import random
import os.path

conn = sqlite3.connect('./StudentDB.db')
cursor = conn.cursor()


def check_alpha(name):
    while not name.isalpha():
        name = input("Enter valid input: ")
    return name


def check_gpa(gpa):
    while not (gpa.count('.') == 1 and gpa.replace(".","").isdecimal() and 0.00 <= float(gpa) <= 4.00):
        gpa = input("\nEnter valid Student GPA: ")
    return round(float(gpa),2)


def check_alpha_with_space(words):
    while not words.replace(" ", "").isalpha():
        words = input("Enter valid input: ")
    return words


def assign_faculty_advisor():
    cursor.execute("SELECT COUNT(*) "
                   "FROM FacultyAdvisors ")
    advisor_number = cursor.fetchone()
    advisor_number = advisor_number[0]
    random_number = random.randint(1, advisor_number)
    sql = "SELECT FullName FROM FacultyAdvisors WHERE ID = "
    sql = sql + str(random_number)
    cursor.execute(sql)
    faculty_name = cursor.fetchone()
    faculty_name = str(faculty_name[0])
    return faculty_name


def update_faculty_advisor(number):
    sql = "SELECT FullName FROM FacultyAdvisors WHERE ID = "
    sql = sql + str(number)
    cursor.execute(sql)
    faculty_name = cursor.fetchone()
    faculty_name = str(faculty_name[0])
    return faculty_name



def check_state(state):
    s_state_to_abbrev = {
        "AL": "Alabama",
        "AK": "Alaska",
        "AZ": "Arizona",
        "AR": "Arkansas",
        "CA": "California",
        "CO": "Colorado",
        "CT": "Connecticut",
        "DE": "Delaware",
        "FL": "Florida",
        "GA": "Georgia",
        "HI": "Hawaii",
        "ID": "Idaho",
        "IL": "Illinois",
        "IN": "Indiana",
        "IA": "Iowa",
        "KS": "Kansas",
        "KY": "Kentucky",
        "LA": "Louisiana",
        "ME": "Maine",
        "MD": "Maryland",
        "MA": "Massachusetts",
        "MI": "Michigan",
        "MN": "Minnesota",
        "MS": "Mississippi",
        "MO": "Missouri",
        "MT": "Montana",
        "NE": "Nebraska",
        "NV": "Nevada",
        "NH": "New Hampshire",
        "NJ": "New Jersey",
        "NM": "New Mexico",
        "NY": "New York",
        "NC": "North Carolina",
        "ND": "North Dakota",
        "OH": "Ohio",
        "OK": "Oklahoma",
        "OR": "Oregon",
        "PA": "Pennsylvania",
        "RI": "Rhode Island",
        "SC": "South Carolina",
        "SD": "South Dakota",
        "TN": "Tennessee",
        "TX": "Texas",
        "UT": "Utah",
        "VT": "Vermont",
        "VA": "Virginia",
        "WA": "Washington",
        "WV": "West Virginia",
        "WI": "Wisconsin",
        "WY": "Wyoming",
        "DC": "District of Columbia",
        "AS": "American Samoa",
        "GU": "Guam",
        "MP": "Northern Mariana Islands",
        "PR": "Puerto Rico",
        "UM": "United States Minor Outlying Islands",
        "VI": "U.S. Virgin Islands",
    }
    state = check_alpha(state)
    while state.upper() not in s_state_to_abbrev.keys():
        state = input("Enter valid Two-Letter State Code: ")
    return s_state_to_abbrev.get(state.upper())


def check_zipcode(zipcode):
    while not (zipcode.isnumeric() and len(zipcode) == 5):
        zipcode = input("Enter valid input: ")
    return str(zipcode)


def check_phone_number(phone_number):
    while not phone_number.isnumeric():
        phone_number = input("Enter valid input: ")
    return phone_number


def import_data():
    csv_filename = input("Enter CSV file: ")
    csv_filepath = "./" + csv_filename
    is_file = os.path.isfile(csv_filepath)
    while not is_file:
        csv_filename = input("Enter CSV file: ")
        csv_filepath = "./" + csv_filename
        is_file = os.path.isfile(csv_filepath)
    print("\nOpening File...\n")
    filename = open(csv_filename, 'r')
    csv_file = csv.DictReader(filename)
    for row in csv_file:
        faculty_name = assign_faculty_advisor()
        cursor.execute("INSERT INTO Students('FirstName', 'LastName', 'GPA', 'Major', 'Address', "
                       "'City', 'State', 'ZipCode', 'MobilePhoneNumber', 'isDeleted', 'FacultyAdvisor') "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                       (row['FirstName'], row['LastName'], row['GPA'], row['Major'], row['Address'],
                        row['City'], row['State'], row['ZipCode'],
                        row['MobilePhoneNumber'], 0, faculty_name))
    conn.commit()


def display_students():
    print("(StudentId, FirstName, LastName, GPA, Major, "
          "FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted)")
    cursor.execute("SELECT StudentId, FirstName, LastName, GPA, Major, "
                   "FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber "
                   "FROM Students "
                   "WHERE isDeleted = 0 "
                   "ORDER BY LastName; ")
    rows = cursor.fetchall()
    for row in rows:
        print(row)



def search_students():
    userinput = input("Search (Enter only one keyword): ")

    if userinput.replace(".", "").isnumeric():
        query = ("SELECT StudentId, FirstName, LastName, GPA, Major, "
                 "FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber "
                 "FROM Students WHERE isDeleted = 0 "
                 "AND GPA = ")
        query += userinput
    else:
        query = ("SELECT StudentId, FirstName, LastName, GPA, Major, "
                 "FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber "
                 "FROM Students WHERE "
                 "Major LIKE '%{m}%' "
                 "OR City LIKE '%{c}%' "
                 "OR State LIKE '%{s}%' "
                 "OR FacultyAdvisor LIKE '%{a}%' "
                 "AND isDeleted = 0 "
                 "ORDER BY LastName; ").format(m=userinput, c=userinput, s=userinput, a=userinput)
    cursor.execute(query)
    rows = cursor.fetchall()
    count = 0
    for row in rows:
        count += 1
    count = str(count)
    print("About "+count+" results.")
    print("(StudentId, FirstName, LastName, GPA, Major, "
          "FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted)")
    for row in rows:
        print(row)


def add_student():
    first_name = check_alpha(input("Enter Student First Name: "))
    last_name = check_alpha_with_space(input("\nEnter Student Last Name: "))
    gpa = check_gpa(input("\nEnter Student GPA: "))

    major = check_alpha_with_space(input("\nEnter Student Major: "))
    # Faculty advisor is randomly assigned
    faculty_advisor = assign_faculty_advisor()

    # Address does not need to be checked
    address = input("\nEnter Student Address: ")

    city = check_alpha_with_space(input("\nEnter Student City: "))
    state = check_state(input("\nEnter Student State (Two-Letter Code): "))
    zipcode = check_zipcode(input("\nEnter Student Zip Code: "))
    mobile_phone = check_phone_number(input("\nEnter Student Mobile Phone Number: "))

    cursor.execute("INSERT INTO Students('FirstName', 'LastName', 'GPA', 'Major', 'Address', "
                   "'City', 'State', 'ZipCode', 'MobilePhoneNumber', 'isDeleted', 'FacultyAdvisor') "
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); ",
                   (first_name, last_name, gpa, major, address, city, state, zipcode, mobile_phone, 0, faculty_advisor))
    conn.commit()
    print("\nStudent was added!")


def update_student():
    student_id = input("Enter StudentID: ")
    is_int = student_id.isnumeric()
    while not is_int:
        student_id = input("Enter valid StudentID: ")
        is_int = student_id.isnumeric()
    int(student_id)
    cursor.execute(("SELECT StudentId, FirstName, LastName, GPA, Major, "
                    "FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber "
                    "FROM Students "
                    "WHERE StudentId = (?) AND isDeleted = 0;"), (student_id,))
    rows = cursor.fetchall()
    count = 0
    for row in rows:
        count += 1
    while count == 0:
        student_id = input("StudentID not found. Enter valid StudentId: ")
        is_int = student_id.isnumeric()
        while not is_int:
            student_id = input("Enter valid StudentID: ")
            is_int = student_id.isnumeric()
        cursor.execute(("SELECT * "
                        "FROM Students "
                        "WHERE StudentId = (?) AND isDeleted = 0;"), (student_id,))
        count = 1

    userinput = input(
        "Student found. Change Major, Advisor, or PhoneNumber. Press \"c\" to cancel. (m/a/p/c): ")
    while not (userinput == "m" or userinput == "a" or userinput == "p" or userinput == "c"):
        userinput = input("Change Major, Advisor, or PhoneNumber. Press \"c\" to cancel. (m/a/p/c): ")
    if userinput == "m":
        major = check_alpha_with_space(input("Enter New Major: "))
        cursor.execute(("UPDATE Students "
                        "SET Major = (?)"
                        "WHERE StudentId = (?); "), (major, student_id,))
    elif userinput == "a":
        print("ID, FullName")
        cursor.execute("SELECT * "
                       "FROM FacultyAdvisors;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        conn.commit()
        number = input("Input Faculty ID: ")
        advisor = update_faculty_advisor(number)
        cursor.execute(("UPDATE Students "
                        "SET FacultyAdvisor = (?)"
                        "WHERE StudentId = (?); "), (advisor, student_id,))
    elif userinput == "p":
        phone_number = check_phone_number(input("Enter New PhoneNumber: "))
        cursor.execute(("UPDATE Students "
                        "SET MobilePhoneNumber = (?)"
                        "WHERE StudentId = (?); "), (phone_number, student_id,))
    elif userinput == "c":
        return
    else:
        return
    conn.commit()


def delete_student():
    is_found = False
    student_id = input("Enter StudentId to Delete: ")
    cursor.execute("SELECT * "
                   "FROM Students ")
    rows = cursor.fetchall()
    count = 0
    for row in rows:
        count += 1
    while not is_found:
        while not student_id.isnumeric() and 1 <= int(student_id) <= count:
            student_id = input("Enter StudentId to Delete: ")
        query = "UPDATE Students SET isDeleted = 1 WHERE StudentId = "
        query += student_id
        cursor.execute(query)
        conn.commit()
        if cursor.rowcount == 1:
            is_found = True


if __name__ == '__main__':
    # Beginning of Program
    isDone = False
    while not isDone:

        print("1. Import CSV file"
              "\n2. Display All Students"
              "\n3. Add New Student"
              "\n4. Update Student"
              "\n5. Delete Student"
              "\n6. Search Students"
              "\n7. Exit")
        userinput = input("\nEnter a number: ")

        while not userinput.isnumeric() or int(userinput) < 1 or int(userinput) > 7:
            userinput = input("Enter a valid number: ")

        userinput = int(userinput)

        if userinput == 1:
            import_data()
        elif userinput == 2:
            display_students()
        elif userinput == 3:
            add_student()
        elif userinput == 4:
            update_student()
        elif userinput == 5:
            delete_student()
        elif userinput == 6:
            search_students()
        elif userinput == 7:
            isDone = True
        else:
            isDone = True

cursor.close()
