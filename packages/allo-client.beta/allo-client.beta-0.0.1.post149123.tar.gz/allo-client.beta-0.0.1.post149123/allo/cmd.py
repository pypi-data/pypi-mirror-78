#!/usr/bin/env python
# -*- coding: utf-8 -*-
import allo
import click


@click.group(invoke_without_command=True, help="Lancement de allo")
@click.version_option()
@click.pass_context
def cmd(ctx):
    print("ALLO-NG v{} - Utilitaire de mise a jour automatique et telemaintenance".format(allo.__version__))
    """Allo CLI program."""
    if not ctx.invoked_subcommand:
        from allo.ansible import AlloAnsible
        AlloAnsible().install_dependencies()
        from allo.core import TestingAllo
        TestingAllo("PROD")


@cmd.command(help="Installation de dependances allo")
def install():
    from allo.ansible import AlloAnsible
    AlloAnsible().install_dependencies()


@cmd.command(help="Utilisation de allo en mode CLI, sans fichier de configuration")
def cli():
    # do something here
    print("TODO")
