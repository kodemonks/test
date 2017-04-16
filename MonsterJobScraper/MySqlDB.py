import MySQLdb
import time
import datetime

#
#DB_schema.sql config here
#
config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'database': 'monster',
  'raise_on_warnings': True
}


#
#Class to handle database
#
class MySqlDBFetcher:
  conn = None

  def connect(self):
    self.conn = self.conn or MySQLdb.connect(
          host=config['host'],
          user=config['user'],
          passwd=config['password'],
          db=config['database']
    )




#
#
#
  def fetchDBdetailsforTimeStamp(self, sql):
    try:
      cursor = self.conn.cursor()
      cursor.execute(sql)
    except (AttributeError, MySQLdb.OperationalError):
      self.connect()
      cursor = self.conn.cursor()
      cursor.execute(sql)
    return cursor



#
#
#
  def fillDBwithDetails(self,jobDetailList):

    self.connect()
    cursor = self.conn.cursor()
    ts = time.time()
    print('Trying insert!!')
    listInsert = []
    for row in jobDetailList:
        job_title = row[1]
        company = row[2]
        location = row[3]
        timestamp = row[4]
        fileName = row[5]
        timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M")

        listInsert.append((0, str(job_title), str(company), str(location), timestamp.strftime('%Y-%m-%d'),
                           str(fileName), "monster"))

    sql = """ insert ignore into jobs_raw (
                id, job_title, company_name, location, register_date,text_file,source )
                values (%s,%s,%s,%s,%s,%s,%s)
            """

    try:
        cursor.executemany(sql,listInsert)
        self.conn.commit()

    except (AttributeError, MySQLdb.OperationalError):
        self.rollbackandReconnect()
        cursor = self.conn.cursor()
        cursor.executemany(sql, listInsert)
    except Exception as e:
        self.rollbackandReconnect()
        cursor = self.conn.cursor()
        cursor.executemany(sql, listInsert)
        print(e)
    return cursor



  def rollbackandReconnect(self):
    self.conn.rollback()
    self.connect()

  def disconnect(self):
      self.conn.close()
