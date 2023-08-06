import os

import click
from halo import Halo

from .. import convert_to_xml, Services


@click.command(context_settings=dict(max_content_width=200))
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "-o",
    "--output",
    help="output directory for file",
    default=os.getcwd(),
    show_default=True,
    type=click.Path(exists=True),
)
@click.pass_context
def to_xml(ctx, path, output):
    """ Convert invoice to xml """
    # Services available
    spinner = Halo(spinner="dots")
    spinner.start()
    services = Services(ctx, check_up=True)
    spinner.succeed(f"Found file: {path}\n ")

    # Conversion
    convert_to_xml(
        path,
        output,
        services.extractor_endpoint,
        services.vat_validator_endpoint,
        services.validation_endpoint,
        services.token,
    )
    spinner.succeed("Converted invoice to xml")
