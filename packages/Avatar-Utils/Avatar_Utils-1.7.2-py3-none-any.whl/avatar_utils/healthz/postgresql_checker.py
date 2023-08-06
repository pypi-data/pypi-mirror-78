from logging import getLogger

from flask_sqlalchemy import SQLAlchemy

from avatar_utils.healthz.checker_base import CheckerBase

logger = getLogger(__name__)


class PostgresqlChecker(CheckerBase):

    def __init__(self, db: SQLAlchemy):
        super(PostgresqlChecker, self).__init__(name='postgresql', db=db)

    def checker(self, db: SQLAlchemy) -> bool:
        is_passed: bool = False

        try:
            a = db.engine.execute('SELECT 1')
            is_passed = True
        except Exception as err:  # noqa
            logger.error('Health check failed:\n{err}')

        return is_passed
