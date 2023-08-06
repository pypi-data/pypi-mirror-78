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

TM_PREFIX = 'TM_'
TI_PREFIX = 'ti_'

ROOT_BASE_PATH = "/opt/ml/"
CODE_PATH = os.path.join(ROOT_BASE_PATH, "code")
MODEL_PATH = os.path.join(ROOT_BASE_PATH, "model")
INPUT_PATH = os.path.join(ROOT_BASE_PATH, "input")
OUTPUT_PATH = os.path.join(ROOT_BASE_PATH, "output")

INPUT_CHANNLE_PATH = os.path.join(INPUT_PATH, "data")
INPUT_CONFIG_PATH = os.path.join(INPUT_PATH, "config")

OUTPUT_SUCCESS_PATH = os.path.join(OUTPUT_PATH, "success")
OUTPUT_FAILURE_PATH = os.path.join(OUTPUT_PATH, "failure")
OUTPUT_DATA_PATH = os.path.join(OUTPUT_PATH, "data")

HYPERPARAMETERS_PATH = os.path.join(INPUT_CONFIG_PATH, "hyperparameters.json")
RESOURCE_CONFIG_PATH = os.path.join(INPUT_CONFIG_PATH, "resourceconfig.json")
INPUT_DATA_CONFIG_PATH = os.path.join(INPUT_CONFIG_PATH, "inputdataconfig.json")

TI_REGION = "ti_region"
TI_JOB_NAME = "ti_job_name"
TI_NETWORK_INTERFACE_NAME = "ti_network_interface_name"
TI_CONTAINER_LOG_LEVEL = "ti_container_log_level"
TI_PROGRAM = "ti_program"
TI_SUBMIT_DIRECTORY = "ti_submit_directory"
TI_PARAMETER_SERVER_ENABLED = "ti_parameter_server_enabled"
TI_MPI_ENABLED = "ti_mpi_enabled"
TI_MPI_NUM_OF_PROCESSES_PER_HOST = "ti_mpi_num_of_processes_per_host"
TI_MPI_CUSTOM_MPI_OPTIONS = "ti_mpi_custom_mpi_options"
TI_TRAINING_FRAMEWORK = 'TI_TRAINING_FRAMEWORK'

CURRENT_HOST = "current_host"
HOSTS = "hosts"

TF_WORKER_PORT = 5555
TF_PS_PORT = 5556

PYTORCH_MASTER_PORT = 6666

MXNET_PS_PORT = 7777
MXNET_PS_VERBOSE = 0

TIMEOUT_SECONDS = 600
INTERVAL_SECONDS = 5

DEFAULT_NIC_NAME = 'eth0'

SSH_PORT = 23456

MPI_OPERATOR_SUBMIT = "mpi_operator_submit"

