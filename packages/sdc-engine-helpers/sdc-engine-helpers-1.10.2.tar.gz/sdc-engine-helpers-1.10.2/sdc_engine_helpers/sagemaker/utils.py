"""
    Sagemaker Utils
        - this is a fork of sagemaker.utils found here:
        https://github.com/aws/sagemaker-python-sdk/blob/master/src/sagemaker/utils.py
"""
import time
from urllib.parse import urlparse

def sagemaker_timestamp():
    """Return a timestamp with millisecond precision."""
    moment = time.time()
    moment_ms = repr(moment).split(".")[1][:3]
    return time.strftime("%Y-%m-%d-%H-%M-%S-{}".format(moment_ms), time.gmtime(moment))

def sagemaker_short_timestamp():
    """Return a timestamp that is relatively short in length"""
    return time.strftime("%y%m%d-%H%M")

def name_from_base(base, max_length=63, short=False):
    """Append a timestamp to the provided string.
    This function assures that the total length of the resulting string is
    not longer than the specified max length, trimming the input parameter if
    necessary.
    Args:
        base (str): String used as prefix to generate the unique name.
        max_length (int): Maximum length for the resulting string.
        short (bool): Whether or not to use a truncated timestamp.
    Returns:
        str: Input parameter with appended timestamp.
    """
    timestamp = sagemaker_short_timestamp() if short else sagemaker_timestamp()
    trimmed_base = base[: max_length - len(timestamp) - 1]
    return "{}-{}".format(trimmed_base, timestamp)

def parse_s3_url(url: str):
    """Returns an (s3 bucket, key name/prefix) tuple from a url with an s3
    scheme.
    Args:
        url (str):
    Returns:
        tuple: A tuple containing:
            str: S3 bucket name str: S3 key
    """
    parsed_url = urlparse(url)
    if parsed_url.scheme != "s3":
        raise ValueError("Expecting 's3' scheme, got: {} in {}.".format(parsed_url.scheme, url))
    return parsed_url.netloc, parsed_url.path.lstrip("/")

def create_resource_name(
        *,
        context: str,
        function: str,
        additional_details: list = None
):
    """
        Constructs a structured string name, separated by a "-" delimiter.

        args:
            service (str):
            group (str): group name which speaks to function of resource
            prefix (list): (optiional) list of args containing prefixes to add in order

        Return:
            (str) : name of the form {service}-{prefixes}-{group}

        example:
            >> cache_key = SagemakerEngineHelpers.build_resource_name(
                service='recommend', group='lookup', prefix=['prefix1', 'prefix2', 'prefix3'])
            >> print(cache_key)
            'recommend-prefix1-prefix2-prefix3-lookup'
    """
    # join prefixes
    if additional_details is not None:
        additional_details = [str(p) for p in additional_details]
        prefixes = "-".join(additional_details)

        # build cache key
        cache_key = '{context}-{function}-{prefixes}'.format(
            context=context,
            prefixes=prefixes,
            function=function
        )
    else:
        # build cache key
        cache_key = '{context}-{function}'.format(
            context=context,
            function=function
        )

    return cache_key.replace(" ", "-").replace("_", "-").lower()

def build_resource_tags(current_tags: list, new_tags: list) -> list:
    """
        given a list of tags, in the AWS sagemaker tag format
        looks for resource_tags and creates a new set of resource tags
        by adding tags given. Finally returns the new tags.

    Args:
        tags (list): list of resource tags to add

    Returns:
        list: new resource tags
    """
    new_resource_tags = []
    if current_tags not in [None, []]:
        new_resource_tags = current_tags
    for tag in new_tags:
        tag_key = tag.get('Key', None)
        if tag_key is None:
            raise Exception((
                "KeyError: cannot be None. "\
                "Make Sure you use \"Key\" & \"Value\" style AWS tags"
            ))

        for index, resource_tag in enumerate(current_tags):
            if tag_key.lower() == resource_tag.get('Key').lower():
                # remove if already exists
                new_resource_tags.pop(index)
                break
        # add new key to tags
        new_resource_tags.append(tag)

    return new_resource_tags
