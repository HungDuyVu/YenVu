import re
from database.validation import Validation

import mysql.connector
import json

# connect DB
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="audio"
)

Validation(mydb).check_table_exists()
class Database():
    def get_all_information_without_test(self):
        mycursor = mydb.cursor(dictionary=True)
        sql = "SELECT * FROM audio WHERE audio.category != 'new'"

        mycursor.execute(sql)
        # Fetch all the results
        results = mycursor.fetchall()
        return results
    def get_all_information(self):
        mycursor = mydb.cursor(dictionary=True)
        sql = "SELECT * FROM audio"

        mycursor.execute(sql)
        # Fetch all the results
        results = mycursor.fetchall()
        return results

    def save_word_extraction(self,content,file_name):
        mycursor = mydb.cursor()
        sql = "UPDATE audio SET content = %s WHERE name = %s"
        values = (content, file_name)

        mycursor.execute(sql, values)

        # Remember to commit the transaction if you want to make the changes permanent
        mydb.commit()

    def save_audio_name(self,file_name,category):
        mycursor = mydb.cursor()
        sql = "INSERT INTO audio (name, content, category) VALUES (%s, %s, %s)"
        values = (file_name, 'null', category)

        mycursor.execute(sql, values)

        # Remember to commit the transaction if you want to make the changes permanent
        mydb.commit()

    def remove_all_audio_information(self):
        mycursor = mydb.cursor()
        sql = "DELETE FROM audio"

        mycursor.execute(sql)
        mydb.commit()

    def get_file_name_by_id(self,id):
        mycursor = mydb.cursor(dictionary=True)
        sql = "SELECT * FROM audio WHERE id = %s"

        mycursor.execute(sql,(id,))
        results = mycursor.fetchone()
        return results
db = Database()
