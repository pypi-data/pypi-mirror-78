"""aiokafkadaemon: framework for daemonized apps using kafka with AsyncIO"""
import json
import logging
import logging.config
import os
import urllib.request

from .daemon import Daemon, default_exit_handler
from .worker import Worker


def setup_logging(loglevel="INFO"):
    log_format = "%(asctime)s [%(levelname)s] %(name)s => %(message)s"
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"info_format": {"format": log_format}},
            "handlers": {
                "console": {
                    "level": loglevel,
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "formatter": "info_format",
                },
            },
            "loggers": {"": {"handlers": ["console"], "level": loglevel}},
        }
    )


def retrieve_ecs_metadata():
    # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-metadata-endpoint-v3.html#task-metadata-endpoint-v3-response
    if not os.getenv("ECS_CONTAINER_METADATA_URI"):
        return None

    try:
        with urllib.request.urlopen(
            os.getenv("ECS_CONTAINER_METADATA_URI")
        ) as response:
            ecs_info = json.loads(response.read().decode())

        task_arn = ecs_info["Labels"]["com.amazonaws.ecs.task-arn"]
        cluster = ecs_info["Labels"]["com.amazonaws.ecs.cluster"]
        region = task_arn.split(":")[3].split("-")[0]

        return {
            "region": region,
            "cluster": cluster,
            "task_arn": task_arn,
            "task": task_arn.split("/")[-1],
            "environment": f"{region}_{cluster}",  # environment is user-defined used for easy external logging
        }

    except Exception as e:
        logging.error(e)

        return None
