
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings


class MySQLStorePipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        try:
            print("Creating MySQL connection!!")
            dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
            print(dbpool)
            print("Created MySQL connection!!")

            return cls(dbpool)
        except:
            print("\n\n\n\nERROR in MySQL connection")
            pass


    def _handle_error(self, e):
        print('Got an Error here!!!\n\n\n')
        print(e)
        # log.err(e)




    def process_item(self, item, spider):
        # run db query in thread pool
        d = self.dbpool.runInteraction(self._conditional_insert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _conditional_insert(self, tx, item):
        # create record if doesn't exist.
        # all this block run on it's own thread
        tx.execute("select * from websites where University = %s", (item['University'][0],))
        result = tx.fetchone()
        if result:
            print('No insert as Item already present')
# log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
        else:
            print('\n\nTrying to insert\n\n\n')
            tx.execute("""INSERT INTO UniversityInfo
                        VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                       (item['University'].encode('utf-8'), item['Type'].encode('utf-8'),
                        item['City'].encode('utf-8'), item['Website'].encode('utf-8'),
                        item['Address'].get('Address:').encode('utf-8'), item['Credential_Type'].encode('utf-8'),
                        item['Email'], item['Fax'], item['Joint_Credential_Type'], item['Joint_Program_Level'],
                        item['Program_Level'], item['Telephone'], item['Toll_Free']
))
            # log.msg("Item stored in db: %s" % item, level=log.DEBUG)

