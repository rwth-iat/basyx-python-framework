# Copyright (c) 2024 the Eclipse BaSyx Authors
#
# This program and the accompanying materials are made available under the terms of the MIT License, available in
# the LICENSE file of this project.
#
# SPDX-License-Identifier: MIT
"""
This module implements Registries for the AAS, in order to enable resolving global
`Identifiers`; and mapping `Identifiers` to `Identifiable` objects.
"""

import abc
from typing import MutableSet, Iterator, Generic, TypeVar, Dict, List, Optional, Iterable

from aas_core3.types import Identifiable, Referable, Class

""" TODO: Add docstring """
_IdentifiableType = TypeVar('_IdentifiableType', bound=Identifiable)
""" TODO: Add docstring """
_ReferableType = TypeVar('_ReferableType', bound=Referable)


class AbstractObjectProvider(metaclass=abc.ABCMeta):
    """
    Abstract baseclass for all objects, that allow to retrieve `Identifiable` objects
    (resp. proxy objects for remote `Identifiable` objects) by their `Identifier`.

    This includes local object stores, database clients and AAS API clients.
    """

    @abc.abstractmethod
    def get_identifiable(self, identifier: str) -> Identifiable:
        """
        Find an `Identifiable` by its `Identifier`

        This may include looking up the object's endpoint in a registry and fetching it from an HTTP server or a
        database.

        :param identifier: `Identifier` of the object to return
        :return: The `Identifiable` object (or a proxy object for a remote `Identifiable` object)
        :raises KeyError: If no such `Identifiable` can be found
        """
        pass

    def get(self, identifier: str, default: Optional[Identifiable] = None) -> Optional[Identifiable]:
        """
        Find an object in this set by its `Identifier`, with fallback parameter

        :param identifier: `Identifier` of the object to return
        :param default: An object to be returned, if no object with the given `Identifier` is found
        :return: The `Identifiable` object with the given `Identifier` in the provider. Otherwise, the ``default``
                 object or None, if none is given.
        """
        try:
            return self.get_identifiable(identifier)
        except KeyError:
            return default


class AbstractObjectStore(AbstractObjectProvider, MutableSet[_IdentifiableType], Generic[_IdentifiableType], metaclass=abc.ABCMeta):
    """
    Abstract baseclass of for container-like objects for storage of `Identifiable` objects.

    ObjectStores are special ObjectProvides that – in addition to retrieving objects by
    `Identifier` – allow to add and delete objects (i.e. behave like a Python set).
    This includes local object stores (like `DictObjectStore`) and database `Backends`.

    The AbstractObjectStore inherits from the :class:`~collections.abc.MutableSet` abstract collections class and
    therefore implements all the functions of this class.
    """

    @abc.abstractmethod
    def __init__(self):
        pass

    def update(self, other: Iterable[_IdentifiableType]) -> None:
        for x in other:
            self.add(x)


class ObjectStore(AbstractObjectStore[_IdentifiableType], Generic[_IdentifiableType]):
    """
    A local in-memory object store for `Identifiable` objects, backed by a dict, mapping
    `Identifier` → `Identifiable`
    """

    def __init__(self, objects: Iterable[_IdentifiableType] = ()) -> None:
        self._backend: Dict[str, _IdentifiableType] = {}
        for x in objects:
            self.add(x)

    def get_identifiable(self, identifier: str) -> _IdentifiableType:
        return self._backend[identifier]

    def add(self, x: _IdentifiableType) -> None:
        if x.id in self._backend and self._backend.get(x.id) is not x:
            raise KeyError("Identifiable object with same id {} is already stored in this store"
                           .format(x.id))
        self._backend[x.id] = x

    def discard(self, x: _IdentifiableType) -> None:
        if self._backend.get(x.id) is x:
            del self._backend[x.id]

    def get_referable(self, identifier: str, id_short: str) -> _ReferableType:
        referable: Referable
        identifiable = self.get_identifiable(identifier)
        for referable in identifiable.descend():

            if (
                    issubclass(type(referable), Referable)
                    and id_short in referable.id_short
            ):
                return referable

    def get_children_referable(self, id_short: str) -> [Referable]:
        referable: Referable
        for identifiable in self._backend.values():
            if identifiable.id_short == id_short:
                return identifiable.descend()
            for referable in identifiable.descend():
                if (
                        issubclass(type(referable), Referable)
                        and id_short in referable.id_short
                ):
                    return list(referable.descend())
        raise KeyError("there is no referable with id_short {}".format(id_short))

    def get_parent_referable(self, id_short: str) -> Referable:
        referable: Referable
        referable_descended: Referable
        for identifiable in self._backend.values():
            for referable in identifiable.descend():
                if (
                        issubclass(type(referable), Referable)
                        and id_short in [referable_descended.id_short
                                         for referable_descended in referable.descend_once()]
                ):
                    return referable
        raise KeyError("there is no parent Identifiable for id_short {}".format(id_short))

    def __contains__(self, x: object) -> bool:
        if isinstance(x, str):
            return x in self._backend
        if not isinstance(x, Identifiable):
            return False
        return self._backend.get(x.id) is x

    def __len__(self) -> int:
        return len(self._backend)

    def __iter__(self) -> Iterator[_IdentifiableType]:
        return iter(self._backend.values())


class ObjectProviderMultiplexer(AbstractObjectProvider):
    """
    A multiplexer for Providers of `Identifiable` objects.

    This class combines multiple registries of `Identifiable` objects into a single one
    to allow retrieving `Identifiable` objects from different sources.
    It implements the :class:`~.AbstractObjectProvider` interface to be used as registry itself.

    :ivar providers: A list of :class:`AbstractObjectProviders <.AbstractObjectProvider>` to query when looking up an
                      object
    """

    def __init__(self, registries: Optional[List[AbstractObjectProvider]] = None):
        self.providers: List[AbstractObjectProvider] = registries if registries is not None else []

    def get_identifiable(self, identifier: str) -> Identifiable:
        for provider in self.providers:
            try:
                return provider.get_identifiable(identifier)
            except KeyError:
                pass
        raise KeyError("Identifier could not be found in any of the {} consulted registries."
                       .format(len(self.providers)))
