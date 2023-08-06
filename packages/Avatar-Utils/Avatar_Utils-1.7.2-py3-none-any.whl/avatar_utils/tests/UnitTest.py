import logging
from unittest import TestCase

from avatar_utils.tests.AbstractApp import AbstractApp

logger = logging.getLogger(__name__)


class UnitTest(TestCase, AbstractApp):
    app = None
    db = None

    def setUp(self):
        TestCase.setUp(self)
        try:
            print('SQLALCHEMY_DATABASE_URI: %s' % self.app.config['SQLALCHEMY_DATABASE_URI'])
        except KeyError:
            pass

        self.assertTrue(self.app)
        self.assertTrue(self.client)
        self.assertTrue(self.app.config['TESTING'])

        self.app_context = self.app.app_context()
        self.app_context.push()

        if self.db:
            self.db.create_all()

        super().setUp()

    def tearDown(self):
        if self.db:
            self.db.session.remove()
            self.db.drop_all()

        self.app_context.pop()

        TestCase.tearDown(self)
