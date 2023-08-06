from app import db


class CrawlerTask(db.Model):
    __tablename__ = 'crawler_task'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.BigInteger, unique=True, index=True)
    name = db.Column(db.String, index=True)
    last_crawled = db.Column(db.BigInteger, default=0)
    task_body = db.Column(db.Text)

    def __repr__(self):
        return "<{}:{}:{}>".format(self.task_id, self.name, self.last_crawled)
