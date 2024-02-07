# cis6930sp24 -- Project0 -- Template

Name: Omkar Sunil Bhabad

## Description 
This project presents an innovative approach to automating the extraction and analysis of incident reports from the Norman Police Department, converting PDF documents into structured data within a SQLite database. It Utilizes Python to automate the downloading, parsing, and summarizing of data, making it easier for users to access and analyze public safety information. It's a practical tool aimed at simplifying how we interact with and study law enforcement data, offering a hands-on solution to data management problems commonly faced in academic and professional settings.

## How to Install
1. Ensure Python 3.x is installed on your system. Check this by running `python --version` in your terminal.
2. Clone the project repository to your local machine from its GitHub page.
3. Execute `pipenv install` to create a virtual environment and install dependencies.
4. Activate the environment with `pipenv shell`.
5. Navigate to the project's root directory in your terminal.
6. Execute the script by running `python main.py --incidents URL`, replacing URL with the actual link to the Norman Police Department's PDF report you wish to analyze.

## How to Run
Video

## Functions
#### main.py 
The `main` function orchestrates the process of downloading, extracting, and storing incident data from a specified PDF URL. It uses command-line arguments to receive the PDF URL, calls `fetchincidents` to download the PDF, `extractincidents` to parse data, `createdb` to prepare a database, and `populatedb` to insert data. Finally, it displays a summary of incidents with `status`.

#### fetchincidents 
The `fetchincidents` function automates the process of downloading a PDF file from a provided URL. It establishes an SSL context to handle HTTPS requests without verifying SSL certificates, ensuring compatibility with various servers. After downloading the PDF content, it saves the file to a temporary directory, specifically naming it `incident.pdf`. This functionality is crucial for preparing the PDF for data extraction, facilitating the seamless retrieval of incident reports for analysis.

#### extractincidents 
The `extractincidents` function processes the downloaded PDF file to extract incident data. It utilizes the PyMuPDF library to read each page of the PDF and identifies text based on predefined column coordinates. By parsing through the text elements, it organizes the data into structured rows representing individual incidents. This structured data is then prepared for database insertion, enabling the transformation of unstructured PDF content into a format suitable for analysis and storage.

#### createdb 
The `createdb` function initiates the creation of a new SQLite database named 'normanpd.db'. It ensures a fresh start by removing any existing file with the same name before establishing a new database connection. Within this database, it sets up a table specifically designed to store incident data, with columns for incident time, number, location, nature, and the incident ORI. This setup is pivotal for organizing the extracted data into a structured and queryable format, facilitating both storage and subsequent analysis.

#### populatedb 
The `populatedb` function is tasked with inserting the structured incident data into the SQLite database. It executes a batch insertion command that maps the extracted data fields to the corresponding columns in the database's `incidents` table. This method efficiently transfers the parsed incident records into the database, ensuring the data is stored in a manner that supports easy retrieval and analysis.

#### status 
The `status` function queries the SQLite database to aggregate and count incidents based on their nature. It organizes the results in descending order by count and prints a summary to the console. This display provides a quick overview of incident frequencies, allowing users to discern patterns or prevalent issues within the dataset.

## Test 
Testing involves creating your own test files, particularly because Norman PD files are removed irregularly. Tests cover downloading, processing data, and are designed to be run with `pipenv run python -m pytest`, ensuring functionality like PDF handling and database operations. It's recommended to download and save test files locally for reliability.

## Assumptions
1. Assumes consistent PDF format from Norman PD, this Can lead to Potential parsing inaccuracies with complex PDF layouts.
2. Relies on internet for PDF downloads, affecting functionality without connectivity.
3. Tests based on locally saved test files, assuming they accurately represent typical reports.