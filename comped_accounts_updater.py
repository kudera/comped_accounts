import psycopg2
import json
import sys
import requests
import google_sheets_api_class


with open("../config.json") as CONFIG:
    CONFIG = json.load(CONFIG)

GOOGLE_SHEET = google_sheets_api_class.GoogleSheetsAPI("1fG60nPO-5fy0ovW8jpaafmB3t0LOt-SY5gfP_laKOLY")


# Execute a SELECT query against mysql database with psycopg2
def query_mysql_db_psycopg2(query):
    conn_string = "host='{0}' port={1} dbname='{2}' user='{3}' password='{4}'".format(CONFIG["sql"]["redshift"]["host"],
                                                                                      CONFIG["sql"]["redshift"]["port"],
                                                                                      CONFIG["sql"]["redshift"]["database"],
                                                                                      CONFIG["sql"]["redshift"]["user"],
                                                                                      CONFIG["sql"]["redshift"]["password"])
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(query)
    query_results = cursor.fetchall()
    cursor.close()
    conn.close()

    return query_results



comped_account_query =  """SELECT p.name, u.email, s.user_id, s.account_id, p.description, s.start_date              
                        FROM mondo.subscriptions s     
                        JOIN mondo.products p          
                        ON s.product_id = p.id
                        JOIN v3seomoz.users u
                        ON u.id = s.user_id
                        WHERE p.level LIKE '%pro%'     
                        AND pay_processor = 'comped'                            
                        AND NOT p.level LIKE '%student%'""".format() #something needs to go here

comped_accounts = [row for row in comped_account_query]

comped_account_query_results = query_mysql_db_psycopg2(comped_account_query)
print(comped_account_query_results)

#comped_account_values = [list(row) for row in comped_account_query_results]
#GOOGLE_SHEET.write_range("dave_test!A2", comped_accounts)
