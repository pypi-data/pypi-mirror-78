import requests

from avatar_utils.tests import RemoteApp
from avatar_utils.tests.BaseUnitTest import BaseUnitTest


class WithLoggedUser(BaseUnitTest):
    # test user credentials
    username = None
    password = None

    # actual test user id in used database
    test_token = None
    id_test_user = None

    def setUp(self):
        super().setUp()

        backend_url = self.app.config['BACKEND_URL']

        # login user
        response = RemoteApp.convert_to_flask_response(
            requests.post(f'{backend_url}/login', json=dict(username=self.username, password=self.password)))
        self.rprint(response)

        token = response.json['result']['token']
        self.test_token = token

        # get user_id
        response = RemoteApp.convert_to_flask_response(
            requests.get(f'{backend_url}/user', headers={'Authorization': f'Bearer {token}'}, verify=False))
        self.rprint(response)

        self.id_test_user = response.json['result']['id']['value']
        print(f'id_test_user = {self.id_test_user}')

        # add a token to headers
        auth_header = {'Authorization': f'Bearer {self.test_token}'}
        self.headers = {**self.headers, **auth_header}
