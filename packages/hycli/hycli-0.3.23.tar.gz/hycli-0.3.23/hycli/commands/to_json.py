import click
from halo import Halo

from .. import convert_to_json, Services


@click.command(context_settings=dict(max_content_width=200))
@click.argument("path", type=click.Path(exists=True))
@click.option("-w", "--workers", default=3, show_default=True, help="amount of workers")
@click.pass_context
def to_json(ctx, path, workers):
    """ Convert invoices to ocr json output """
    # Services available
    spinner = Halo(spinner="dots")
    spinner.start()
    services = Services(ctx, check_up=True)
    spinner.succeed(f"Found dir: {path}\n ")

    # Conversion
    convert_to_json(
        path, services.extractor_endpoint, services.token, workers, services.headers
    )
    spinner.succeed("Converted invoice(s) to ocr json output.")
