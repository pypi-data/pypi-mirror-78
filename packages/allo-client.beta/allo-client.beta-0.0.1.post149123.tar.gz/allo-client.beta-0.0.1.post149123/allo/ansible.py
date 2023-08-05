import os
import sys
import subprocess
import progressbar


class AlloAnsible:
    def create_user(self, product):
        self._run_playbook("create_user.yml", [
            'Création de l\'utilisateur de télémaintenance : ', progressbar.AnimatedMarker()
        ], "user_name=libriciel-{}".format(product.lower()))

    def install_dependencies(self):
        self._run_playbook("install_allo.yml", [
            'Préparation au lancement : ', progressbar.AnimatedMarker()
        ])

    def _run_playbook(self, ymlfile, widgets, pb_vars=""):
        fh = open(os.devnull, "w")
        self.process = subprocess.Popen(
            (
                'ansible-playbook',
                os.path.dirname(os.path.realpath(__file__)) + "/playbooks/" + ymlfile,
                "--extra-vars",
                pb_vars
            ), stdout=fh, stderr=fh)
        self.iterations = 0
        self.bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength, widgets=widgets)

        while not self._wait():
            # Do nothing, just wait and update progressbar
            pass
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")

        fh.close()

    def _wait(self):
        try:
            self.iterations += 1
            self.bar.update(self.iterations)
            self.process.wait(0.2)
            self.bar.finish()
            return True
        except subprocess.TimeoutExpired:
            return False
