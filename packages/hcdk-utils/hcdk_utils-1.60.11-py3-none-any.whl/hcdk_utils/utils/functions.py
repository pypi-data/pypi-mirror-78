import os
import socket
import hashlib
import re
from aws_cdk import (
    aws_secretsmanager as secretsmanager
)


def short_env():
    environment = os.getenv('ENVIRONMENT')
    stack_name = os.getenv('STACK_NAME')
    if stack_name != "ymonitor":
        env = stack_name.lower()
    elif environment == "production":
        env = "prd"
    elif environment == "acceptance":
        env = "acc"
    elif environment == "test":
        env = "tst"
    else:
        env = "dev"
    return env


def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True


def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True


def short_env_prod_empty():
    environment = os.getenv('ENVIRONMENT')
    if environment == "production":
        return ""
    else:
        return short_env()


def whitelisted_ips_list(ip_list):
    from aws_cdk import (core)
    ip_set_descriptors = []
    for full_ip in ip_list:
        ip = full_ip.split("/")[0]
        if is_valid_ipv4_address(ip):
            ip_type = "IPV4"
        elif is_valid_ipv6_address(ip):
            ip_type = "IPV6"
        else:
            print("Not a valid IP address! " + ip.to_s)

        ip_set_descriptors.append(
            core.Token.as_any({"type": ip_type, "value": full_ip})
        )
    return ip_set_descriptors


def md5(fname: str) -> bytes:
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_secret(
    secret: secretsmanager.ISecret,
    key_name: str,
    as_int: bool = False
):
    my_secret = secret.secret_value_from_json(key_name)
    if as_int:
        return int(my_secret)
    else:
        return my_secret.to_string()


def replace_non_alphanumeric(
    text: str,
    replacement: str = ""
) -> str:
    return re.sub('[^0-9a-zA-Z]+', replacement, text)


def private_stack_name():
    stack_name = os.getenv('STACK_NAME')
    if stack_name != 'ymonitor':
        env = stack_name.capitalize()
    else:
        env = ''
    return env


def tag_resource(
    config: dict,
    appl_value: str = None
):
    if not appl_value:
        appl_value = config['application']

    tags = []
    tags.extend(get_tag('Environment', config['environment'], False, False))
    tags.extend(get_tag('Stack', config['stack_name'], False, False))
    tags.extend(get_tag('Application', appl_value, False, False))
    return tags


def get_tag(
    tag_name: str,
    tag_value: str,
    propagate_at_launch: bool = False,
    is_autoscale: bool = False
):
    tag = {
        'key': tag_name,
        'value': tag_value
    }
    if is_autoscale:
        tag['propagateAtLaunch'] = propagate_at_launch
    return [tag]


def tag_autoscale_resource(
    config: dict,
    prop_at_launch: bool = False,
    appl_value: str = None
):
    if not appl_value:
        appl_value = config['application']

    tags = []
    tags.extend(
        get_tag('Environment', config['environment'], prop_at_launch, True)
    )
    tags.extend(
        get_tag('Stack', config['stack_name'], prop_at_launch, True)
    )
    tags.extend(
        get_tag('Application', appl_value, prop_at_launch, True)
    )
    return tags
