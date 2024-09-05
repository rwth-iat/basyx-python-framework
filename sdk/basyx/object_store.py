# Copyright (c) 2024 the Eclipse BaSyx Authors
#
# This program and the accompanying materials are made available under the terms of the MIT License, available in
# the LICENSE file of this project.
#
# SPDX-License-Identifier: MIT
"""
This module implements Registries for the AAS, in order to enable resolving global
:attr:`~basyx.aas.model.base.Identifier` and mapping
:attr:`~basyx.aas.model.base.Identifier` to :class:`~basyx.aas.model.base.Identifiable` objects.
"""

import abc
import typing
from typing import MutableSet, Iterator, Generic, TypeVar, Dict, List, Optional, Iterable

from aas_core3.types import Identifiable, Referable, Class

""" TODO: Add docstring """
_IdentifiableType = TypeVar('_IdentifiableType', bound=Identifiable)


class AbstractObjectProvider(metaclass=abc.ABCMeta):
    """
    Abstract baseclass for all objects, that allow to retrieve :class:`~basyx.aas.model.base.Identifiable` objects
    (resp. proxy objects for remote :class:`~basyx.aas.model.base.Identifiable` objects) by their
    :attr:`~basyx.aas.model.base.Identifier`

    This includes local object stores, database clients and AAS API clients.
    """

    @abc.abstractmethod
    def get_identifiable(self, identifier: str) -> Identifiable:
        """
        Find an :class:`~basyx.aas.model.base.Identifiable` by its :attr:`~basyx.aas.model.base.Identifier`

        This may include looking up the object's endpoint in a registry and fetching it from an HTTP server or a
        database.

        :param identifier: :attr:`~basyx.aas.model.base.Identifier` of the object to return
        :return: The :class:`~basyx.aas.model.base.Identifiable` object (or a proxy object for a remote
                 :class:`~basyx.aas.model.base.Identifiable` object)
        :raises KeyError: If no such :class:`~.basyx.aas.model.base.Identifiable` can be found
        """
        pass

    def get(self, identifier: str, default: Optional[Identifiable] = None) -> Optional[Identifiable]:
        """
        Find an object in this set by its :attr:`id <basyx.aas.model.base.Identifier>`, with fallback parameter

        :param identifier: :class:`~basyx.aas.model.base.Identifier` of the object to return
        :param default: An object to be returned, if no object with the given
                        :attr:`id <basyx.aas.model.base.Identifier>` is found
        :return: The :class:`~basyx.aas.model.base.Identifiable` object with the given
                 :attr:`id <basyx.aas.model.base.Identifier>` in the provider. Otherwise, the ``default`` object
                 or None, if none is given.
        """
        try:
            return self.get_identifiable(identifier)
        except KeyError:
            return default


class AbstractObjectStore(AbstractObjectProvider, MutableSet[_IdentifiableType], Generic[_IdentifiableType],
                          metaclass=abc.ABCMeta):
    """
    Abstract baseclass of for container-like objects for storage of :class:`~basyx.aas.model.base.Identifiable` objects.

    ObjectStores are special ObjectProvides that – in addition to retrieving objects by
    :attr:`~basyx.aas.model.base.Identifier` – allow to add and delete objects (i.e. behave like a Python set).
    This includes local object stores (like :class:`DictObjectStore <basyx.aas.model.provider.DictObjectStore>`)
    and database :class:`Backends <basyx.aas.backend.backends.Backend>`.

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
    A local in-memory object store for :class:`~basyx.aas.model.base.Identifiable` objects, backed by a dict, mapping
    :attr:`~basyx.aas.model.base.Identifier` → :class:`~basyx.aas.model.base.Identifiable`
    """

    def __init__(self, objects: Iterable[_IdentifiableType] = ()) -> None:
        self._backend: Dict[str, _IdentifiableType] = {}
        for x in objects:
            self.add(x)

    def descend(self) -> Iterator["Class"]:
        """Iterate recursively over all the instances referenced from this one."""
        if self._backend is not None:
            for identifiable in self._backend.values():
                yield identifiable

                yield from identifiable.descend()

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

    def get_referable(self, identifier: str, id_short: str) -> Referable:
        referable: Referable
        identifiable = self.get_identifiable(identifier)
        for element in identifiable.descend():

            if (
                    isinstance(element, Referable) and id_short == element.id_short
            ):
                return element
        raise KeyError("Referable object with short_id {} does not exist for identifiable object with id {}"
                       .format(id_short, identifier))

    def get_children_referable(self, id_short: str) -> List[Referable]:
        referable_id_short: List[Referable] = []
        for referable in self.descend():
            if isinstance(referable, Referable) and id_short == referable.id_short:
                referable_id_short.append(referable)
        if len(referable_id_short) == 0:
            raise KeyError("there is no referable with id_short {}".format(id_short))
        if len(referable_id_short) != 1:
            raise KeyError("there are multiple referables with id_short {}".format(id_short))

        referable_list: list[Referable] = []
        for element in referable_id_short[0].descend():
            if isinstance(element, Referable):
                referable_list.append(element)
        return referable_list

    @typing.no_type_check  # TODO fix typing
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
