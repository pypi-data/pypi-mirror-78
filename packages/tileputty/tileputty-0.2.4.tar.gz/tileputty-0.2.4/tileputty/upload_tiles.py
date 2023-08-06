import logging
import multiprocessing
import os
import sys
from logging import Logger
from typing import Iterator

import boto3
import click
from botocore.config import Config
from parallelpipe import stage

LOGGER: Logger = logging.getLogger("tileputty")
CORES: int = multiprocessing.cpu_count()

# File headers for different formats
MVT_META = {
    "ContentType": "application/x-protobuf",
    "ContentEncoding": "gzip",
    "CacheControl": "max-age=31536000",  # 1 yr
}
PNG_META = {"ContentType": "image/png", "CacheControl": "max-age=31536000"}  # 1 yr
JPG_META = {"ContentType": "image/jpeg", "CacheControl": "max-age=31536000"}  # 1 yr
JSON_META = {"ContentType": "application/json"}

ARGS = {
    ".pbf": MVT_META,
    ".mvt": MVT_META,
    ".png": PNG_META,
    ".jpg": JPG_META,
    ".json": JSON_META,
}


@click.command()
@click.option("--bucket", default="gfw-tiles", help="AWS Bucket")
@click.option("--dataset", help="Dataset Name")
@click.option("--version", help="Dataset Version ID")
@click.option("--implementation", default="default", help="Tile Cache Implementation")
@click.argument("tile_cache")
def cli(
    tile_cache: str, dataset: str, version: str, bucket: str, implementation: str
) -> None:
    """ TILE_CACHE: path to local tile cache """

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s %(levelname)-4s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
    )
    LOGGER.addHandler(handler)

    upload_tiles(
        tile_cache=tile_cache,
        bucket=bucket,
        dataset=dataset,
        version=version,
        implementation=implementation,
    )


def upload_tiles(
    tile_cache: str,
    dataset: str,
    version: str,
    bucket: str = "gfw-tiles",
    implementation: str = "default",
) -> None:
    """
    :param tile_cache: Path to local tile cache
    :param layer: Layer name
    :param version: Layer version number
    :param bucket: AWS S3 bucket name (default: gfw-tiles)
    :param option: Layer option (default: default)
    :param ext: Tile cache format (default: mvt)
    :param update_latest: Update latest file in tile cache root (default: False)
    :return: None
    """

    LOGGER.info(
        f"Upload tile cache to {dataset}/{version}/{implementation} using {CORES} processes"
    )

    # pipe files
    pipe = _files(tile_cache) | _stage_copy(
        tile_cache, bucket, dataset, version, implementation
    )

    # collect results
    for output in pipe.results():
        LOGGER.debug(output)


def _files(tile_cache: str) -> Iterator[str]:
    """Collect all files in tile cache."""
    for root, dirs, files in os.walk(tile_cache):
        for f in files:
            yield os.path.join(root, f).replace("\\", "/")


@stage(workers=CORES)
def _stage_copy(
    files, tile_cache, bucket, dataset, version, implementation
) -> Iterator[str]:
    """Upload files to S3 and update file header."""

    config = Config(retries={"max_attempts": 10, "mode": "standard"})
    endpoint_url = os.environ.get("ENDPOINT_URL", None)
    s3 = boto3.client("s3", config=config, endpoint_url=endpoint_url)

    for f in files:

        file_name = os.path.basename(f)
        prefix = os.path.dirname(f).replace(tile_cache + "/", "")
        basename, extension = os.path.splitext(file_name)

        try:
            args = ARGS[extension]
        except KeyError:
            args = {}

        s3_path = f"{dataset}/{version}/{implementation}/{prefix}/{file_name}"
        s3.upload_file(f, bucket, s3_path, ExtraArgs=args)
        yield s3_path


if __name__ == "__main__":
    cli()
