# Copyright (c) 2023 the Eclipse BaSyx Authors
#
# This program and the accompanying materials are made available under the terms of the MIT License, available in
# the LICENSE file of this project.
#
# SPDX-License-Identifier: MIT
"""
The dicts defined in this module are used in the json and xml modules to translate enum members of our
implementation to the respective string and vice versa.
"""
import os
from typing import BinaryIO, Dict, IO, Type, Union


# type aliases for path-like objects and IO
# used by write_aas_xml_file, read_aas_xml_file, write_aas_json_file, read_aas_json_file
Path = Union[str, bytes, os.PathLike]
PathOrBinaryIO = Union[Path, BinaryIO]
PathOrIO = Union[Path, IO]  # IO is TextIO or BinaryIO

# XML Namespace definition
XML_NS_MAP = {"aas": "https://admin-shell.io/aas/3/0"}
XML_NS_AAS = "{" + XML_NS_MAP["aas"] + "}"