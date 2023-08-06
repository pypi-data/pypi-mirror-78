import warnings

import click

from . import __version__


@click.group(name="engine")
@click.version_option(version=__version__, prog_name="nomnomdata-engine")
def cli():
    """NomNomData Engine CLI, used for the execution of engines"""
    warnings.warn(
        "nnd engine cli is deprecated, please use new python models", DeprecationWarning,
    )
