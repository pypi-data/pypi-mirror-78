import logging
import time
import uuid
from logging.config import dictConfig

from .kfproducer import push_to_queue
from .eswrapper import index_error_to_es
from .loghandler import log_exception
from .config import anu_etl_wf_error_topic
from .config import es_url

log = logging.getLogger('file')


# Method to standardize and index errors for the core flow
# code: Any string that uniquely identifies an error
# message: The error message
# cause: JSON or String that explains the cause of the error
def post_error(code, message, cause):
    try:
        error = {
            "errorID": generate_error_id(),
            "code": code,
            "message": message,
            "timeStamp": eval(str(time.time()).replace('.', '')),
            "errorType": "core-error"
        }
        if cause is not None:
            error["cause"] = str(cause)
        if es_url != 'localhost':
            index_error_to_es(error)
        return error
    except Exception as e:
        log_exception("Error Handler Failed.", None, e)
        return None


# Method to standardize, post and index errors for the workflow.
# code: Any string that uniquely identifies an error
# message: The error message
# cause: JSON or String that explains the cause of the error
# jobID: Unique JOB ID generated for the wf.
# taskID: Unique TASK ID generated for the current task.
# state: State of the workflow pertaining to the current task.
# status: Status of the workflow pertaining to the current task.
def post_error_wf(code, message, entity, cause):
    try:
        error = {
            "errorID": generate_error_id(),
            "code": code,
            "message": message,
            "timeStamp": eval(str(time.time()).replace('.', '')),
            "status": "FAILED",
            "errorType": "wf-error"
        }
        if cause is not None:
            error["cause"] = str(cause)
        if entity["jobID"]:
            error["jobID"] = entity["jobID"]
        if entity["taskID"]:
            error["taskID"] = entity["taskID"]
        if entity["state"]:
            error["state"] = entity["state"]
        if entity["status"]:
            error["status"] = entity["status"]
        if entity["metadata"] is not None:
            error["metadata"] = entity["metadata"]

        if es_url != 'localhost':
            push_to_queue(error, anu_etl_wf_error_topic)
            index_error_to_es(error)
        return error
    except Exception as e:
        log_exception("Error Handler WF Failed.", None, e)
        return None


# Method to generate error ID.
def generate_error_id():
    return str(uuid.uuid4())

# Log config
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] {%(filename)s:%(lineno)d} %(threadName)s %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'info': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'filename': 'info.log'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {
        'file': {
            'level': 'DEBUG',
            'handlers': ['info', 'console'],
            'propagate': ''
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['info', 'console']
    }
})
