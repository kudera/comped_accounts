import psycopg2
import json
import sys
import requests


with open("../config.json") as CONFIG:
    CONFIG = json.load(CONFIG)



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

    comped_account_query =  SELECT p.name, u.email, s.user_id, s.account_id, p.description, s.start_date              
                            FROM mondo.subscriptions s     
                            JOIN mondo.products p          
                            ON s.product_id = p.id
                            JOIN v3seomoz.users u
                            ON u.id = s.user_id
                            WHERE p.level LIKE '%pro%'     
                            AND pay_processor = 'comped'
                            AND NOT p.level LIKE '%student%'
                              

