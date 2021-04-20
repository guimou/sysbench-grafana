# This code was written listening to Fortunate Son by Creedence Clearwater Revival

import time, os
import logging
import re
import mysql.connector
from kubernetes import client, config

#Set DB connection
db_user = os.environ['MYSQL_USER']
db_password = os.environ['MYSQL_PASSWORD']
db_host = os.environ['MYSQL_HOST']
db_db = os.environ['MYSQL_DATABASE']

config.load_kube_config()

def update_db(d_reads,d_writes,d_fsyncs,d_latency):
    try:
        cnx = mysql.connector.connect(user=db_user, password=db_password,
                                      host=db_host,
                                      database=db_db)
        cursor = cnx.cursor()
        query = 'INSERT INTO benchmark(time,d_reads,d_writes,d_fsyncs,d_latency) SELECT CURRENT_TIMESTAMP(),"' + d_reads + '","' + d_writes + '","' + d_fsyncs + '","' + d_latency + '";'
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise

print("Listing pods with their IPs:")
namespace='sysbench'
v1 = client.CoreV1Api()   
ret = v1.list_namespaced_pod(namespace)
for i in ret.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
