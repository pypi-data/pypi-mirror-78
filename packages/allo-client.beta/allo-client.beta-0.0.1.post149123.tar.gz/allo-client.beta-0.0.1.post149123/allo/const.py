#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import os

CONFIG_PATH = str(Path.home()) + "/allo-config.dict"
ALLO_URL = "localhost:3080" \
    if os.getenv("ALLOENV") == "TEST" \
    else "allo.dev.libriciel.fr:443"
API_PATH = "http://{}/api/client".format("localhost:8181") \
    if os.getenv("ALLOENV") == "TEST" \
    else "https://{}/api/client".format(ALLO_URL)

CODEPRODUIT = {
    "i-Parapheur": "IP",
    "Pastell": "PA"
}
