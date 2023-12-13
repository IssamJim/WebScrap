import streamlit as st
import plotly.express as px
import sqlite3

connection = sqlite3.connect("temperaturas/data2.db")
cursor = connection.cursor()
cursor.execute("SELECT fecha FROM Temperaturas")
date = cursor.fetchall()
date = [item[0] for item in date]

cursor.execute("SELECT temps from Temperaturas")
temperatura = cursor.fetchall
temperatura = [item[0] for item in temperatura]

figure = px.line(x=date, y=temperatura,
                 labels={"x": "Fecha", "y": "Temperatura (C)"})

st.plotly_chart(figure)