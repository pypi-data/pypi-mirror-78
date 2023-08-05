# -*- coding: utf-8 -*-

import os
import subprocess
from .model.config import AlloConfig
from .const import *


class AlloTelem:
    config_file = str(Path.home()) + "/teleport-config.yml"

    def __init__(self, config: AlloConfig):
        if not os.path.exists(self.config_file):
            self.save_config(config)

    def save_config(self, config):
        teleport_yaml = ("teleport:",
                         '    auth_token: "{}"'.format(config.teleport_token),
                         '    ca_pin: "sha256:996d90b8691278667a3b08d9869fca77a0474fe9d0eefa7001a9bfd43a9ddcc2"',
                         '    auth_servers:',
                         '        - {}'.format(ALLO_URL),
                         'auth_service:',
                         '    enabled: no',
                         'proxy_service:',
                         '    enabled: no',
                         'ssh_service:',
                         '    enabled: "yes"',
                         '    labels:',
                         '        produit: {}'.format(config.code_produit),
                         '        secret: {}'.format(config.id_client),
                         '        internal: {}'.format("true" if config.internal else "false"))

        with open(self.config_file, 'w+') as yaml_file:
            yaml_file.write('\n'.join(teleport_yaml))

    def connect(self):
        with subprocess.Popen(["sudo", "teleport", "start", '-c', self.config_file],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
            try:
                print("Télémaintenance ouverte. Pour l'interrompre, utilisez le raccourci clavier CTRL+C")
                proc.wait()
            except KeyboardInterrupt:
                print("Fin de télémaintenance")
