from twisted.enterprise import adbapi
import pymysql


class MySqlStorePipeline(object):
    def __init__(self):
        self.dbpool = None

    def process_item(self, item, spider):
        # run db query in thread pool
        if spider.name == "szse":
            if self.dbpool == None:
                self.dbpool = adbapi.ConnectionPool('pymysql', host='localhost', db='spider',
                                                    user='root', passwd='123456',
                                                    cursorclass=pymysql.cursors.DictCursor,
                                                    charset='utf8', use_unicode=True)
            query = self.dbpool.runInteraction(self._conditional_insert, item, spider)
            query.addErrback(self.handle_error, spider)
        return item

    def _conditional_insert(self, tx, item, spider):
        # create record if doesn't exist.
        # all this block run on it's own thread
        tx.execute("select * from szse where rulelink = %s", (item['rulelink']))
        result = tx.fetchone()
        if result:
            print("Item already stored")
            # log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
            spider.logger.info("Item already stored in db: %s" % item["rulelink"])
        else:
            tx.execute( \
                "insert into szse (ruletitle, rulelink, ruledate, content, file_urls, filename, filepath) "
                "values (%s, %s, %s, %s, %s, %s, %s)",
                (item['ruletitle'],
                 item['rulelink'],
                 item['ruledate'],
                 item['content'],
                 item['file_urls'],
                 item['filename'],
                 item['filepath']
                 )
            )
            # log.msg("Item stored in db: %s" % item, level=log.DEBUG)

    def handle_error(self, e, spider):
        spider.logger.info("Insert into table error: %s" % e)
