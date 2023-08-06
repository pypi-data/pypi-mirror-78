# Everything from the endpoints.


"""
Data from Conductor endpoints as a singleton.

Also has the ability to use fixtures for dev purposes.
"""
import json
import os
from ciocore.package_tree import PackageTree
from ciocore import api_client

DISK_CACHE_DIR = os.environ.get("CIO_FIXTURES_DIR", "")

__data__ = {}
__product__ = None


def data(
        force=False,
        force_projects=False,
        force_software=False,
        force_instance_types=False,
        try_cache=False):
    """
    Get projects , instance_types, and software from disk or api.

    Data will be valid.

    args: product, force_all, force_projects, force_software, force_instance_types, try_cache
    """

    global __data__
    global __product__

    if not __product__:
        raise ValueError(
            'Data singleton must be initialized before use, e.g. data.init("maya-io") or data.init("all").')

    if force or force_projects:
        __data__["projects"] = None
    if force or force_instance_types:
        __data__["instance_types"] = None
    if force or force_software:
        __data__["software"] = None

    # PROJECTS
    if not __data__.get("projects"):
        cache_path = os.path.join(DISK_CACHE_DIR, "projects.json")
        if DISK_CACHE_DIR and os.path.isfile(cache_path) and try_cache:
            try:
                with open(cache_path) as f:
                    __data__["projects"] = json.load(f)
            except BaseException:
                __data__["projects"] = None
        if not __data__.get("projects"):
            __data__["projects"] = api_client.request_projects()
        if __data__.get("projects"):
            __data__["projects"] = sorted(__data__["projects"])

    # INST_TYPES
    if not __data__.get("instance_types"):
        cache_path = os.path.join(DISK_CACHE_DIR, "instance_types.json")
        if DISK_CACHE_DIR and os.path.isfile(cache_path) and try_cache:
            try:
                with open(cache_path) as f:
                    __data__["instance_types"] = json.load(f)
            except BaseException:
                __data__["instance_types"] = None
        if not __data__.get("instance_types"):
            __data__["instance_types"] = api_client.request_instance_types()
        if __data__.get("instance_types"):
            __data__["instance_types"] = sorted(
                __data__["instance_types"], key=lambda k: (k["cores"], k["memory"]))

    # SOFTWARE
    if not __data__.get("software"):
        all_packages = None
        cache_path = os.path.join(DISK_CACHE_DIR, "software.json")
        if DISK_CACHE_DIR and os.path.isfile(cache_path) and try_cache:
            try:
                with open(cache_path) as f:
                    all_packages = json.load(f)
            except BaseException:
                all_packages = None
        if not all_packages:
            all_packages = api_client.request_software_packages()
        if all_packages:
            if __product__ == "all":
                pt = PackageTree(all_packages)
            else:
                pt = PackageTree(all_packages, product=__product__)
            if pt.tree:
                __data__["software"] = pt

    return __data__


def valid():
    global __data__
    if not __data__.get("projects"):
        return False
    if not __data__.get("instance_types"):
        return False
    if not __data__.get("software"):
        return False
    return True


def clear():
    global __data__
    __data__ = {}


def init(product=None):
    global __product__
    if not product:
        raise ValueError("You must specify a product or 'all'")
    __product__ = product


def product():
    global __product__
    return __product__
