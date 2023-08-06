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

import json
import logging
import os

import six
from ti_containers import constant
from ti_containers import utils


class Config(object):
    def load(self):
        # parse hyperparameters
        hps = utils.read_json_file(constant.HYPERPARAMETERS_PATH)
        hps = utils.format_hyperparameters(hps)
        extend_hps, train_hps = utils.extract_hyperparameters(hps, constant.TI_PREFIX)

        if os.environ.get('OMPI_MCA_btl_tcp_if_include'):
            self.network_interface_name = os.environ.get('OMPI_MCA_btl_tcp_if_include')
        else:
            self.network_interface_name = extend_hps.get(constant.TI_NETWORK_INTERFACE_NAME, constant.DEFAULT_NIC_NAME)
        self.log_level = extend_hps.get(constant.TI_CONTAINER_LOG_LEVEL, logging.INFO)
        self.user_entry_point = extend_hps.get(constant.TI_PROGRAM, '')
        self.parameter_server_enabled = extend_hps.get(constant.TI_PARAMETER_SERVER_ENABLED, '')
        self.mpi_enabled = extend_hps.get(constant.TI_MPI_ENABLED, '')
        self.mpi_process_per_host = extend_hps.get(constant.TI_MPI_NUM_OF_PROCESSES_PER_HOST, '')
        self.custom_mpi_options = extend_hps.get(constant.TI_MPI_CUSTOM_MPI_OPTIONS, '')

        self.train_hps = train_hps

        # parse input data config
        input_data_config = utils.read_json_file(constant.INPUT_DATA_CONFIG_PATH)
        self.input_channels = {v: os.path.join(constant.INPUT_CHANNLE_PATH, v) for v in input_data_config}

        # parse resource config
        resource_config = utils.read_json_file(constant.RESOURCE_CONFIG_PATH)
        self.hosts = resource_config[constant.HOSTS]
        self.mpi_operator_submit = resource_config.get(constant.MPI_OPERATOR_SUBMIT, False)
        if self.mpi_operator_submit:
            self.current_host = self.hosts[int(os.environ.get('INDEX'))]
        else:
            self.current_host = resource_config[constant.CURRENT_HOST]

        self.is_master = self.current_host == self.hosts[0]

        if self.mpi_operator_submit:
            self.is_master = True

        # parse training framework
        self.training_framework = os.environ.get(constant.TI_TRAINING_FRAMEWORK, None)

        self.model_dir = constant.MODEL_PATH
        self.input_config_dir = constant.INPUT_CONFIG_PATH
        self.output_data_dir = constant.OUTPUT_DATA_PATH

        self.update_os_envs()

    def get_args(self):
        args = []
        for k, v in self.train_hps.items():
            args.append('--' + k)
            if str(v).strip():
                args.append(str(v))

        return args

    def get_envs(self):
        envs = {
            "network_interface_name": self.network_interface_name,
            "user_entry_point": self.user_entry_point,
            "hps": self.train_hps,
            "channels": list(self.input_channels.keys()),
            "num_cpus": utils.get_cpu_nums(),
            "num_gpus": utils.get_gpu_nums(),
            "log_level": self.log_level,
            "model_dir": self.model_dir,
            "output_data_dir": self.output_data_dir,
            "input_config_dir": self.input_config_dir,
            "hosts":self.hosts,
            "current_host":self.current_host,
        }

        for name, path in self.input_channels.items():
            envs['channel_%s' % name] = path

        env_vars = {}
        for k, v in envs.items():
            k = constant.TM_PREFIX + str(k).upper()
            if isinstance(v, six.string_types):
                v = str(v)
            else:
                v = json.dumps(v)

            env_vars[k] = v

        return env_vars

    def update_os_envs(self):
        for name, value in self.get_envs().items():
            os.environ[name] = value
