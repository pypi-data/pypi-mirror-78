TEMPLATE_APP = """
import azure.functions as func
from paten import Paten

app = Paten('%s')


@app.http_trigger('req', methods=['GET'], route='/http')
@app.out_http()
def example_http_function(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get('name')
    
    # response
    return func.HttpResponse(name)


@app.http_trigger('req', methods=['GET'], route='/queue')
@app.out_queue('your_queue', queue_name='example_queue')
@app.out_http()
def example_http_queue_function(req: func.HttpRequest, your_queue: func.Out[str]) -> func.HttpResponse:
    name = req.params.get('name')
    # set name in your queue
    your_queue.set(name)
    
    # response
    return func.HttpResponse(name)
    
"""


GITIGNORE = """
.paten/*
"""


WELCOME_PROMPT = r"""
 _____             _______  ______  _   _
|  __ \     /\    |__   __||  ____|| \ | |
| |__) |   /  \      | |   | |__   |  \| |
|  ___/   / /\ \     | |   |  __|  | . ` |
| |      / ____ \    | |   | |____ | |\  |
|_|     /_/    \_\   |_|   |______||_| \_|

Welcome PATEN.
Your function app `%s` is generated
"""