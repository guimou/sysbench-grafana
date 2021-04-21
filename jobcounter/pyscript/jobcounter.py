# This code was written listening to Fortunate Son by Creedence Clearwater Revival

import time, os
import logging
import re
import mysql.connector

from kubernetes import config
config.load_incluster_config()
from kubernetes import client
core_v1 = client.CoreV1Api()

#Set DB connection
db_user = os.environ['MYSQL_USER']
db_password = os.environ['MYSQL_PASSWORD']
db_host = os.environ['MYSQL_HOST']
db_db = os.environ['MYSQL_DATABASE']

def update_db(node_name,node_status):
    try:
        cnx = mysql.connector.connect(user=db_user, password=db_password,
                                      host=db_host,
                                      database=db_db)
        cursor = cnx.cursor()
        query = 'INSERT INTO `' + node_name + '` (time,node_status) SELECT CURRENT_TIMESTAMP(),"' + str(node_status) + '";'
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise

node_name = ''
node_status = None

while 1:
    ret = core_v1.list_node()
    for node in ret.items:
        node_name = node.metadata.name
        for condition in node.status.conditions:
            if(condition.type == 'Ready'):
                if (condition.status == 'True'):
                    node_status = 1
                else:
                    node_status = 0
        update_db(node_name,node_status)
    time.sleep(3)
