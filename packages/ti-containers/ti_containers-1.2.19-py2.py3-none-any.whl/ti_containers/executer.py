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
import sys
import time

from ti_containers import constant
from ti_containers import utils
from ti_containers.exception import RunUserEntrypointError
from ti_containers.utils import get_logger

logger = get_logger()

class Worker(object):
    def __init__(self, config):
        self.config = config

    def _get_command(self):
        return [sys.executable, self.config.user_entry_point] + self.config.get_args()

    '''
    def run(self):
        command = self._get_command()
        logger.info("Training command: %s", " ".join(command))

        process = subprocess.Popen(
            command, stderr=subprocess.PIPE, env=os.environ
        )

        _, stderr = process.communicate()
        exit_code = process.poll()
        if exit_code != 0:
            raise RunUserEntrypointError(command=" ".join(command), output=stderr)
    '''

    def run(self):
        command = self._get_command()
        logger.info("Training command: %s", " ".join(command))

        process = subprocess.Popen(
            command, env=os.environ
        )

        exit_code = process.wait()
        if exit_code != 0:
            raise RunUserEntrypointError(command=" ".join(command), output="")

class MPIWorker(Worker):
    def __init__(self, config):
        self.config = config

    def run(self):
        logger.info('MPI worker start')
        utils.start_sshd_process(constant.SSH_PORT)

        logger.info('Waiting orted process finish.')
        import psutil
        for t in range(int(constant.TIMEOUT_SECONDS / constant.INTERVAL_SECONDS)):
            procs = [p for p in psutil.process_iter(attrs=['name']) if p.info['name'] == "orted"]
            if procs:
                break

            time.sleep(constant.INTERVAL_SECONDS)

        if not procs:
            raise RuntimeError("ERROR. orted process can not work")

        logger.info('Orted process work.')
        psutil.wait_procs(procs)

        logger.info('MPI process finish.')
        time.sleep(30)


class MPILanucher(Worker):
    def __init__(self, config):
        self.config = config

    def _get_command(self):
        command = ['mpirun', '--allow-run-as-root', '-display-allocation', '--display-map']
        np = self.config.mpi_process_per_host * len(self.config.hosts)
        command.extend(['-np', str(np)])
        if not self.config.mpi_operator_submit:
            utils.start_sshd_process(constant.SSH_PORT)
            self._wait_workers_ready()

            host_ips = [utils.dns_lookup(host) for host in self.config.hosts]
            if self.config.mpi_process_per_host == 1:
                mpi_hosts = host_ips
            else:
                mpi_hosts = ['%s:%s' % (host, self.config.mpi_process_per_host) for host in host_ips]

            command.extend([
                '--host', ','.join(mpi_hosts)
            ])
        else:
            command.extend([
                '--host', os.environ.get('NODE_LIST')
            ])

        nccl_options, custom_options = utils.get_mpi_options(self.config.custom_mpi_options)
        command.extend([
            '-bind-to', 'None',
            '-map-by', 'slot',
            '-mca', 'btl_tcp_if_include', self.config.network_interface_name,
            '-mca', 'oob_tcp_if_include', self.config.network_interface_name,
            '-mca', 'pml', 'ob1', '-mca', 'btl', '^openib',
            '-mca', 'orte_abort_on_non_zero_status', '1',
            '-x', 'NCCL_DEBUG=%s' % nccl_options.NCCL_DEBUG,
            '-x', 'NCCL_SOCKET_IFNAME=%s' % self.config.network_interface_name,
            '-x', 'LD_LIBRARY_PATH',
            '-x', 'PATH',
        ])

        command.extend(custom_options)

        for name in self.config.get_envs():
            command.extend(['-x', name])

        command.extend([sys.executable, '-m', 'mpi4py', self.config.user_entry_point])
        command.extend(self.config.get_args())
        return command

    def _wait_workers_ready(self):
        logger.info('Wait MPI workers ssh ready')
        for host in self.config.hosts:
            if host == self.config.current_host:
                continue

            pre = int(time.time())
            while not utils.check_ssh_connect(host, constant.SSH_PORT):
                time.sleep(constant.INTERVAL_SECONDS)
                now = int(time.time())
                if now - pre > constant.TIMEOUT_SECONDS:
                    raise RuntimeError("Training failed. worker %s ssh not ready " % host)

            logger.info('Worker %s ready', host)
