import sqlite3

con = sqlite3.connect('test.db')
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS user(userID INTEGER PRIMARY KEY, firstName NOT NULL, lastName NOT NULL)")
cur.execute(
    "CREATE TABLE IF NOT EXISTS contactInfo(userID, phoneNumber INTEGER, FOREIGN KEY(userID) REFERENCES user(userID))")


def validUser(userID):
    """
    Check if a userID is valid and in use or not.

    Args:
        userID (int): The ID of the user to check.

    Returns:
        boolean: True if userID is in use, else false.
    """
    user = cur.execute("SELECT userID FROM user WHERE userID = ?", (userID,))
    if user.fetchone() is None:
        return False
    else:
        return True


def createUser():
    """
    Create a new user and insert into the database.

    The new user will only be created if the ID provided is not in use.

    After the new user is created, the user will be committed.
    """
    newUserID = int(input("Enter new user ID: "))

    if not validUser(newUserID):
        newFirstName = input("Enter first name: ")
        newLastName = input("Enter last name: ")
        newPhoneNumber = int(input("Enter phone number: "))
        cur.execute("INSERT INTO user VALUES (?, ?, ?)", (newUserID, newFirstName, newLastName))
        cur.execute("INSERT INTO contactInfo VALUES (?, ?)", (newUserID, newPhoneNumber))
        con.commit()
    else:
        print("\nUser with same ID already exists!\n")


def readUsers():
    """
    Retrieve all users from the user table and their contact information where userID is the same.

    Each user will be output on a new row.
    """
    for row in cur.execute(
            "SELECT user.userID, firstName, lastName, phoneNumber FROM user, contactInfo WHERE user.userID = contactInfo.userID"):
        print(row)


def updateUser():
    """
    Update user information by userID.

    The userID provided will be checked for validity.

    If the user exists, changes will be made then committed.
    """
    userID = int(input("Enter user ID to update: "))

    if validUser(userID):
        newFirstName = input("Enter new first name: ")
        newLastName = input("Enter new last name: ")
        newPhoneNumber = int(input("Enter new phone number: "))

        cur.execute("UPDATE user SET firstName = ? WHERE userID = ?", (newFirstName, userID))
        cur.execute("UPDATE user SET lastName = ? WHERE userID = ?", (newLastName, userID))
        cur.execute("UPDATE contactInfo SET phoneNumber = ? WHERE userID = ?", (newPhoneNumber, userID))
        con.commit()
    else:
        print("\nA user with this ID does not exist\n")


def deleteUser():
    """
    Delete a user from the database by userID.

    The userID provided will be checked for validity before deletion.

    The changes will then be committed.
    """
    userID = int(input("Enter user ID to delete: "))

    if not validUser(userID):
        print("\nA user with this ID does not exist\n")
    else:
        cur.execute("DELETE FROM user WHERE userID = ?", (userID,))
        con.commit()
        print("\nUser has been deleted.\n")


endProgram = False
userInput = 0

while not endProgram:
    """
    A loop that will ask the user for input to perform CRUD operations.

    When the user selects exit the loop will end and the database connection is closed.
    """
    print("\n1: Create user\n"
          "2: Read users\n"
          "3: Update user\n"
          "4: Delete user\n"
          "5: Exit & close database\n")

    userInput = int(input("Enter your choice (1-5): "))
    if userInput == 1:
        createUser()
    if userInput == 2:
        readUsers()
    if userInput == 3:
        updateUser()
    if userInput == 4:
        deleteUser()
    if userInput == 5:
        con.close()
        endProgram = True