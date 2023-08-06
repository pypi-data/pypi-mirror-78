# -*- coding: utf8 -*-
# Copyright (c) 2018-2020 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import traceback
import os
from importlib import import_module

from ti_containers import constant
from ti_containers import utils
from ti_containers.config import Config
from ti_containers.exception import RunUserEntrypointError
from ti_containers.executer import (
    Worker,
    MPILanucher,
    MPIWorker,
)
from ti_containers.utils import get_logger, configure_logger

logger = get_logger()


def framework_training(config):
    framework = config.training_framework
    logger.info('Training framework %s load', framework)

    module = "ti_containers." + framework.lower() + ".prepare"
    worker = getattr(import_module(module), "run")
    worker(config).run()


def common_training(config):
    logger.info('Training entry point load')

    if config.mpi_enabled:
        if config.is_master:
            executor = MPILanucher(config)
        else:
            executor = MPIWorker(config)
    else:
        executor = Worker(config)

    executor.run()


def main():
    try:
        # config load
        config = Config()
        config.load()

        # set log level
        configure_logger(config.log_level)

        # train start
        if config.training_framework and not config.mpi_enabled:
            framework_training(config)
        else:
            common_training(config)

        logger.info("Training success")
        utils.write_file(constant.OUTPUT_SUCCESS_PATH, "success")
    except RunUserEntrypointError as e:
        error_msg = "Run error: \n%s\n" % (str(e))
        logger.error(error_msg)
        utils.write_file(constant.OUTPUT_FAILURE_PATH, error_msg)
        os._exit(1)
    except Exception as e:
        error_msg = "Training error: \n%s\n" % (str(e))
        logger.error(error_msg)
        utils.write_file(constant.OUTPUT_FAILURE_PATH, error_msg)
        os._exit(1)
