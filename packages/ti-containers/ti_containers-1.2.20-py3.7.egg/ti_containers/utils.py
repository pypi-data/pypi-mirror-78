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

import argparse
import json
import logging
import multiprocessing
import os
import shlex
import socket
import subprocess

from retrying import retry

def get_logger():
    return logging.getLogger("ti")

def configure_logger(level):
    logging.basicConfig(format='%(asctime)s %(name)-4s %(levelname)-4s %(message)s', level=int(level))

def file_exist(path):
    if not os.path.isfile(path):
        return False

    return True


def read_json_file(path):
    with open(path, 'r') as f:
        return json.load(f)


def write_json_file(obj, path):
    with open(path, 'w') as f:
        json.dump(obj, f)


def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


def format_hyperparameters(hps):
    hyperparameters = {}
    for k, v in hps.items():
        try:
            v = json.loads(v)
        except (ValueError, TypeError):
            pass

        hyperparameters[k] = v

    return hyperparameters


def extract_hyperparameters(hps, prefix):
    extend_hps = {}
    train_hps = {}

    for k, v in hps.items():
        if k.startswith(prefix):
            extend_hps[k] = v
        else:
            train_hps[k] = v

    return extend_hps, train_hps


def get_gpu_nums():
    try:
        cmd = shlex.split('nvidia-smi --list-gpus')
        output = subprocess.check_output(cmd).decode('utf-8')
        return sum([1 for x in output.split('\n') if x.startswith('GPU ')])
    except Exception as e:
        return 0


def get_cpu_nums():
    return multiprocessing.cpu_count()


def get_mpi_options(mpi_options):
    mpi_parser = argparse.ArgumentParser()
    mpi_parser.add_argument("--NCCL_DEBUG", default="INFO", type=str)
    return mpi_parser.parse_known_args(mpi_options.split())


def start_sshd_process(port):
    subprocess.Popen(["/usr/sbin/sshd", "-D", "-p", str(port)])


def check_ssh_connect(host, port):
    import paramiko

    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=port)
        client.close()
        return True
    except Exception as e:
        get_logger().info('Cannot connect host %s, %s', host, e)
        return False


@retry(stop_max_delay=1000 * 60 * 10,
       wait_exponential_multiplier=200,
       wait_exponential_max=50000)
def dns_lookup(host):
    return socket.gethostbyname(host)
