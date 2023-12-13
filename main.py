import requests
import selectorlib 
import smtplib, ssl
import time
import sqlite3

URL = "http://programmer100.pythonanywhere.com/tours/"

'''connection = sqlite3.connect("data.db")'''
# Crear una clase Singleton para la conexión a la base de datos
class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = sqlite3.connect('data.db')
        return cls._instance

    def get_connection(self):
        return self.connection


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    textSource = response.text
    return textSource

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value

def sendEmail(message):
    host = "smtp.gmail.com"
    port = 465

    username = "contacto.issam@gmail.com"
    password = "xvkz soha otsc noye"

    receiver = "silverio.contacto@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print("Email enviado!")


def store(extracted, connection):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    '''cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()'''
    with connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", row)

def read(extracted, connection):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row 
    with connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
        rows = cursor.fetchall()
        return rows

if __name__ == "__main__":
    db_manager = DatabaseManager()
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        
        
        if extracted != "No upcoming tours":
            connection = db_manager.get_connection()
            row = read(extracted, connection)
            if not row:
                store(extracted, connection)
                sendEmail(message="Nuevo evento proximamente!")
        time.sleep(2)