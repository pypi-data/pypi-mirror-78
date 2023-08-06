import errno
import os
import fcntl


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        elif exc.errno in [errno.EPERM, errno.EACCES]:
            print("Permission error on %s" % path)
        else:
            raise


def create_parent_dir(path):
    mkdir_p(os.path.dirname(path))


def delete_all_symlink_in_path(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.islink(file_path):
                os.unlink(file_path)
        for dir in dirs:
            folder_path = os.path.join(root, dir)
            if os.path.islink(folder_path):
                os.unlink(folder_path)


def recreate_symlinks(symlinks, destination_path):
    for symlink in symlinks:
        link_path = os.path.join(destination_path, symlink["path"], symlink["name"])
        os.symlink(symlink["destination"], link_path)


def get_topic_folder(settings):
    topic_name = settings["name"].strip().replace(" ", "_")
    download_folder = settings["download_folder"]
    return os.path.join(download_folder, topic_name)


def get_component_folder(settings, component):
    topic_folder = get_topic_folder(settings)
    component_type = component["type"].strip().replace(" ", "_").lower()
    return os.path.join(topic_folder, component_type)


class file_lock(object):
    def __init__(self, file_path):
        self.lock_fd = open(file_path, "a")
        fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def __enter__(self):
        return self.lock_fd

    def __exit__(self, type, value, traceback):
        os.remove(self.lock_fd.name)
        fcntl.flock(self.lock_fd, fcntl.LOCK_UN)
        self.lock_fd.close()
