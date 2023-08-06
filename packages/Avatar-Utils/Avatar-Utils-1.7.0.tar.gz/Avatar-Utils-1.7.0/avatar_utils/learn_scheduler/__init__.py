import atexit
from logging import getLogger
from typing import Any

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

logger = getLogger()


class BaseLearnScheduler:

    def __init__(self, app: Flask, learn_func: Any, learn_args: Any = ()):
        self.app = app
        self.learn_func = learn_func
        self.learn_args = learn_args

        if app.config.get('LEARN_SCHEDULE'):
            self.schedule_learn()
        if app.config.get('LEARN_RUN_AT_START'):
            self.run_learn()

    def cron_trigger_args(self):
        trigger_args = {'day': self.app.config.get('LEARN_DAY'),
                        'day_of_week': self.app.config.get('LEARN_DAY_OF_WEEK'),
                        'hour': self.app.config.get('LEARN_HOUR'),
                        'minute': self.app.config.get('LEARN_MINUTE')}
        return dict((arg, value) for arg, value in trigger_args.items() if value is not None)

    def interval_trigger_args(self):
        trigger_args = {'days': self.app.config.get('LEARN_DAYS'),
                        'hours': self.app.config.get('LEARN_HOURS'),
                        'minutes': self.app.config.get('LEARN_MINUTES'),
                        'seconds': self.app.config.get('LEARN_SECONDS'),
                        'start_date': self.app.config.get('LEARN_START_DATE'),
                        'end_date': self.app.config.get('LEARN_END_DATE')}
        return dict((arg, value) for arg, value in trigger_args.items() if value is not None)

    def schedule_learn(self):
        scheduler = BackgroundScheduler()
        args_dict = {
            'cron': self.cron_trigger_args,
            'interval': self.interval_trigger_args
        }

        try:
            trigger = self.app.config.get('LEARN_TRIGGER')
            trigger_args = args_dict[trigger]()
        except ValueError as err:
            logger.error(err)
            return

        scheduler.add_job(func=self.learn_func, args=self.learn_args, trigger=trigger, **trigger_args)

        scheduler.start()
        atexit.register(lambda: scheduler.shutdown())
        logger.debug(f'Learn scheduled')

    def run_learn(self):
        self.learn_func(*self.learn_args)
