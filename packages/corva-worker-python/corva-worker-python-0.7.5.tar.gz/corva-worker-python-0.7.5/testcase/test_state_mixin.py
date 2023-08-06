import importlib
import os
import time
import unittest

import testcase.state_testing_app.app_constants
from testcase.state_testing_app.app_constants import constants
from testcase.state_testing_app.app_lambda import lambda_handler


class TestStateMixin(unittest.TestCase):
    def test_state_mixin(self):
        importlib.reload(constants)
        importlib.reload(testcase.state_testing_app.app_constants)
        asset_id = 29399830

        os.environ["LOGGING_ASSET_ID"] = str(asset_id)
        os.environ["LOGGING_LEVEL"] = "debug"
        os.environ["STATE_STORAGE_CRITICAL_LIMIT"] = "10"
        event = [{
            "asset_id": asset_id,
            "timestamp": 2
        }]
        start_timer = time.time()
        lambda_handler(event, None)
        print(f"Finished testing StateMixin in {int(time.time() - start_timer)} seconds.")
