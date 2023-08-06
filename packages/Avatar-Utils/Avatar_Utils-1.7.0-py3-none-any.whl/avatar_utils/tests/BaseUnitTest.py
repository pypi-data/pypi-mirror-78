import logging

from avatar_utils.tests.UnitTest import UnitTest

logger = logging.getLogger(__name__)


class BaseUnitTest(UnitTest):
    from app import create_app, db

    app = create_app('testing')
    client = app.test_client()
    db = db
