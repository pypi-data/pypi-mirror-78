import json

from concurrent.futures import ThreadPoolExecutor, as_completed

import click

from ..services.requests import extract_invoice
from .commons import read_pdf, get_filenames


def convert_to_json(path, extractor_endpoint, token, workers, headers):
    # Todo: add single invoice path besides dir
    files = get_filenames(path)

    with ThreadPoolExecutor(max_workers=workers) as exe:
        jobs = {
            exe.submit(
                extract_invoice,
                read_pdf(file_path),
                extractor_endpoint,
                file_extension,
                token,
                headers,
            ): file_path
            for file_path, file_extension in files.items()
        }
        label = f"Converting {len(jobs)} invoices"
        with click.progressbar(jobs, label=label) as bar:
            for idx, future in enumerate(as_completed(jobs)):
                file_name = jobs[future].split("/")[-1]
                try:
                    response = future.result(timeout=300)

                except Exception as e:
                    print(f"Error: {e}")

                with open(file_name.split(".")[0] + ".json", "w") as f:
                    json.dump(response, f)

                bar.update(1)
