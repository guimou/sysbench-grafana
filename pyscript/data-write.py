# This code was written listening to Fortunate Son by Creedence Clearwater Revival

import time, os
import logging
import re
import mysql.connector

#Set DB connection
db_user = os.environ['MYSQL_USER']
db_password = os.environ['MYSQL_PASSWORD']
db_host = os.environ['MYSQL_HOST']
db_db = os.environ['MYSQL_DATABASE']

#Set the filename and open the file
filename = '/logs/output.txt'
file = open(filename,'r')

#Find the size of the file and move to the end
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

REGEX = re.compile(r"((?<=reads:\s)\S*)|((?<=writes:\s)\S*)|((?<=fsyncs:\s)\S*(?=/s))|((?<=latency \(ms,95%\):\s)\S*)",re.M)

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

def process_line(line):
    values = re.findall(REGEX, line)
    d_reads = values[0][0]
    d_writes = values[1][1]
    d_fsyncs = values[2][2]
    d_latency = values[3][3]
    update_db(d_reads,d_writes,d_fsyncs,d_latency)

while 1:
    where = file.tell()
    line = file.readline().strip()
    if not line:
        time.sleep(1)
        file.seek(where)
    else:
        process_line(line)
