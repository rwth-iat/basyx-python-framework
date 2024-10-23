# Copyright (c) 2023 the Eclipse BaSyx Authors
#
# This program and the accompanying materials are made available under the terms of the MIT License, available in
# the LICENSE file of this project.
#
# SPDX-License-Identifier: MIT
"""
.. _adapter.json.json_serialization:

Module for serializing Asset Administration Shell objects to the official JSON format

The module provides an custom JSONEncoder classes :class:`AASToJsonEncoder` and :class:`StrippedAASToJsonEncoder`
to be used with the Python standard :mod:`json` module. While the former serializes objects as defined in the
specification, the latter serializes stripped objects, excluding some attributes
(see https://git.rwth-aachen.de/acplt/pyi40aas/-/issues/91).
Each class contains a custom :meth:`~.AASToJsonEncoder.default` function which converts BaSyx Python SDK objects to
simple python types for an automatic JSON serialization.
To simplify the usage of this module, the :meth:`write_aas_json_file` and :meth:`object_store_to_json` are provided.
The former is used to serialize a given :class:`~basyx.AbstractObjectStore` to a file, while the
latter serializes the object store to a string and returns it.

The serialization is performed in an iterative approach: The :meth:`~.AASToJsonEncoder.default` function gets called for
every object and checks if an object is an BaSyx Python SDK object. In this case, it calls a special function for the
respective BaSyx Python SDK class which converts the object (but not the contained objects) into a simple Python dict,
which is serializable. Any contained  BaSyx Python SDK objects are included into the dict as they are to be converted
later on. The special helper function ``_abstract_classes_to_json`` is called by most of the
conversion functions to handle all the attributes of abstract base classes.
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


