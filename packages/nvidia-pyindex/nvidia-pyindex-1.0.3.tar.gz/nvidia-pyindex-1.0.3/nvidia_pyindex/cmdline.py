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
import sys

from nvidia_pyindex.utils import get_configuration_files


def uninstall():
    file_dict = get_configuration_files()

    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("Uninstalling NVIDIA Pip Configuration ...")
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    for key, files in file_dict.items():
        for file in files:
            try:

                backup_file = "{}.old".format(file)
                if all([os.path.isfile(_f) for _f in [file, backup_file]]):
                    print("Removing custom configuration file: %s ..." % file)
                    try:
                        os.remove(file)
                    except:
                        print("Error deleting: {}".format(file))

                    try:
                        os.rename(backup_file, file)
                    except:
                        print("Error renaming: `{}` to  `{}`".format(
                            backup_file,
                            file
                        ))
            except (FileNotFoundError, PermissionError) as e:
                print("Error: {}: {}".format(e.__class__.__name__, str(e)))
                pass


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "uninstall":
        uninstall()
    else:
        raise RuntimeError(
            "Incorrect usage: `nvidia_pyindex uninstall`\n."
            "Received: %s" % sys.argv
        )


if __name__ == "__main__":
    sys.exit(main())
