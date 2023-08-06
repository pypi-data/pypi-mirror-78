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
import json
import multiprocessing
import tensorflow as tf

from ti_containers import constant
from ti_containers import utils
from ti_containers.executer import Worker
from ti_containers.utils import get_logger

logger = get_logger()

def _build_config(config):
    master, ps, workers = config.hosts[0], config.hosts[0], config.hosts[1:]
    tf_config = {
        'cluster': {
            'master': ['{}:{}'.format(master, constant.TF_WORKER_PORT)],
            'ps': ['{}:{}'.format(ps, constant.TF_PS_PORT)],
            'worker': ['{}:{}'.format(host, constant.TF_WORKER_PORT) for host in workers],
        },
        'environment': 'cloud'
    }

    if config.is_master:
        tf_config['task'] = {'index': 0, 'type': 'master'}
    else:
        tf_config['task'] = {'index': workers.index(config.current_host), 'type': 'worker'}

    return tf_config


def _run_ps_server(tf_config):
    cluster_spec = tf.train.ClusterSpec(tf_config['cluster'])
    if tf.__version__ < '2.0.0':
        config = tf.ConfigProto(device_count={'GPU': 0})
        server = tf.train.Server(cluster_spec, job_name='ps', task_index=0, config=config)
    else:
        config = tf.compat.v1.ConfigProto(device_count={'GPU': 0})
        server = tf.distribute.Server(cluster_spec, job_name='ps', task_index=0, config=config)

    multiprocessing.Process(target=lambda: server.join()).start()


def run(config):
    logger.info('DNS lookups begin')
    for host in config.hosts:
        utils.dns_lookup(host)

    if config.parameter_server_enabled and len(config.hosts) > 1:
        tf_config = _build_config(config)
        os.environ["TF_CONFIG"] = json.dumps(tf_config)
        if config.is_master:
            _run_ps_server(tf_config)

    return Worker(config)
