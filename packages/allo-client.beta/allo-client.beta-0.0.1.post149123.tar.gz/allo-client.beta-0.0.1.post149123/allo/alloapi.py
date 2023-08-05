#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import jsons
from requests import Response
from uuid import getnode
from .const import *
from .model.colors import BColors
from .model.config import AlloConfig


class AlloAPI:
    @staticmethod
    def find_instance():
        r = requests.get("{}/{}".format(API_PATH, getnode()))
        if AlloAPI.has_error(r):
            return False
        return r.json()

    @staticmethod
    def get_secret():
        r = requests.get("{}/{}/secret".format(API_PATH, getnode()))
        if AlloAPI.has_error(r):
            return False
        return r.text

    @staticmethod
    def is_active():
        r = requests.get("{}/{}/active".format(API_PATH, getnode()))
        if AlloAPI.has_error(r) or r.status_code == 404:
            return False
        return True

    @staticmethod
    def list_version(config: AlloConfig):
        r = requests.get("{}/{}/versions".format(API_PATH, config.code_produit),
                         headers={'channel': config.env})
        if AlloAPI.has_error(r):
            return False
        versions = r.json()
        if 'status' in versions:
            print(BColors.FAIL + "{} : {}".format(config.code_produit, versions['message']))
            return False
        elif len(versions) is 0:
            print(BColors.FAIL + "{} : {}".format(config.code_produit, "Aucune versions disponibles"))
            return False
        return versions

    @staticmethod
    def register(config: AlloConfig):
        r = requests.post("{}/{}/register".format(API_PATH, getnode()), json={
            "idClient": config.id_client,
            "product": config.code_produit,
            "version": jsons.dump(config.version)
        })
        if AlloAPI.has_error(r):
            return False
        data = r.json()
        if 'status' in data:
            print(BColors.FAIL + "{} pour l'identifiant {} et le produit {}".format(data['message'],
                                                                                    config.id_client,
                                                                                    config.code_produit))
            return False
        # Update id_client in case we sent something incomplete to the server
        config.id_client = data['idClient']
        config.id = data['id']
        return data

    @staticmethod
    def activate(config: AlloConfig, pin_code: str):
        r = requests.post("{}/{}/activate".format(API_PATH, getnode()), json={
            "idClient": config.id_client,
            "product": config.code_produit,
            "version": jsons.dump(config.version),
            'pin': pin_code
        })
        if AlloAPI.has_error(r):
            return False
        data = r.json()
        if not data['active']:
            print(BColors.FAIL + "Mauvais code PIN")
            return False
        print(BColors.OKGREEN + "Code PIN OK")
        return True

    @staticmethod
    def get_git_token(config: AlloConfig):
        # Get deploy token
        r = requests.get(
            "{}/{}/{}/{}/{}/{}/token".format(API_PATH,
                                             config.id_client,
                                             getnode(),
                                             config.code_produit,
                                             config.version.name,
                                             config.version.channel
                                             ))
        if AlloAPI.has_error(r):
            return False
        data = r.json()
        return data['token']

    @staticmethod
    def has_error(r: Response):
        if r.status_code is 502:
            print(BColors.FAIL + "Erreur lors de la communication avec Allo Server : Erreur {}".format(r.status_code))
            return True
        return False
