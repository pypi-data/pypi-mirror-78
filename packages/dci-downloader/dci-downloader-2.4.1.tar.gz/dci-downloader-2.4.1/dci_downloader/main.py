#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import signal
import traceback
import time

from dci_downloader import api
from dci_downloader import downloader
from dci_downloader.fs import file_lock, get_topic_folder
from dci_downloader.certificates import configure_ssl_certificates
from dci_downloader.settings import get_settings, exit_if_settings_invalid


if sys.version_info[0] == 3:
    LOCK_IO_ERROR = BlockingIOError  # noqa: F821
else:
    LOCK_IO_ERROR = IOError


def signal_handler(sig, frame):
    print("Exiting...")
    sys.exit(130)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def download_components(settings):
    if "component_id" in settings and settings["component_id"]:
        component_id = settings["component_id"]
        component = api.get_component_by_id(component_id)
        topic_id = component["topic_id"]
        topic = api.get_topic_by_id(topic_id)
        components = [component]
    else:
        topic_name = settings["name"]
        topic = api.get_topic(topic_name)
        if topic is None:
            raise Exception("Topic name %s not found" % topic_name)
        components = api.get_components(topic)
    for component in components:
        downloader.download_component(topic, component, settings)


def download_topic(settings):
    not_finished = True
    count = 0
    ten_hours = 10 * 60 * 60
    sleep = 30
    while not_finished or count < (ten_hours / sleep):
        try:
            topic_path = get_topic_folder(settings)
            lock_file = os.path.join(topic_path, '.lock')
            with file_lock(lock_file):
                download_components(settings)
                not_finished = False
        except LOCK_IO_ERROR:
            time.sleep(sleep)
            count += 1


def main():
    settings = get_settings(sys_args=sys.argv[1:], env_variables=dict(os.environ))
    exit_if_settings_invalid(settings)
    configure_ssl_certificates(settings)
    return_code = 0
    for topic_settings in settings["topics"]:
        topic_name = topic_settings["name"]
        try:
            download_topic(topic_settings)
        except Exception:
            print("Exception when downloading components for %s" % topic_name)
            traceback.print_exc()
            return_code = 1
    sys.exit(return_code)


if __name__ == "__main__":
    main()
