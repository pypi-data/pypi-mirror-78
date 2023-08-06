from typing import Iterator
import logging

import boto3

logger = logging.getLogger(__name__)


def iter_objects(
    Bucket: str, client: "botocore.client.S3" = None, **kwargs
) -> Iterator[dict]:
    """
    Repeatedly (recursively) call `client.list_objects_v2` until listing is exhausted.
    Iterates over each object in each response's "Contents" field.

    If `client` is omitted, a new default client will be created.

    Additional options specifiable as kwargs:
    * Delimiter: str = character to group keys
    * EncodingType: str = type of encoding to encode keys (default: "url")
    * MaxKeys: int = page size (default: 1000) (max: 1000)
    * Prefix: str = limit response to keys beginning with `Prefix`
    * FetchOwner: bool = fetch `Owner` field (default: False)
    * StartAfter: str = limit response to keys strictly greater than `StartAfter`
    * RequestPayer: str = "requester" to acknowledge API charges for 3rd-party buckets
    """
    if not client:
        client = boto3.client("s3")

    logger.debug("Listing objects in bucket %r with options %r", Bucket, kwargs)
    response = client.list_objects_v2(Bucket=Bucket, **kwargs)

    yield from response.get("Contents", ())

    if response["IsTruncated"]:
        kwargs.update(ContinuationToken=response["NextContinuationToken"])
        yield from iter_objects(Bucket, client, **kwargs)
    else:
        logger.debug("Exhausted listing")
