import contextlib
import json
from typing import Dict, Callable, ContextManager, TypeVar, Type, List, IO, Optional, Set, get_args
from aas_core3.types import AssetAdministrationShell, Submodel, ConceptDescription
import aas_core3.jsonization as aas_jsonization

from basyx.object_store import ObjectStore, Identifiable
from .._generic import PathOrIO, Path

T = TypeVar('T')


def _get_ts(dct: Dict[str, object], key: str, type_: Type[T]) -> T:
    """
    Helper function for getting an item from a (str→object) dict in a typesafe way.

    The type of the object is checked at runtime and a TypeError is raised, if the object has not the expected type.

    :param dct: The dict
    :param key: The key of the item to retrieve
    :param type_: The expected type of the item
    :return: The item
    :raises TypeError: If the item has an unexpected type
    :raises KeyError: If the key is not found in the dict (just as usual)
    """
    val = dct[key]
    if not isinstance(val, type_):
        raise TypeError("Dict entry '{}' has unexpected type {}".format(key, type(val).__name__))
    return val


def read_aas_json_file_into(object_store: ObjectStore, file: PathOrIO, replace_existing: bool = False,
                            ignore_existing: bool = False) -> Set[str]:
    """
    Read an Asset Administration Shell JSON file according to 'Details of the Asset Administration Shell', chapter 5.5
    into a given object store.

    :param object_store: The :class:`ObjectStore <basyx.aas.model.provider.AbstractObjectStore>` in which the
                         identifiable objects should be stored
    :param file: A filename or file-like object to read the JSON-serialized data from
    :param replace_existing: Whether to replace existing objects with the same identifier in the object store or not
    :param ignore_existing: Whether to ignore existing objects (e.g. log a message) or raise an error.
                            This parameter is ignored if replace_existing is ``True``.
    :raises KeyError: Encountered a duplicate identifier
    :raises KeyError: Encountered an identifier that already exists in the given ``object_store`` with both
                     ``replace_existing`` and ``ignore_existing`` set to ``False``
    :raises TypeError: **Non-failsafe**: Encountered an element in the wrong list
                                         (e.g. an AssetAdministrationShell in ``submodels``)
    :return: A set of :class:`Identifiers <basyx.aas.model.base.Identifier>` that were added to object_store
    """
    ret: Set[str] = set()

    # json.load() accepts TextIO and BinaryIO
    cm: ContextManager[IO]
    if isinstance(file, get_args(Path)):
        # 'file' is a path, needs to be opened first
        cm = open(file, "r", encoding="utf-8-sig")
    else:
        # 'file' is not a path, thus it must already be IO
        # mypy seems to have issues narrowing the type due to get_args()
        cm = contextlib.nullcontext(file)  # type: ignore[arg-type]

    # read, parse and convert JSON file
    with cm as fp:
        data = json.load(fp)

    for name, expected_type in (('assetAdministrationShells', AssetAdministrationShell),
                                ('submodels', Submodel),
                                ('conceptDescriptions', ConceptDescription)):
        try:
            lst = _get_ts(data, name, list)
        except (KeyError, TypeError):
            continue

        for item in lst:
            identifiable = aas_jsonization.identifiable_from_jsonable(item)

            if identifiable.id in ret:
                error_message = f"{item} has a duplicate identifier already parsed in the document!"
                raise KeyError(error_message)
            existing_element = object_store.get(identifiable.id)
            if existing_element is not None:
                if not replace_existing:
                    error_message = f"object with identifier {identifiable.id} already exists " \
                                    f"in the object store: {existing_element}!"
                    if not ignore_existing:
                        raise KeyError(error_message + f" failed to insert {identifiable}!")
                object_store.discard(existing_element)
            object_store.add(identifiable)
            ret.add(identifiable.id)

    return ret


def read_aas_json_file(file, **kwargs) -> ObjectStore[Identifiable]:
    """
    A wrapper of :meth:`~basyx.adapter.json.json_deserialization.read_aas_json_file_into`, that reads all objects
    in an empty :class:`~basyx.model.provider.DictObjectStore`. This function supports the same keyword arguments as
    :meth:`~basyx.adapter.json.json_deserialization.read_aas_json_file_into`.

    :param file: A filename or file-like object to read the JSON-serialized data from
    :param kwargs: Keyword arguments passed to :meth:`read_aas_json_file_into`
    :raises KeyError: Encountered a duplicate identifier
    :return: A :class:`~basyx.ObjectStore` containing all AAS objects from the JSON file
    """
    obj_store: ObjectStore[Identifiable] = ObjectStore()
    read_aas_json_file_into(obj_store, file, **kwargs)
    return obj_store
