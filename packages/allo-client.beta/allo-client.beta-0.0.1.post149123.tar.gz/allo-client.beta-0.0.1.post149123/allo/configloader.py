# -*- coding: utf-8 -*-
import pickle
from time import sleep

from PyInquirer import prompt
from .model.config import AlloConfig
from .model.version import Version
from .model.colors import BColors
from .const import *
from .alloapi import AlloAPI
from .ansible import AlloAnsible


class ConfigLoader:
    config: AlloConfig

    __error_config_msg = "Erreur de configuration, sortie du programme Allo"

    def __init__(self, env):
        # TODO - Reduce complexity / Refactor
        try:
            with open(CONFIG_PATH, 'rb') as config_dictionary_file:
                self.config = pickle.load(config_dictionary_file)
            found_instance = AlloAPI.find_instance()
        except FileNotFoundError:
            self.config = AlloConfig()
            self.config.env = env
            found_instance = AlloAPI.find_instance()
            secret = AlloAPI.get_secret()
            if "status" in found_instance and found_instance["status"] == 404:
                print(BColors.OKBLUE + "En attente d'association... Identifiant du noeud : " + secret)
                while "token" not in found_instance:
                    sleep(5)
                    found_instance = AlloAPI.find_instance()
                    continue
                print(BColors.OKGREEN + "Association effectuée avec succès")
            if "server_node_c" not in found_instance:
                self.config.id_client = secret
                self.config.internal = True
                self.config.code_produit = prompt(
                    [{'type': 'input', 'name': 'code_produit', 'message': 'Code produit'}])['code_produit']
            else:
                self.config.id_client = found_instance["server_node_c"]
                self.config.code_produit = CODEPRODUIT[found_instance["produit"]]
            if "token" in found_instance:
                self.config.teleport_token = found_instance["token"]
            else:
                self.config.teleport_token = prompt(
                    [{'type': 'input', 'name': 'teleport_token', 'message': 'Token de télémaintenance'}])['teleport_token']
            self.save()
            # Create specific user to access node only if product is well known
            if self.config.code_produit in CODEPRODUIT.values():
                AlloAnsible().create_user(self.config.code_produit.lower())
        if "server_node_c" not in found_instance:
            print(BColors.HEADER + "Instance interne détectée")
        else:
            print(BColors.HEADER + "- Compte              : {}".format(
                found_instance["account"]["name"]
                if found_instance["account"] is not None and "name" in found_instance["account"]
                else "Aucun compte associé"))
            print(BColors.HEADER + "- Type d'exploiration : {}".format(found_instance["type_exploitation"]))
            print(BColors.HEADER + "- Produit             : {}".format(found_instance["produit"]))
            print(BColors.HEADER + "- Version             : {}".format(found_instance["version_actuelle"]))

    def ask_user_configuration(self):
        print(BColors.OKBLUE + "Merci de rentrer les informations suivantes afin d'initialiser Allo :")
        self.ask_for_client_info()

        versions = AlloAPI.list_version(self.config)
        if not versions:
            print(BColors.FAIL + self.__error_config_msg)
            exit(1)
        else:
            qversions = []
            for v in versions:
                qversions.append({"value": "0", "name": v['name']})
            questions = [{'type': 'list',
                          'name': 'version',
                          'message': 'Version du produit',
                          'choices': qversions}]
            answers = prompt(questions)
            self.config.version = Version(versions[int(answers['version'])])

        if self.verify():
            self.config.teleport_token = prompt(
                [{'type': 'input', 'name': 'teleport_token', 'message': 'Token de télémaintenance'}])['teleport_token']
            # disable repo_path for now
            # self.config.repo_path = prompt(
            #     [{'type': 'input', 'name': 'repo_path', 'message': 'Chemin d\'installation du logiciel'}])['repo_path']
            self.save()
        else:
            print(BColors.FAIL + "Erreur de configuration, sortie du programme Allo")
            exit(1)

    def verify(self):
        status = AlloAPI.register(self.config)
        if not status:
            print(BColors.FAIL + self.__error_config_msg)
            exit(1)
        if not status['active']:
            cfg = prompt([{'type': 'input', 'name': 'pin_code', 'message': 'Code PIN d\'activation Allo'}])
            AlloAPI.activate(self.config, cfg['pin_code'])
        print(BColors.OKGREEN + "Connexion Allo OK")
        return True

    def ask_for_client_info(self):
        questions = [{'type': 'input', 'name': 'id_client', 'message': 'Identifiant unique Client'},
                     {'type': 'input', 'name': 'code_produit', 'message': 'Code Produit'}]
        cfg = prompt(questions)
        self.config.id_client = cfg['id_client']
        self.config.code_produit = cfg['code_produit']

    def save(self):
        with open(CONFIG_PATH, 'wb') as config_dictionary_file:
            pickle.dump(self.config, config_dictionary_file)
