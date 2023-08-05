# -*- coding: utf-8 -*-

from flask import jsonify
import locust


def add_listener():
    @locust.events.init.add_listener
    def on_locust_init(web_ui, **kw):
        @web_ui.app.route("/status")
        @web_ui.auth_required_if_enabled
        def status():
            runner = web_ui.environment.runner
            return jsonify({
                "state": runner.state,
                "result": getattr(runner, 'result', None),
                "worker_count": getattr(runner, 'worker_count', None),  # 'worker_count' does not exist for LocalRunner
                "user_count": runner.user_count,
            })
