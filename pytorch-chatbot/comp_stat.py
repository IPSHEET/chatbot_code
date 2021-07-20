import mysql.connector
import json
from datetime import date

def checkstat(compID):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ipu@3011",
            database="espl2"
        )

        cursor = connection.cursor(prepared=True)

        query="""SELECT comp_stat FROM comp_stat where comp_id=%s"""
        cursor.execute(query, (compID,))
        myresult=cursor.fetchall()
    
        for x in myresult:
            return x[0]

    except mysql.connector.Error as error:
        # return "Couldn't connect to server"
        print("Failed to update table record: {}".format(error))



def checkrem(compID):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ipu@3011",
            database="espl2"
        )
        cursor = connection.cursor(prepared=True)

        query="""SELECT rem_date FROM comp_stat where comp_id=%s"""
        cursor.execute(query, (compID,))
        myresult=cursor.fetchall()
    
        for x in myresult:
            return x[0]

    except mysql.connector.Error as error:
        print("Failed to update table record: {}".format(error))


def setrem(compID):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ipu@3011",
            database="espl2"
        )

        cursor = connection.cursor(prepared=True)
        sql_update_query = """Update comp_stat set rem_date = %s where comp_id = %s"""
        input_data=(date.today(),compID)
        cursor.execute(sql_update_query,input_data)
        connection.commit()
        print("Reminder Set")

    except mysql.connector.Error as error:
        print("Failed to update table record: {}".format(error))


# print(checkstat(112))