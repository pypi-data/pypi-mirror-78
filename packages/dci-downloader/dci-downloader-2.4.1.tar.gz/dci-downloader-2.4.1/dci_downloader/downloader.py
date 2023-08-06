#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from dci_downloader.api import get_files_list, get_base_url, download_files
from dci_downloader.stats import check_download_folder_size
from dci_downloader.filters import filter_files_list
from dci_downloader.files_list import get_files_to_download, get_files_to_remove
from dci_downloader.fs import (
    mkdir_p,
    delete_all_symlink_in_path,
    recreate_symlinks,
    get_component_folder,
)


def clean_download_folder(files_list, download_folder):
    if not os.path.isdir(download_folder):
        mkdir_p(download_folder)

    for file in get_files_to_remove(files_list, download_folder):
        print("Remove file %s" % file)
        os.remove(file)

    delete_all_symlink_in_path(download_folder)


def download_component(topic, component, settings):
    print("Download component %s" % component["name"])
    base_url = get_base_url(topic, component)
    files_list = get_files_list(base_url, settings)
    download_folder = get_component_folder(settings, component)
    clean_download_folder(files_list, download_folder)
    files_list = filter_files_list(files_list, settings)
    files_to_download = get_files_to_download(base_url, download_folder, files_list)
    check_download_folder_size(files_to_download, download_folder)
    download_files(files_to_download["files"], settings)
    recreate_symlinks(files_list["symlinks"], download_folder)
