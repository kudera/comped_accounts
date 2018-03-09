import json
import sys
import requests
import google_sheets_api_class
import mysql.connector
import datetime


with open("../config.json") as CONFIG:
    CONFIG = json.load(CONFIG)

GOOGLE_SHEET = google_sheets_api_class.GoogleSheetsAPI("1fG60nPO-5fy0ovW8jpaafmB3t0LOt-SY5gfP_laKOLY")


# Execute a SELECT query against MySQL database
def query_mysql_db(query):
    conn = mysql.connector.connect(user = CONFIG["sql"]["v3seomoz"]["user"],
                                   password = CONFIG["sql"]["v3seomoz"]["password"],
                                   host = CONFIG["sql"]["v3seomoz"]["host"],
                                   database = CONFIG["sql"]["v3seomoz"]["database"])
    cursor = conn.cursor()
    cursor.execute(query)
    query_results = cursor.fetchall()
    cursor.close()
    conn.close()

    return query_results


query_results = query_mysql_db("""SELECT p.name, u.email, s.user_id, s.account_id, p.description, s.start_date              
                                  FROM mondo.subscriptions s     
                                  JOIN mondo.products p          
                                  ON s.product_id = p.id
                                  JOIN v3seomoz.users u
                                  ON u.id = s.user_id
                                  WHERE p.level LIKE '%pro%'     
                                  AND pay_processor = 'comped'                            
                                  AND NOT p.level LIKE '%student%'""")

query_values = [list(row) for row in query_results]

for row in query_values:
    row[5] = row[5].strftime('%m/%d/%Y')
    row.append(datetime.date.today().strftime('%m/%d/%Y'))


header_list = [["NAME", "EMAIL", "USER ID", "ACCOUNT ID", "DESCRIPTION", "START DATE", "DATE RAN"]]

GOOGLE_SHEET.insert_lines(GOOGLE_SHEET.sheet_ids["dave_test"], 2, len(query_values))
GOOGLE_SHEET.write_range("dave_test!A1", header_list)
GOOGLE_SHEET.write_range("dave_test!A2", query_values)
