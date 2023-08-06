import copy
import logging
from unittest import TestCase

from avatar_utils.tests.RemoteApp import RemoteApp

logger = logging.getLogger(__name__)


class IntegrationTest(TestCase, RemoteApp):

    def setUp(self):
        super().setUp()

        # reset current env
        self.current_env = copy.deepcopy(RemoteApp.default_env)
