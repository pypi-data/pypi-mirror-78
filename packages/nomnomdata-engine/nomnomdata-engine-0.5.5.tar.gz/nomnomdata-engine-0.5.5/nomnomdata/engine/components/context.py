import json
import logging
import re
from os import environ
from pprint import pformat

from httmock import HTTMock, urlmatch
from wrapt import ObjectProxy


class NominodeContextMock(HTTMock):
    def __init__(self, task_parameters=None):
        super().__init__(self.api_match)
        self.logger = logging.getLogger("nomigen.nominode-mock")
        task_parameters = task_parameters or {}
        self.secrets = task_parameters.pop("config", {})
        self.params = task_parameters
        self.calls = []
        self.environ = None

    def __enter__(self):
        self.environ = environ.copy()
        environ["execution_uuid"] = "TEST_UUID"
        environ["task_uuid"] = "TASK_UUID"
        environ["project_uuid"] = "TEST_PROJECT"
        environ["nomnom_api"] = "http://127.0.0.1:9090"
        environ["token"] = "token"
        self.nnd_context = NominodeContext.from_env()
        self.nnd_context.__enter__()
        super().__enter__()
        return self

    def __exit__(self, *args):
        self.nnd_context.__exit__(*args)
        super().__exit__(*args)
        environ.pop("execution_uuid")
        environ.pop("task_uuid")
        environ.pop("project_uuid")
        environ.pop("nomnom_api")
        environ.pop("token")

    @urlmatch(netloc=r"(.*\.)?127.0.0.1:9090$")
    def api_match(self, url, request):
        self.calls.append((url.path, json.loads(request.body)))
        match = re.match(r"/connection/(?P<uuid>.+)/update", url.path)
        if match:
            json_data = request.body
            loaded = json.loads(json_data)
            uuid = match.groupdict()["uuid"]
            self.params["config"][uuid] = json.loads(loaded["parameters"])
            self.logger.debug("Caught connections update. Test creds updated")
        elif url.path == "/execution/log/TEST_UUID":
            json_data = request.body
            loaded = json.loads(json_data)
        elif url.path == "/task/TASK_UUID/update":
            json_data = request.body
            loaded = json.loads(json_data)
            self.logger.debug("Caught task update {}".format(pformat(loaded)))
        elif url.path == "/execution/update/TEST_UUID":
            json_data = request.body
            loaded = json.loads(json_data)
            self.logger.debug(
                "Caught execution progress update {}".format(pformat(loaded))
            )
        elif url.path == "/execution/decode/TEST_UUID":
            return json.dumps(self.secrets)
        elif url.path == "/task/TASK_UUID/parameters":
            json_data = request.body
            loaded = json.loads(json_data)
            self.logger.debug("Caught task parameter update {}".format(pformat(loaded)))
            return json.dumps({"result": "success"})
        elif url.path == "/execution/checkout/TEST_UUID":
            return json.dumps({"parameters": self.params, "task_uuid": "TASK_UUID"})
        else:
            self.logger.info(
                f"Unknown api endpoint called {url.path}, \n Body {request.body}"
            )
        return '{"you_logged":"test"}'


class NominodeContext:
    def __init__(self, execution_uuid, task_uuid, project_uuid, nomnom_api, token):
        self.execution_uuid = execution_uuid
        self.task_uuid = task_uuid
        self.project_uuid = project_uuid
        self.nomnom_api = nomnom_api
        self.token = token
        self.api_mock = NoContext()

    def __enter__(self):
        nominode_ctx._set_nominode_context(self)
        return self

    def __exit__(self, *args):
        nominode_ctx._set_nominode_context(NoContext())

    @classmethod
    def from_env(cls):
        try:
            instance = cls(
                execution_uuid=environ["execution_uuid"],
                task_uuid=environ["task_uuid"],
                project_uuid=environ["project_uuid"],
                nomnom_api=environ["nomnom_api"],
                token=environ["token"],
            )
        except KeyError as e:
            raise RuntimeError(
                f"Could not find expected environment variable '{e.args[0]}'"
            )
        return instance


class NoContext:
    def __getattr__(self, name):
        if name in ["execution_uuid", "task_uuid", "project_uuid", "nomnom_api", "token"]:
            raise RuntimeError(
                "Not in nominode context, wrap with ExecutionContextMock or only execute via a nominode"
            )
        else:
            return super().__getattribute__(name)


class NominodeContextProxy(ObjectProxy):
    def __init__(self):
        super().__init__(None)

    def _set_nominode_context(self, nominode_ctx):
        super().__init__(nominode_ctx)


nominode_ctx: NominodeContext = NominodeContextProxy()
