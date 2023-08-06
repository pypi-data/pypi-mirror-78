#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys

from dci_downloader.version import __version__

EXAMPLES = """
examples:
  # download the latest RHEL-8-milestone compose in /tmp/repo
  dci-downloader RHEL-8-milestone /tmp/repo

  # download specific arch
  dci-downloader RHEL-8-milestone /tmp/repo --arch ppc64le

  # download explicit variants
  dci-downloader RHEL-8-milestone /tmp/repo --variant AppStream --variant BaseOS

  # load options from yaml settings file
  dci-downloader --settings settings.yml
"""

COPYRIGHT = """
copyright:
  Copyright © 2019 Red Hat.
  Licensed under the Apache License, Version 2.0
"""


def parse_arguments(arguments):
    parser = argparse.ArgumentParser(
        usage="dci-downloader TOPIC DEST [OPTIONS]",
        description="Download the latest DCI components easily:\n * source your credentials file\n * specify the topic name and the destination folder",
        epilog=EXAMPLES + COPYRIGHT,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "name",
        metavar="TOPIC",
        nargs="?",
        help="topic name (i.e. RHEL-8-nightly, RHEL-8-milestone, RHEL-8.2-milestone, etc...)",
    )
    parser.add_argument(
        "download_folder", metavar="DEST", nargs="?", help="destination folder."
    )
    parser.add_argument(
        "--component-id",
        metavar="COMPONENT_ID",
        dest="component_id",
        help="download a specific component by id",
    )
    parser.add_argument(
        "--arch",
        action="append",
        metavar="ARCH",
        dest="archs",
        default=[],
        help="download a specific architecture (default: x86_64)",
    )
    parser.add_argument(
        "--variant",
        action="append",
        metavar="VARIANT",
        dest="variants",
        default=[],
        help="download a specific variant (default: all variants)",
    )
    parser.add_argument(
        "--debug", help="download debug RPMs", dest="with_debug", action="store_true"
    )
    parser.add_argument(
        "--all",
        help="download all archs, all variants with debugs rpms",
        dest="download_everything",
        action="store_true",
    )
    parser.add_argument(
        "--settings",
        dest="settings_file_path",
        metavar="FILE_PATH",
        help="settings file to overwrite cli parameters",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parsed_arguments = parser.parse_args(arguments)
    if not parsed_arguments.archs:
        parsed_arguments.archs = ["x86_64"]
    parsed_arguments.archs = list(set(parsed_arguments.archs))

    if parsed_arguments.settings_file_path is None:
        download_folder = parsed_arguments.download_folder
        if download_folder is None:
            print("download folder is required")
            print("Try 'dci-downloader --help' for more information.")
            sys.exit(2)
        topic_name = parsed_arguments.name
        component_id = parsed_arguments.component_id
        if not topic_name and not component_id:
            print("TOPIC or --component-id is required")
            print("Try 'dci-downloader --help' for more information.")
            sys.exit(2)

    parsed_arguments.variants = [
        {"name": v, "with_debug": parsed_arguments.with_debug}
        for v in parsed_arguments.variants
    ]
    return vars(parsed_arguments)
