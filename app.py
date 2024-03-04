
from flask import Flask, g, render_template, request
import sqlite3


import sklearn as sk
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import io
import base64

"""
This script contains routes and functions for a Flask web application.

It defines routes for the main page, message submission, and viewing messages.
"""

DATABASE = 'messages_db.sqlite'
app = Flask(__name__)


@app.route('/')
def base():
    messages = random_messages(3)  # Retrieve 3 random messages
    return render_template('base.html', messages=messages)

@app.route('/submit', methods=['GET','POST'])
def submit():
    """
    Handles message submission.

    If the request method is POST, it inserts the message into the database.
    Renders the 'submit.html' template.
    """
    if request.method == 'POST':
        insert_message(request)
    return render_template('submit.html')

@app.route('/message')
def message():
    """
    Displays all messages stored in the database.

    Retrieves all messages from the database and renders the 'view.html' template with these messages.
    """
    db = get_message_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM messages")
    messages = cursor.fetchall()
    cursor.close()
    return render_template('view.html', messages=messages)



# Function to get the message database
def get_message_db():
    """
    Retrieve the SQLite database connection for storing messages.

    If the 'message_db' attribute is not present in the global 'g' object, 
    it creates a new connection to the SQLite database defined by the 
    'DATABASE' constant. It also creates a 'messages' table in the database 
    if it doesn't already exist.

    Returns:
    - sqlite3.Connection: The SQLite database connection object.
    """
    if 'message_db' not in g:
        g.message_db = sqlite3.connect(DATABASE)
        cursor = g.message_db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                            id INTEGER PRIMARY KEY,
                            handle TEXT,
                            message TEXT
                        )''')
        g.message_db.commit()
    return g.message_db
    

# Function to insert a user message into the database
def insert_message(request):
    """
    Insert a user message into the database.

    Args:
    - request (flask.request): The request object containing form data.

    Returns:
    - str: The message that was inserted into the database.
    """
    db = get_message_db()
    cursor = db.cursor()
    name = request.form['nm']
    message = request.form['message']
    cursor.execute("INSERT INTO messages (handle, message) VALUES (?, ?)", (name, message))
    db.commit()
    cursor.close()
    return message
 

@app.route('/view_messages')
def view_messages():
    """
    Display a page showing a random selection of messages.

    Returns:
    - flask.render_template: HTML page displaying the random messages.
    """
    messages = random_messages(5)  # You can change the number of messages to retrieve
    return render_template('view.html', messages=messages)

# Function to retrieve n random messages from the database
def random_messages(n):
    """
    Retrieve n random messages from the database.

    Args:
    - n (int): Number of random messages to retrieve.

    Returns:
    - list: A list of tuples containing the retrieved messages.
    """
    db = get_message_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM messages ORDER BY RANDOM() LIMIT ?", (n,))
    messages = cursor.fetchall()
    cursor.close()
    db.close()  # Close the database connection
    return messages


