# https://tool.lu/crontab/
# 默认是内存存储，如果是分布式可以使用
# RDBMS 数据库，
# MongoDB
#
# Redis
#
# RethinkDB
#
# ZooKeeper

class ScheduleServer(object):
    def __init__(self, crontab='0 */1 * * *'):
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        # 默认整点执行一次
        self.crontab = crontab
        # 后期支持分布式
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.sync, CronTrigger.from_crontab(self.crontab))

    def sync(self):
        # 同步api
        # 同步数据库
        ...

    def start(self):
        self.scheduler.start()
