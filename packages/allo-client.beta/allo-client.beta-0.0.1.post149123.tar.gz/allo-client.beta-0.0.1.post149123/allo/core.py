#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyInquirer import prompt
from .model.config import AlloConfig
from .model.colors import BColors
from .configloader import ConfigLoader
from .telem import AlloTelem
from .git.gitutils import AlloGit
from .alloapi import AlloAPI


class TestingAllo:
    config: AlloConfig
    telem: AlloTelem
    git: AlloGit

    def __init__(self, env):
        self.config = ConfigLoader(env).config
        self.telem = AlloTelem(self.config)
        # self.git = AlloGit(self.config, AlloAPI.get_git_token(self.config))

        self.what_to_do()

    def what_to_do(self):
        questions = [{'type': 'list', 'name': 'action', 'message': 'Que voulez-vous faire ?',
                      'choices': [
                          'Verifier la connexion',
                          'Ouvrir la télémaintenance',
                          # 'Modifier les informations de connexion',
                          # 'Mettre à jour',
                          # 'Annuler une mise à jour'
                      ]}]
        answers = prompt(questions)
        if 'action' not in answers:
            return
        if 'Verifier la connexion' in answers['action']:
            AlloAPI.register(self.config)
        if 'Ouvrir la télémaintenance' in answers['action']:
            self.telem.connect()
        if 'Modifier les informations de connexion' in answers['action']:
            print("TODO")
        if 'Mettre à jour' in answers['action']:
            self.change_version(True)
        if 'Annuler une mise à jour' in answers['action']:
            self.change_version(False)
        self.what_to_do()

    def change_version(self, upgrade: bool):
        choices = self.git.get_versions_to_pass("", not upgrade)
        if len(choices) > 0:
            questions = [{'type': 'list',
                          'name': 'version',
                          'message': 'Mettre à jour vers quelle version ?' if upgrade else 'Revenir à quelle version ?',
                          'choices': choices}]
            ans = prompt(questions)
            self.git.upgrade_to(ans['version']) if upgrade else self.git.downgrade_to(ans['version'])
        else:
            print(BColors.OKBLUE +
                  ("=> Vous êtes déjà en dernière version" if upgrade else "=> Aucune version sur laquelle revenir"))
