# -*- coding: utf-8 -*-

import gevent
import requests

from locust import constant
from locust.argument_parser import get_parser
from locust.user import User, task
from locust.test.testcases import LocustTestCase

from locust_plugin_result import set_result, RESULT_FAIL, add_listener


class TestWebUI(LocustTestCase):
    def setUp(self):
        super(TestWebUI, self).setUp()

        parser = get_parser(default_config_files=[])
        self.environment.parsed_options = parser.parse_args([])
        self.stats = self.environment.stats

        self.web_ui = self.environment.create_web_ui("127.0.0.1", 0)
        self.web_ui.app.view_functions["request_stats"].clear_cache()

        # This is run when plugin is imported (normally in locustfile.py) but the locust_plugin_result import here happens before
        # locust initialization, so execute again here
        add_listener()

        # Fire locust init event which is normally done in main, after import of locustfile.py
        self.environment.events.init.fire(environment=self.environment, runner=self.runner, web_ui=self.web_ui)

        gevent.sleep(0.01)
        self.web_port = self.web_ui.server.server_port

    def tearDown(self):
        super(TestWebUI, self).tearDown()
        self.web_ui.stop()
        self.runner.quit()

    def test_status_result_is_not_set(self):
        response = requests.get("http://127.0.0.1:%i/status" % self.web_port)
        print('response', response.text)
        self.assertEqual(200, response.status_code)
        assert response.json() == {'result': None, 'state': 'ready', 'worker_count': None, 'user_count': 0}

    def test_status_result_is_set(self):
        class MyUser(User):
            wait_time = constant(1)
            @task(1)
            def my_task(self):
                pass
        self.environment.user_classes = [MyUser]

        response = requests.post(
            "http://127.0.0.1:%i/swarm" % self.web_port,
            data={'user_count': 5, 'spawn_rate': 5},
        )
        self.assertEqual(200, response.status_code)

        reason = 'Oops'
        set_result(self.runner, RESULT_FAIL, reason)
        response = requests.get("http://127.0.0.1:%i/status" % self.web_port)
        print('response', response.text)
        self.assertEqual(200, response.status_code)

        result = response.json()['result']
        assert result['value'] == RESULT_FAIL
        assert result['reason'] == reason

        worker_count = response.json()['worker_count']
        assert worker_count == None
