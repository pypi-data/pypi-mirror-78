import json
import os
from datetime import datetime
from logging import getLogger
from pathlib import Path
from time import sleep
from typing import Optional

import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import app_path
from .models import CrawlerTask

logger = getLogger()


class BaseCrawlerAdapter():
    tasks_path: Path = app_path.joinpath('crawling', 'tasks')

    @property
    def crawler_create_task_url(self):
        return f'{self.crawler_url}/task/create'

    @property
    def crawler_run_task_url(self):
        return f'{self.crawler_url}/task/run'

    @property
    def crawler_task_status_url(self):
        return f'{self.crawler_url}/task/status'

    @property
    def crawler_data_url(self):
        return f'{self.crawler_url}/data/get'

    def __init__(self, app: Flask, db: SQLAlchemy, tasks_path: Path = app_path.joinpath('crawling', 'tasks')):
        self.app = app
        self.db = db
        self.tasks_path = tasks_path

        self.crawler_url = app.config.get('CRAWLER_URL')

        logger.debug(f'CrawlerAdapter created')

        if app.config.get('CRAWLER_ADD_TASKS'):
            self.__add_tasks()
            logger.debug(f'Tasks from {self.tasks_path} added')

    def __add_tasks(self) -> None:
        logger.debug(f'Scan {self.tasks_path} directory')

        with os.scandir(self.tasks_path) as entries:
            entry: os.DirEntry
            for entry in entries:
                with open(entry, mode='r', encoding='utf8') as file:
                    task_body = json.load(file)
                    task_name = task_body.get('name')
                    if not task_name:
                        logger.error(f'Cannot import task from file {file.name}. Specify task name in task.name')
                        continue

                    self.__create_crawler_task(task_name=task_name, task_body=task_body)

    def __create_crawler_task(self, task_name: str, task_body: str) -> None:
        response = requests.post(self.crawler_create_task_url, json=task_body)

        if response.status_code != 200:
            logger.warning(f'Response status is {response.status_code}: Payload: {response.text}')

        data = response.json()
        if data:
            task_id = data['result']['id']

            crawler_task: CrawlerTask = CrawlerTask.query.filter_by(name=task_name).first()
            if not crawler_task:
                crawler_task = CrawlerTask()
                crawler_task.name = task_name
                self.db.session.add(crawler_task)

            crawler_task.task_id = task_id
            crawler_task.task_body = json.dumps(task_body)
            self.db.session.commit()

            logger.debug(f'Task {task_name} added')
        else:
            logger.warning('Response data is empty')

    def __run_task(self, crawler_task: CrawlerTask) -> None:
        task = json.loads(crawler_task.task_body)
        task['task_id'] = crawler_task.task_id

        response = requests.post(self.crawler_run_task_url, json=task)

        if response.status_code != 200:
            logger.error(f'Run task is not succeed. Status {response.status_code}. Payload: {response.text}')

        logger.debug(response.text)

    def __wait_until_task_finish(self, crawler_task: CrawlerTask, timeout: int) -> None:
        data = {
            'task_id': crawler_task.task_id
        }

        while True:
            response = requests.post(self.crawler_task_status_url, json=data)

            if response.status_code != 200:
                logger.warning(f'Check task status is not succeed. Status {response.status_code}. Payload: {response.text}')
            logger.debug(response.text)

            status = response.json()['result']['status']
            logger.debug(f'{crawler_task.name} task status: {status}')
            if status == 'in_db':
                break

            sleep(timeout)

    def __fetch(self, crawler_task: CrawlerTask, limit: int, last_crawled: Optional[int] = None) -> dict:
        task = {
            'task_id': crawler_task.task_id,
            'start_ts': last_crawled if last_crawled is not None else crawler_task.last_crawled
        }
        if limit:
            task['limit'] = limit

        response = requests.post(self.crawler_data_url, json=task)

        data = response.json()['result']['data']

        logger.info(f'Crawled {len(data)} pieces of data')
        ctimes = [item.get('ctime') for item in data if item.get('ctime')]
        if ctimes:
            last_crawled = max(ctimes)
            logger.debug(f'last_crawled is {str(datetime.fromtimestamp(last_crawled))}')
            if last_crawled:
                crawler_task.last_crawled = last_crawled

        self.db.session.add(crawler_task)
        self.db.session.commit()

        return data

    def data(self, task_name: str, limit=None, timeout: int = 15, last_crawled: Optional[int] = None,
             run_task: Optional[bool] = None, wait_until_task_finish: Optional[bool] = None) -> dict:
        crawler_task: CrawlerTask = CrawlerTask.query.filter_by(name=task_name).first()
        if not crawler_task:
            raise KeyError(f'task {task_name} does not exist')

        logger.debug(f"run_task: parameter is {run_task}, config is {self.app.config.get('CRAWLER_RUN_TASK')}")

        if run_task is True or \
                (run_task is None and self.app.config.get('CRAWLER_RUN_TASK') is True):
            logger.debug('running __run_task')
            self.__run_task(crawler_task=crawler_task)

        logger.debug(f"wait_until_task_finish: parameter is {wait_until_task_finish}, "
                     f"config is {self.app.config.get('CRAWLER_WAIT_UNTIL_TASK_FINISH')}")

        if wait_until_task_finish is True or \
                (wait_until_task_finish is None and self.app.config.get('CRAWLER_WAIT_UNTIL_TASK_FINISH') is True):
            logger.debug('running __wait_until_task_finish')
            self.__wait_until_task_finish(crawler_task=crawler_task, timeout=timeout)

        data = self.__fetch(crawler_task=crawler_task, limit=limit, last_crawled=last_crawled)

        return data
