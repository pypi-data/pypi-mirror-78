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

import os
import subprocess

from ti_containers import constant
from ti_containers.executer import Worker
from ti_containers.utils import (
    dns_lookup,
    get_logger
)

logger = get_logger()

def _run_process(hosts):
    os.environ['DMLC_NUM_WORKER'] = str(len(hosts))
    os.environ['DMLC_NUM_SERVER'] = str(len(hosts))
    os.environ['DMLC_PS_ROOT_URI'] = dns_lookup(hosts[0])
    os.environ['DMLC_PS_ROOT_PORT'] = str(constant.MXNET_PS_PORT)
    os.environ['PS_VERBOSE'] = str(constant.MXNET_PS_VERBOSE)

    subprocess.Popen("python -c 'import mxnet'", shell=True, env=os.environ).pid


def run(config):
    logger.info('DNS lookups begin')
    for host in config.hosts:
        dns_lookup(host)

    if config.parameter_server_enabled and len(config.hosts) > 1:
        if config.is_master:
            os.environ['DMLC_ROLE'] = 'scheduler'
            _run_process(config.hosts)

        os.environ['DMLC_ROLE'] = 'server'
        _run_process(config.hosts)

        os.environ['DMLC_ROLE'] = 'worker'

    return Worker(config)
