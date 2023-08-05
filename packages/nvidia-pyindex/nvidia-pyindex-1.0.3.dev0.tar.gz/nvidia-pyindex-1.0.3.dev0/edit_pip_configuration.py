#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from urllib.parse import urlparse

__all__ = [
    "create_pip_config_file",
    "maybe_edit_pip_config_file"
]

NVIDIA_PyPI_SERVERS = [
    "https://pypi.ngc.nvidia.com",
]


def _get_host_from_url(url):
    parsed_uri = urlparse(url)
    return '{uri.netloc}'.format(uri=parsed_uri)


def _format_extra_index_url(url):
    return "%s%s\n" % (" " * 18, url)


def _format_trusted_host(url):
    return "%s%s\n" % (" " * 15, _get_host_from_url(url))


def create_pip_config_file(filepath):

    try:
        print("Creating dir:", os.path.dirname(filepath))
        os.makedirs(os.path.dirname(filepath))
    except FileExistsError:
        pass

    with open(filepath, 'w') as _file:
        content = """[global]
timeout = 60
no-cache-dir = true
index-url = https://pypi.org/simple
extra-index-url =
{extra_index_urls}
trusted-host =
{trusted_hosts}
"""
        extra_index_urls = list()
        trusted_hosts = list()

        for nvidia_pypi_server in NVIDIA_PyPI_SERVERS:
            extra_index_urls.append(_format_extra_index_url(nvidia_pypi_server))
            trusted_hosts.append(_format_trusted_host(nvidia_pypi_server))

        _file.write(
            content.format(
                extra_index_urls="".join(extra_index_urls),
                trusted_hosts="".join(trusted_hosts),
            )
        )


def maybe_edit_pip_config_file(filepath):
    with open(filepath, 'r') as _file:
        original_contents = _file.readlines()

    with open("%s.old" % filepath, 'w') as _file:
        _file.writelines(original_contents)

    # Add `no-cache-dir = true`
    for i in range(len(original_contents)):
        line = original_contents[i]
        if line.startswith("no-cache-dir", 0, 12):
            original_contents[i] = "no-cache-dir = true\n"
            break
    else:
        original_contents.append("no-cache-dir = true\n")

    # Remove from `extra-index-url` and `trusted-host` the nvidia prod packages
    try:
        for i in range(len(original_contents)):

            if "nvidia.com" in original_contents[i]:
                del original_contents[i]
    except IndexError:
        pass

    # Add the `extra-index-url(s)` and `trusted-host` for nvidia python packages
    for nvidia_pypi_server in NVIDIA_PyPI_SERVERS:

        contains_index_url = any(
            [nvidia_pypi_server in line for line in original_contents]
        )

        if not contains_index_url:

            for i in range(len(original_contents)):
                line = original_contents[i]
                if line.startswith("extra-index-url", 0, 15):
                    original_contents.insert(
                        i+1,
                        _format_extra_index_url(nvidia_pypi_server)
                    )
                    break
            else:
                original_contents += [
                    "extra-index-url =\n",
                    _format_extra_index_url(nvidia_pypi_server)
                ]

            for i in range(len(original_contents)):
                line = original_contents[i]
                if line.startswith("trusted-host", 0, 12):
                    original_contents.insert(
                        i+1,
                        _format_trusted_host(nvidia_pypi_server)
                    )
                    break
            else:
                original_contents += [
                    "trusted-host =\n",
                    _format_trusted_host(nvidia_pypi_server)
                ]

        else:
            print("`%s` has been skipped ..." % nvidia_pypi_server)

    with open(filepath, 'w') as _file:
        _file.writelines(original_contents)
