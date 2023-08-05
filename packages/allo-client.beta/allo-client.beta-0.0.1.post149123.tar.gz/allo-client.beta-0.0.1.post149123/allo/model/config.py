# -*- coding: utf-8 -*-

from .version import Version


class AlloConfig:
    id: int
    id_client: str
    code_produit: str
    teleport_token: str
    env: str
    repo_path: str
    version: Version
    internal: bool = False
