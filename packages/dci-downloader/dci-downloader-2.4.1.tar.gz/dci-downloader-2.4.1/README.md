# DCI Downloader

`dci-downloader` is a useful tool for downloading the latest versions of Red Hat products

## TLDR

```console
$ sudo yum -y install https://packages.distributed-ci.io/dci-release.el7.noarch.rpm
$ sudo yum -y install dci-downloader
$ source ~/dcirc.sh
$ dci-downloader RHEL-8 /tmp/repo
```

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

## Requirements

### Red Hat SSO

DCI is connected to the Red Hat SSO. You will need a [Red Hat account](https://access.redhat.com/).

### Remoteci

A remoteci is a Virtual Machine or a baremetal server running RHEL.
You should check that your remoteci:

- Is running the latest RHEL 7 release.
- Has enough free space in the destination folder.
- Should be able to reach:
  - `https://api.distributed-ci.io` (443).
  - `https://repo.distributed-ci.io` (443).

## Installation

The `dci-downloader` is packaged and available as a RPM files.

```console
$ sudo yum -y install https://packages.distributed-ci.io/dci-release.el7.noarch.rpm
$ sudo yum -y install dci-downloader
```

## Limitation

At the moment it is not possible to perform two parallel downloads in two different processes. If you use a configuration file with multiple topics, the download is done synchronously topic after topic.

## Configuration

### Remoteci creation

DCI is connected to the Red Hat SSO. You need to log in `https://www.distributed-ci.io` with your redhat.com SSO account. Your user account will be created in our database the first time you connect.

After the first connection you can create a remoteci. Go to [https://www.distributed-ci.io/remotecis](https://www.distributed-ci.io/remotecis) and click `Create a new remoteci` button. Once your `remoteci` is created, you can retrieve the connection information in the `Authentication` column. Save those information in `~/dcirc.sh` file.

At this point, you can validate your credentials with the following commands:

```console
$ source ~/dcirc.sh
$ dcictl remoteci-list
```

If you see your remoteci in the list, everything is working great so far.

### Topic access

Before using dci-downloader, we need to check the list of topic (version of the product) you have access to:

```console
$ source ~/dcirc.sh
$ dcictl topic-list
```

If you don't see any topic then **you should contact your EPM at Red Hat** which will give you access to the topic you need.
/!\ Only RHEL topics are supported at the moment

## Usage

You can now download the latest version of a product using dci-downloader.

Example command to download the latest RHEL 8 compose into /tmp/repo folder.

```console
$ dci-downloader RHEL-8 /tmp/repo
```

## Options

By default dci-downloader will download all variants for x86_64 architecture without debug RPMs.

### Download other architectures

To download a specific architecture you can specify those using `--arch` option

```console
$ dci-downloader RHEL-8 /tmp/repo --arch x86_64 --arch ppc64le
```

### Specific variants

To download only specific variants you can specify those using `--variant`

```console
$ dci-downloader RHEL-8 /tmp/repo --variant AppStream --variant BaseOS
```

### Download the whole component

To download everything you can add the `--all` flag

```console
$ dci-downloader RHEL-8 /tmp/repo --all
```

### Debug RPMs

To download debug RPMs you can add the `--debug` flag

```console
$ dci-downloader RHEL-8 /tmp/repo --variant AppStream --debug
```

### Settings file

You can use a settings file to send parameters to parameterize dci-downloader.

Use `--settings` parameter:

```console
$ dci-downloader --settings "/etc/dci-rhel-agent/settings.yml"
```

All settings from settings.yml file will overwrite cli parameters.

Examples of a settings file:

```yaml
download_folder: /var/www/html
topics:
  - topic: RHEL-7.8
    archs:
      - x86_64
      - ppc64le
    variants:
      - Server
      - Server-SAP
  - topic: RHEL-8.1
    archs:
      - x86_64
    variants:
      - AppStream
      - name: BaseOS
        with_debug: true
```

## SSL certificates

dci-downloader downloads SSL certificates prior the download phase. To customize the CRT and KEY path you can change `DCI_KEY_FILE` and `DCI_CERT_FILE` env variables.

If you are using `settings.yml` file change

```
dci_key_file: /etc/dci-rhel-agent/dci.key
dci_cert_file: /etc/dci-rhel-agent/dci.crt
```

## Proxy

If you are using a proxy, just add `HTTP_PROXY` or `HTTPS_PROXY` env variable pointing to your proxy.


## License

Apache License, Version 2.0 (see [LICENSE](LICENSE) file)

## Help

If something is not working correctly, ensure you have the latest version installed

```console
$ dci-downloader --version
$ dci-downloader --help
```

## Contact

Email: Distributed-CI Team <distributed-ci@redhat.com>
IRC: #distributed-ci on Freenode
