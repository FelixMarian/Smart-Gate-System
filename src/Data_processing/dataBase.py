import sqlite3

conn = sqlite3.connect('licencePlates.db')

# Create a cursor to execute SQL commands
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS licencesPlates(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          licencePlate TEXT NOT NULL)''')

def searchLicencePlate(searchedLicencePlate):
    # Search for the licence plate in the database
    c.execute("SELECT * FROM licencesPlates WHERE licencePlate = ?", (searchedLicencePlate,))

    result = c.fetchone()

    # 1 - Found in the database | 0 - Not found in the database
    if result is not None:
        return 1
    else:
        return 0

def deleteFromDatabase(licencePlateToDelete):
    c.execute("DELETE FROM licencesPlates WHERE licencePlate = ?", (licencePlateToDelete,))
    conn.commit()

def addToDatabase(licencePlateToAdd):
    c.execute("INSERT INTO licencesPlates (licencePlate) VALUES (?)", (licencePlateToAdd,))
    conn.commit()

# If the licence plate exists in the database, we delete it, and if it doesn't exist, we add it.
def processLicencePlate(licencePlate):
    try:
        if searchLicencePlate(licencePlate) == 1:
            deleteFromDatabase(licencePlate)
        else:
            addToDatabase(licencePlate)
    except Exception as e:
        return None

conn.commit()
