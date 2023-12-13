import requests
import selectorlib 
import datetime
import streamlit as st
import sqlite3

connection = sqlite3.connect("temperaturas/data2.db")
URL = "http://programmer100.pythonanywhere.com/"

def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    textSource = response.text
    return textSource


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("temperaturas/temps.yaml")
    value = extractor.extract(source)["temps"]
    
    return value


def store(extracted):
    tiempoActual = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Temperaturas VALUES(?, ?)", (extracted, tiempoActual))
    connection.commit()

if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    store(extracted)
    print(extracted)
    