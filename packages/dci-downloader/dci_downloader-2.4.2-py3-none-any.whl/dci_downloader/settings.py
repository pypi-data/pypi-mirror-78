#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import traceback
import yaml
import sys

from dci_downloader.cli import parse_arguments


def _read_settings_file(settings_file_path):
    with open(settings_file_path, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError:
            print("Can't read %s file" % settings_file_path)
            traceback.print_exc()


def _get_download_folder(cli_settings, env_variables):
    dci_local_repo = env_variables.get("DCI_LOCAL_REPO")
    if dci_local_repo:
        return dci_local_repo
    download_folder = cli_settings["download_folder"]
    if download_folder:
        return download_folder
    return None


def _clean_topic(topic):
    name = topic["topic"] if "topic" in topic else topic["name"]
    component_id = topic["component_id"] if "component_id" in topic else None
    components = topic["components"] if "components" in topic else []
    archs = topic["archs"] if "archs" in topic else ["x86_64"]
    variants = topic["variants"] if "variants" in topic else []
    variants = [
        v if type(v) is dict else {"name": v, "with_debug": False} for v in variants
    ]
    all = topic["download_everything"] if "download_everything" in topic else False
    return {
        "name": name,
        "components": components,
        "archs": archs,
        "variants": variants,
        "download_everything": all,
        "download_folder": topic["download_folder"],
        "dci_key_file": topic["dci_key_file"],
        "dci_cert_file": topic["dci_cert_file"],
        "component_id": component_id,
    }


def _clean_settings(settings):
    new_settings = settings.copy()
    new_topics = []
    for topic in settings["topics"]:
        topic["download_folder"] = settings["download_folder"]
        topic["dci_key_file"] = settings["dci_key_file"]
        topic["dci_cert_file"] = settings["dci_cert_file"]
        new_topics.append(_clean_topic(topic))
    new_settings["topics"] = new_topics
    return new_settings


def _keep_backward_compatibility(settings):
    if "local_repo" in settings:
        settings["download_folder"] = settings["local_repo"]
    if "topic" in settings:
        settings["topics"] = [settings]
    if "jobs" in settings:
        settings["topics"] = settings["jobs"]
    if "download_key_file" in settings:
        settings["dci_key_file"] = settings["download_key_file"]
    if "download_crt_file" in settings:
        settings["dci_cert_file"] = settings["download_crt_file"]
    return settings


def _get_remoteci_id(env_variables):
    remoteci_id = env_variables.get("DCI_CLIENT_ID")
    if remoteci_id:
        return remoteci_id.split("/")[1]
    return None


def _get_dci_downloader_home_folder(env_variables):
    DEFAULT_XDG_DATA_HOME = os.path.join(os.path.expanduser("~"), ".local", "share")
    data_home_path = env_variables.get("XDG_DATA_HOME", DEFAULT_XDG_DATA_HOME)
    return os.path.join(data_home_path, "dci-downloader")


def get_settings(sys_args, env_variables={}):
    cli_arguments = parse_arguments(sys_args)
    dci_home_path = _get_dci_downloader_home_folder(env_variables)
    key = env_variables.get("DCI_KEY_FILE", os.path.join(dci_home_path, "dci.key"))
    crt = env_variables.get("DCI_CERT_FILE", os.path.join(dci_home_path, "dci.crt"))
    settings = {
        "remoteci_id": _get_remoteci_id(env_variables),
        "env_variables": env_variables,
        "topics": [cli_arguments],
        "download_folder": _get_download_folder(cli_arguments, env_variables),
        "dci_key_file": key,
        "dci_cert_file": crt,
    }
    settings_file_path = cli_arguments["settings_file_path"]
    if settings_file_path:
        settings_from_file = _read_settings_file(settings_file_path)
        settings.update(_keep_backward_compatibility(settings_from_file))
    return _clean_settings(settings)


def _variants_are_invalid(topic):
    topic_variants = {
        "RHEL-7": [
            "Server-NFV",
            "Server-RT",
            "Server-SAP",
            "Server-SAPHANA",
            "Server-optional",
            "Server",
        ],
        "RHEL-8": [
            "AppStream",
            "BaseOS",
            "CRB",
            "HighAvailability",
            "NFV",
            "RT",
            "ResilientStorage",
            "SAP",
            "SAPHANA",
            "unified",
        ],
    }
    invalid = False
    for topic_name, variants in topic_variants.items():
        current_topic_name = topic["name"]
        current_variants = [v["name"] for v in topic["variants"]]
        variants_not_allowed = set(current_variants) - set(variants + ["metadata"])
        if current_topic_name.startswith(topic_name) and variants_not_allowed:
            invalid = True
            print(
                "Variants %s for the %s topic are not valid"
                % (", ".join(variants_not_allowed), current_topic_name)
            )
            print(
                "The authorized variants for %s are %s."
                % (current_topic_name, ", ".join(variants))
            )
            break
    return invalid


def exit_if_settings_invalid(settings):
    has_error = False
    for env_variable in ["DCI_CLIENT_ID", "DCI_API_SECRET", "DCI_CS_URL"]:
        if env_variable not in settings["env_variables"]:
            has_error = True
            print("Environment variable %s not set" % env_variable)

    if settings["download_folder"] is None:
        has_error = True
        print("The destination folder for the download is not specified.")

    topics = settings["topics"]
    if not topics:
        has_error = True
        print("You need to specify at least one topic")

    for topic in topics:
        if _variants_are_invalid(topic):
            has_error = True

    if has_error:
        sys.exit(1)
