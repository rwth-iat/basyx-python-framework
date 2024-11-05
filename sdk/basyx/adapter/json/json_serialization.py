# Copyright (c) 2023 the Eclipse BaSyx Authors
#
# This program and the accompanying materials are made available under the terms of the Eclipse Public License v. 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0, or the Apache License, Version 2.0 which is available
# at https://www.apache.org/licenses/LICENSE-2.0.
#
# SPDX-License-Identifier: EPL-2.0 OR Apache-2.0
"""
.. _adapter.json.json_serialization:

Module for serializing Asset Administration Shell objects to the official JSON format


"""
import base64
import contextlib
import inspect
import io
import time
from typing import ContextManager, List, Dict, Optional, TextIO, Type, Callable, get_args
import json
from basyx.object_store import ObjectStore
from aas_core3.types import AssetAdministrationShell, Submodel, ConceptDescription
from aas_core3.jsonization import to_jsonable
from .. import _generic

import os
from typing import BinaryIO, Dict, IO, Type, Union

Path = Union[str, bytes, os.PathLike]
PathOrBinaryIO = Union[Path, BinaryIO]
PathOrIO = Union[Path, IO]  # IO is TextIO or BinaryIO


def _create_dict(data: ObjectStore) -> dict:
    # separate different kind of objects
    asset_administration_shells: List = []
    submodels: List = []
    concept_descriptions: List = []
    for obj in data:
        if isinstance(obj, AssetAdministrationShell):
            asset_administration_shells.append(to_jsonable(obj))
        elif isinstance(obj, Submodel):
            submodels.append(to_jsonable(obj))
        elif isinstance(obj, ConceptDescription):
            concept_descriptions.append(to_jsonable(obj))
    dict_: Dict[str, List] = {}
    if asset_administration_shells:
        dict_['assetAdministrationShells'] = asset_administration_shells
    if submodels:
        dict_['submodels'] = submodels
    if concept_descriptions:
        dict_['conceptDescriptions'] = concept_descriptions
    return dict_


class _DetachingTextIOWrapper(io.TextIOWrapper):
    """
    Like :class:`io.TextIOWrapper`, but detaches on context exit instead of closing the wrapped buffer.
    """

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.detach()


def write_aas_json_file(file: PathOrIO, data: ObjectStore, **kwargs) -> None:
    """
    Write a set of AAS objects to an Asset Administration Shell JSON file according to 'Details of the Asset
    Administration Shell', chapter 5.5

    :param file: A filename or file-like object to write the JSON-serialized data to
    :param data: :class:`ObjectStore <basyx.aas.model.provider.AbstractObjectStore>` which contains different objects of
                 the AAS meta model which should be serialized to a JSON file
    :param kwargs: Additional keyword arguments to be passed to `json.dump()`
    """

    # json.dump() only accepts TextIO
    cm: ContextManager[TextIO]
    if isinstance(file, get_args(_generic.Path)):
        # 'file' is a path, needs to be opened first
        cm = open(file, "w", encoding="utf-8")
    elif not hasattr(file, "encoding"):
        # only TextIO has this attribute, so this must be BinaryIO, which needs to be wrapped
        # mypy seems to have issues narrowing the type due to get_args()
        cm = _DetachingTextIOWrapper(file, "utf-8", write_through=True)  # type: ignore[arg-type]
    else:
        # we already got TextIO, nothing needs to be done
        # mypy seems to have issues narrowing the type due to get_args()
        cm = contextlib.nullcontext(file)  # type: ignore[arg-type]
    # serialize object to json#

    with cm as fp:
        json.dump(_create_dict(data), fp, **kwargs)
