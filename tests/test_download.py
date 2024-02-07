import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO
import os
import fitz
import sqlite3
from assignment0 import main

@pytest.fixture
def setup_mock_urlopen():
    with patch('urllib.request.urlopen') as mock_request:
        mock_response = BytesIO(b"Sample PDF data")
        mock_request.return_value = MagicMock(read=MagicMock(return_value=mock_response.getvalue()))
        yield

def test_download_and_save_pdf(setup_mock_urlopen):
    test_url = "https://example.com/test_pdf.pdf"
    expected_file_path = "/tmp/incident.pdf"

    result_path = main.fetchincidents(test_url)

    assert result_path == expected_file_path
    assert os.path.isfile(result_path)
    assert os.path.getsize(result_path) > 0

    # Cleanup
    os.remove(result_path)


def create_test_pdf(pdf_path, content):
    doc = fitz.open()  # Create a new PDF in memory
    page = doc.new_page()  # Add a new page
    page.insert_text((72, 72), content)  # Add text to the page
    with open(pdf_path, "wb") as f:
        doc.save(f)  # Save the PDF to the given path
    doc.close()

def test_extract():
    expected_data = ('1/7/2024 0:07', '2024-00001345', '300 E GRAY ST', 'Traffic Stop', 'OK0140200')
    global incident_data
    incident_data = main.extractincidents("tests/test_file.pdf")
    actual_data = incident_data[0]
    if expected_data == actual_data:
        assert True
    else:
        assert False

def matchWithIncident(incident, anticipatedIncident):
    return (
        incident["date_time"] == anticipatedIncident["date_time"] and
        incident["incident_number"] == anticipatedIncident["incident_number"] and
        incident["location"] == anticipatedIncident.get("location", incident["location"]) and
        incident["nature"] == anticipatedIncident["nature"] and
        incident["incident_ori"] == anticipatedIncident.get("incident_ori", incident["incident_ori"]))


def test_create_db():
    conn = main.createdb()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents';")
    assert cursor.fetchone()
    conn.close()

def test_populate_db():
    conn = main.createdb()
    test_data = [('2024-01-01 00:00', '12345', 'Location 1', 'Nature 1', 'ORI1')]
    main.populatedb(conn, test_data)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM incidents;")
    count = cursor.fetchone()[0]
    assert count == len(test_data)


def test_status(capsys):
    conn = sqlite3.connect(":memory:")
    conn.execute('''CREATE TABLE IF NOT EXISTS incidents (
        incident_time TEXT,
        incident_number TEXT,
        incident_location TEXT,
        nature TEXT,
        incident_ori TEXT
    );''')
    conn.executemany('''INSERT INTO incidents 
                    (incident_time, incident_number, incident_location, nature, incident_ori) 
                    VALUES (?, ?, ?, ?, ?);''', 
                    [   ("01/01/2024 12:00", "1234-567890", "123 Example St", "Abdominal Pains/Problems", "ABC123"),
                        ("02/02/2024 13:30", "1235-567891", "124 Example St", "Cough", "ABC124"),
                        ("03/03/2024 14:40", "1236-567892", "125 Example St", "Sneeze", "ABC125"),
                        ("04/04/2024 15:50", "1237-567893", "126 Example St", "Breathing Problems", "ABC126"),
                        ("05/05/2024 16:00", "1238-567894", "127 Example St", "Noise Complaint", "ABC127"),
                        ("06/06/2024 17:10", "1239-567895", "128 Example St", "Cough", "ABC128"),
                        ("07/07/2024 18:20", "1240-567896", "129 Example St", "Sneeze", "ABC129"),
                    ])
    main.status(conn)

    captured = capsys.readouterr()

    expected_output = "Cough|2\nSneeze|2\nAbdominal Pains/Problems|1\nBreathing Problems|1\nNoise Complaint|1\n"

    assert captured.out == expected_output

    conn.close()




