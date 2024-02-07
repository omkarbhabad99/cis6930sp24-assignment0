# -*- coding: utf-8 -*-
# main.py

import argparse  # Used for parsing command line arguments
import urllib.request  # For issuing HTTP requests to download PDF files
import os  # For interacting with the operating system, e.g., file paths
import sqlite3  # For database operations
import fitz  # PyMuPDF, used for interacting with PDF files
import ssl  # Import the SSL module for handling HTTPS requests
import tempfile  

def fetchincidents(url):
    """
    Download the PDF from the given URL and save it to a temporary file.
    
    """
    context = ssl._create_unverified_context()  # Create a context that does not verify SSL certificates
    response = urllib.request.urlopen(url, context=context) 
    
    temp_dir = tempfile.gettempdir()  # Get the path to the system's temporary directory
    file_name = os.path.join(temp_dir, 'incident.pdf') 
    
    with open(file_name, 'wb') as file: 
        file.write(response.read())  # Write the downloaded PDF content to the file
    return file_name 

def extractincidents(pdf_path):
    columns = [52.560001373291016, 150.86000061035156, 229.82000732421875, 423.19000244140625,
               623.8599853515625]

    pages = fitz.open(pdf_path)
    final_response = []
    my_dict = {}
    prev = 0
    for page in pages:
        array = page.get_text('words')
        for tuple_data in array:
            block_no = tuple_data[5]
            if block_no in my_dict:
                list_incidents = my_dict.get(block_no)
                list_incidents.append(tuple_data)
            else:
                if my_dict:
                    list_words = my_dict[prev]
                    rows = ["", "", "", "", ""]
                    for data in list_words:
                        x_coordinate = data[0]
                        text = data[4]
                        if x_coordinate == columns[0] or x_coordinate < columns[1]:
                            rows[0] = rows[0] + " " + text if rows[0] else text
                        elif x_coordinate == columns[1] or x_coordinate < columns[2]:
                            rows[1] = rows[1] + " " + text if rows[1] else text
                        elif x_coordinate == columns[2] or x_coordinate < columns[3]:
                            rows[2] = rows[2] + " " + text if rows[2] else text
                        elif x_coordinate == columns[3] or x_coordinate < columns[4]:
                            rows[3] = rows[3] + " " + text if rows[3] else text
                        else:
                            rows[4] = rows[4] + " " + text if rows[4] else text
                    if rows[2].find("NORMAN POLICE DEPARTMENT") == -1 and rows[2].find(
                            "Daily Incident Summary") == -1 and rows[1].find("Incident Number") == -1:
                        final_response.append(tuple(rows))
                    rows = ["", "", "", "", ""]
                    my_dict.clear()
                list = []
                list.append(tuple_data)
                my_dict[block_no] = list
            prev = block_no
    return final_response


def createdb():
    """
    Creates a new SQLite database named 'normanpd.db' and sets up a table for incident data.
    """
    db_file = 'resources/normanpd.db'  # Define the database file name
    if os.path.exists(db_file):  # If the database file already exists
        os.remove(db_file)  # Delete the existing file to start fresh
    conn = sqlite3.connect(db_file)  # Create a new database connection
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    cursor.execute('''CREATE TABLE IF NOT EXISTS incidents (
                        incident_time TEXT,
                        incident_number TEXT,
                        incident_location TEXT,
                        nature TEXT,
                        incident_ori TEXT
                      );''')  # Execute a SQL command to create the incidents table
    conn.commit()  # Commit the changes to the database
    return conn  # Return the database connection object

def populatedb(db, incidents):
    """
    Inserts the extracted incident data into the SQLite database.
    """
    cursor = db.cursor()  # Create a cursor object to execute SQL commands
    cursor.executemany('''INSERT INTO incidents 
                          (incident_time, incident_number, incident_location, nature, incident_ori) 
                          VALUES (?, ?, ?, ?, ?);''', incidents)  # Insert the incident data into the database
    db.commit()  # Commit the changes to the database

def status(db):
    """
    Prints a summary of the incident data, grouped by the nature of the incident.
    """
    cursor = db.cursor()  # Create a cursor object to execute SQL commands
    cursor.execute('''SELECT nature, COUNT(*) as count 
                      FROM incidents 
                      GROUP BY nature 
                      ORDER BY count DESC, nature;''')  # Execute a SQL command to aggregate incident data by nature
    answer = cursor.fetchall()
    empty_count = 0
    for nature, count in answer:
        if nature:
            print(f"{nature}|{count}")
        else:
            empty_count += count
    if empty_count != 0:
        print(f"|{empty_count}")

def main(url):
    """
    Main function to orchestrate the downloading, extraction, and storage of incident data.
    """
    incident_data = fetchincidents(url)  # Download the PDF from the specified URL

    incidents = extractincidents(incident_data)  # Extract incident data from the downloaded PDF
    db = createdb()  # Create a new SQLite database
    
    populatedb(db, incidents)  # Insert the extracted incident data into the database
    
    status(db)  # Print a summary of the incident data

if __name__ == '__main__':
    parser = argparse.ArgumentParser()  # Create an argument parser object
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary url.")  # Define a command line argument for the incident summary URL
    
    args = parser.parse_args()  # Parse the command line arguments
    if args.incidents:  # If the incidents argument was provided
        main(args.incidents)  # Call the main function with the specified URL
