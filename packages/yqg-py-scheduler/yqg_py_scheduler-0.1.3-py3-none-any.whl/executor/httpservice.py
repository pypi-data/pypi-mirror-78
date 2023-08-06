import importlib
import json
import logging
import random
import string
import time

from flask import Flask, request, current_app, g, has_request_context
from kazoo.client import KazooClient
from werkzeug.serving import make_server

from executor.app import ExecutorApplication
from executor.executor import TriggerState, Executor, DefaultJobFactory
from executor.notifier import Notifier
from executor.scheduler import Scheduler


class TracingFilter(logging.Filter):

    def filter(self, record):
        if has_request_context():
            if hasattr(g, 'trace_id'):
                record.trace_id = g.trace_id
            else:
                record.trace_id = '-'
        else:
            record.trace_id = '-'
        return True


class HttpService(object):
    """
    在ExecutorApplication的基础上，增加一层http接口
    """

    def __init__(self, id, params):
        self._populate_defaults(params)
        self._id = id
        self._app = self._init_app(params)
        self._flask = self._init_flask(params)
        self._server = self._init_wsgi_server(self._flask, params)

    def _populate_defaults(self, params):
        # backfil default values
        defaults = {
            'zookeeper.hosts': "localhost:2181",
            'zookeeper.conn_timeout': 10,
            'executor.threads_count': 16,
            'executor.job_factory': DefaultJobFactory(),
            'http.host': "localhost",
            'http.port': "8080"
        }
        for key, value in defaults.items():
            if key not in params:
                params[key] = value

    def _init_app(self, params):

        # init zk
        zk = KazooClient(hosts=params["zookeeper.hosts"], timeout=params['zookeeper.conn_timeout'])

        # init executor
        executor = Executor(
            threads_count=params["executor.threads_count"],
            job_factory=params["executor.job_factory"]
        )

        # init yqg-py-scheduler
        scheduler = Scheduler()

        # init notifier
        notifier = Notifier(scheduler)

        # init app
        id = "%s#%s:%s" % (self._id, params["http.host"], params["http.port"])
        return ExecutorApplication(id, zk, executor, scheduler, notifier)

    def _init_flask(self, params):
        flask = Flask("yqg-py-scheduler")

        # configure flask routing
        flask.add_url_rule("/executor/trigger", endpoint="trigger", view_func=self.trigger, methods=["POST"])
        flask.add_url_rule("/executor/interrupt", endpoint="interrupt", view_func=self.interrupt, methods=["POST"])
        flask.add_url_rule("/executor/isRunning", endpoint="isRunning", view_func=self.is_trigger_running, methods=["POST"])
        flask.add_url_rule("/executor/isJobExists", endpoint="jobExists", view_func=self.job_exists, methods=["POST"])
        flask.add_url_rule("/executor/listTasks", endpoint="listTasks", view_func=self.list_triggers, methods=["POST"])

        def set_trace_id():
            g.trace_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))

        def clear_trace_id(error):
            g.trace_id = None

        def log_request_start():
            current_app.logger.info("[%s] %s %s" % (request.remote_addr, request.method, request.full_path))

        def log_request_finish(error):
            if error:
                current_app.logger.info("request threw exception")
            else:
                current_app.logger.info("request finished")

        def handle_exceptions(ex):
            current_app.logger.exception(ex)
            return {
                "status": {
                    "code": 10001,
                    "detail": "",
                    "serverResponseTime": int(time.time() * 1000)
                },
                "body": str(ex)
            }

        # configure interceptors
        flask.before_request(set_trace_id)
        flask.before_request(log_request_start)
        flask.teardown_request(clear_trace_id)
        flask.teardown_request(log_request_finish)

        # configure error handler
        flask.register_error_handler(Exception, handle_exceptions)

        # disable werkzeug logging
        logging.getLogger('werkzeug').disabled = True

        return flask

    def _init_wsgi_server(self, flask, params):
        # 目前就用werkzeug自带的简易wsgi server，也够用
        return make_server(
            host=params["http.host"],
            port=params["http.port"],
            app=flask,
            threaded=True
        )

    def serve(self):
        self._app.start()
        self._server.serve_forever()

    def shutdown(self):
        self._server.shutdown()
        self._app.shutdown(timeout=60)

    def trigger(self):
        # {
        #     "schedulerInfo": {
        #         "address": "172.20.64.12:7039",
        #         "epoch": 53,
        #         "timeUpdated": 1594102627173
        #     },
        #     "body": {
        #         "jobId": 2686,
        #         "triggerId": 7229247,
        #         "timeStamp": 1594328401941,
        #         "jobName": "YueCaiFundingStateScanJob",
        #         "className": "com.yqg.yqg-py-scheduler.jobs.FundingStateScanJob",
        #         "params": "{\"providerTypes\":[\"YUE_CAI_LOAN\"]}"
        #     }
        # }
        data = request.get_json()
        if 'params' in data["body"]:
            params = json.loads(data["body"]["params"])
        else:
            params = {}

        self._app.trigger(
            data["schedulerInfo"]["epoch"],
            data["body"]["triggerId"],
            data["body"]["jobId"],
            data["body"]["jobName"],
            data["body"]["className"],
            params
        )

        return {
            "status": {
                "code": 0,
                "detail": "成功",
                "serverResponseTime": int(time.time() * 1000)
            }
        }

    def interrupt(self):
        # {
        #     "schedulerInfo": {
        #         "address": "172.20.64.12:7039",
        #         "epoch": 53,
        #         "timeUpdated": 1594102627173
        #     },
        #     "body": 7306466   // body中直接为trigger对应的id值
        # }
        data = request.get_json()
        self._app.interrupt(data["schedulerInfo"]["epoch"], data["body"])

        return {
            "status": {
                "code": 0,
                "detail": "成功",
                "serverResponseTime": int(time.time() * 1000)
            },
            "body": True
        }

    def is_trigger_running(self):
        # {
        #     "schedulerInfo": {
        #         "address": "172.20.64.12:7039",
        #         "epoch": 53,
        #         "timeUpdated": 1594102627173
        #     },
        #     "body": 7306466   // body中直接为trigger对应的id值
        # }
        data = request.get_json()
        trigger = self._app.list_triggers(data["schedulerInfo"]["epoch"], trigger_id=data["body"])
        return {
            "status": {
                "code": 0,
                "detail": "成功",
                "serverResponseTime": int(time.time() * 1000)
            },
            "body": trigger.state() == TriggerState.RUNNING
        }

    def job_exists(self):
        # {
        #     "schedulerInfo": {
        #         "address": "172.20.64.12:7039",
        #         "epoch": 53,
        #         "timeUpdated": 1594102627173
        #     },
        #     "body": "com.yqg.yqg-py-scheduler.jobs.FundingStateScanJob"
        # }
        data = request.get_json()

        try:
            tokens = data['body'].split(".")
            module_name = ".".join(tokens[0:(len(tokens) - 1)])
            class_name = tokens[len(tokens) - 1]
            module = importlib.import_module(module_name)
            class_exists = hasattr(module, class_name)
        except:
            class_exists = False

        return {
            "status": {
                "code": 0,
                "detail": "成功",
                "serverResponseTime": int(time.time() * 1000)
            },
            "body": class_exists
        }

    def list_triggers(self):
        # {
        #     "schedulerInfo": {
        #         "address": "172.20.64.12:7039",
        #         "epoch": 53,
        #         "timeUpdated": 1594102627173
        #     },
        #     "body": ""
        # }
        data = request.get_json()

        body = []
        triggers = self._app.list_triggers(data["schedulerInfo"]["epoch"])
        for id, t in triggers.items():
            body.append({
                "triggerId": t.id(),
                "jobName": ".".join([t.job().__module__, type(t.job()).__name__]),
                "params": json.dumps(t.params()),
                "status": t.state().value
            })

        return {
            "status": {
                "code": 0,
                "detail": "成功",
                "serverResponseTime": int(time.time() * 1000)
            },
            "body": body
        }