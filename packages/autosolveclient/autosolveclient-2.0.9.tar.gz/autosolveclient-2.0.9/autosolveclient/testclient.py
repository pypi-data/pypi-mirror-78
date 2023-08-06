import time
from threading import Thread

from autosolveclient.autosolve import AutoSolve


def send_message():
    message = {
        "taskId": 6,
        "url": "https://recaptcha.autosolve.io/version/1",
        "siteKey": "6Ld_LMAUAAAAAOIqLSy5XY9-DUKLkAgiDpqtTJ9b",
        "version": 0,
        "minScore": 0,
    }
    auto_solve.send_token_request(message)

try:
    auto_solve_factory = AutoSolve({
        "access_token": "user-access-token",
        "api_key": "user-api-key",
        "client_key": "your-client-key",
        "debug": True,
        "should_alert_on_cancel": True
    })

    auto_solve = auto_solve_factory.get_instance()
    auto_solve.init()
    finished = auto_solve.initialized()

    time.sleep(1)
    send_message()
    send_message()
    send_message()


except Exception as s:
    print(s)