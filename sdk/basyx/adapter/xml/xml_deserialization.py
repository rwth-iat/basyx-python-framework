# Copyright (c) 2023 the Eclipse BaSyx Authors
#
# This program and the accompanying materials are made available under the terms of the MIT License, available in
# the LICENSE file of this project.
#
# SPDX-License-Identifier: MIT
"""
.. _adapter.xml.xml_deserialization:

Module for deserializing Asset Administration Shell data from the official XML format

This module provides the following functions for parsing XML documents:

- :func:`read_aas_xml_file_into` constructs all elements of an XML document and stores them in a given
  :class:`ObjectStore <basyx.ObjectStore>`
- :func:`read_aas_xml_file` constructs all elements of an XML document and returns them in a
  :class:`~basyx.ObjectStore`


.. code-block::

    KeyError: aas:id on line 252 has no attribute with name idType!
        -> Failed to construct aas:id on line 252 using construct_identifier!
        -> Failed to construct aas:conceptDescription on line 247 using construct_concept_description!



"""

from aas_core3 import types as model
from lxml import etree
import logging
import aas_core3.xmlization as aas_xmlization
from basyx.object_store import ObjectStore, Identifiable

from typing import Any, Callable, Dict, Iterable, Optional, Set, Tuple, Type, TypeVar, List
from .._generic import XML_NS_MAP, XML_NS_AAS, PathOrIO

NS_AAS = XML_NS_AAS
REQUIRED_NAMESPACES: Set[str] = {XML_NS_MAP["aas"]}

logger = logging.getLogger(__name__)

T = TypeVar("T")
RE = TypeVar("RE", bound=model.RelationshipElement)


def _element_pretty_identifier(element: etree._Element) -> str:
    """
    Returns a pretty element identifier for a given XML element.

    If the prefix is known, the namespace in the element tag is replaced by the prefix.
    If additionally also the sourceline is known, it is added as a suffix to name.
    For example, instead of "{https://admin-shell.io/aas/3/0}assetAdministrationShell" this function would return
    "aas:assetAdministrationShell on line $line", if both, prefix and sourceline, are known.

    :param element: The xml element.
    :return: The pretty element identifier.
    """
    identifier = element.tag
    if element.prefix is not None:
        # Only replace the namespace by the prefix if it matches our known namespaces,
        # so the replacement by the prefix doesn't mask errors such as incorrect namespaces.
        namespace, tag = element.tag.split("}", 1)
        if namespace[1:] in XML_NS_MAP.values():
            identifier = element.prefix + ":" + tag
    if element.sourceline is not None:
        identifier += f" on line {element.sourceline}"
    return identifier


def _parse_xml_document(file: PathOrIO, failsafe: bool = True, **parser_kwargs: Any) -> Optional[etree._Element]:
    """
    Parse an XML document into an element tree

    :param file: A filename or file-like object to read the XML-serialized data from
    :param failsafe: If True, the file is parsed in a failsafe way: Instead of raising an Exception if the document
                     is malformed, parsing is aborted, an error is logged and None is returned
    :param parser_kwargs: Keyword arguments passed to the XMLParser constructor
    :raises ~lxml.etree.XMLSyntaxError: If the given file(-handle) has invalid XML
    :raises KeyError: If a required namespace has not been declared on the XML document
    :return: The root element of the element tree
    """

    parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, **parser_kwargs)

    try:
        root = etree.parse(file, parser).getroot()
    except etree.XMLSyntaxError as e:
        if failsafe:
            logger.error(e)
            return None
        raise e

    missing_namespaces: Set[str] = REQUIRED_NAMESPACES - set(root.nsmap.values())
    if missing_namespaces:
        error_message = f"The following required namespaces are not declared: {' | '.join(missing_namespaces)}" \
                        + " - Is the input document of an older version?"
        if not failsafe:
            raise KeyError(error_message)
        logger.error(error_message)
    return root


def read_aas_xml_file_into(object_store: ObjectStore, file: PathOrIO,
                           replace_existing: bool = False, ignore_existing: bool = False) -> Set[str]:
    """
    Read an Asset Administration Shell XML file according to 'Details of the Asset Administration Shell', chapter 5.4
    into a given :class:`ObjectStore <basyx.aas.model.provider.AbstractObjectStore>`.

    :param object_store: The :class:`ObjectStore <basyx.aas.model.provider.AbstractObjectStore>` in which the
                         :class:`~basyx.aas.model.base.Identifiable` objects should be stored
    :param file: A filename or file-like object to read the XML-serialized data from
    :param replace_existing: Whether to replace existing objects with the same identifier in the object store or not
    :param ignore_existing: Whether to ignore existing objects (e.g. log a message) or raise an error.
                            This parameter is ignored if replace_existing is True.
    :param parser_kwargs: Keyword arguments passed to the XMLParser constructor
    :raises ~lxml.etree.XMLSyntaxError: If the given file(-handle) has invalid XML
    :raises KeyError: If a required namespace has not been declared on the XML document
    :raises KeyError: Encountered a duplicate identifier
    :raises KeyError: Encountered an identifier that already exists in the given ``object_store`` with both
                     ``replace_existing`` and ``ignore_existing`` set to ``False``
    :raises (~basyx.aas.model.base.AASConstraintViolation, KeyError, ValueError): Errors during
                                                                                  construction of the objects
    :raises TypeError: Encountered an undefined top-level list (e.g. ``<aas:submodels1>``)
    :return: A set of :class:`Identifiers <basyx.aas.model.base.Identifier>` that were added to object_store
    """
    ret: Set = set()

    element_constructors: Dict[str, Callable[..., model.Identifiable]] = {
        "assetAdministrationShell": aas_xmlization.asset_administration_shell_from_str,
        "conceptDescription": aas_xmlization.concept_description_from_str,
        "submodel": aas_xmlization.submodel_from_str
    }

    element_constructors = {NS_AAS + k: v for k, v in element_constructors.items()}

    root = etree.parse(file).getroot()


    if root is None:
        return ret
    # Add AAS objects to ObjectStore
    for list_ in root:

        element_tag = list_.tag[:-1]
        if list_.tag[-1] != "s" or element_tag not in element_constructors:
            error_message = f"Unexpected top-level list {_element_pretty_identifier(list_)}!"

            logger.warning(error_message)
            continue

        for element in list_:
            str = etree.tostring(element).decode("utf-8-sig")
            constructor = element_constructors[element_tag](str)

            if constructor.id in ret:
                error_message = f"{element} has a duplicate identifier already parsed in the document!"
                raise KeyError(error_message)
            existing_element = object_store.get(constructor.id)
            if existing_element is not None:
                if not replace_existing:
                    error_message = f"object with identifier {constructor.id} already exists " \
                                    f"in the object store: {existing_element}!"
                    if not ignore_existing:
                        raise KeyError(error_message + f" failed to insert {constructor}!")
                    logger.info(error_message + f" skipping insertion of {constructor}...")
                    continue
                object_store.discard(existing_element)
            object_store.add(constructor)
            ret.add(constructor.id)

    return ret


def read_aas_xml_file(file: PathOrIO, **kwargs: Any) -> ObjectStore[Identifiable]:
    """
    A wrapper of :meth:`~basyx.adapter.xml.xml_deserialization.read_aas_xml_file_into`, that reads all objects in an
    empty :class:`~basyx.ObjectStore`. This function supports
    the same keyword arguments as :meth:`~basyx.adapter.xml.xml_deserialization.read_aas_xml_file_into`.

    :param file: A filename or file-like object to read the XML-serialized data from
    :param kwargs: Keyword arguments passed to :meth:`~basyx.aas.adapter.xml.xml_deserialization.read_aas_xml_file_into`
    :raises ~lxml.etree.XMLSyntaxError: If the given file(-handle) has invalid XML
    :raises KeyError: If a required namespace has not been declared on the XML document
    :raises KeyError: Encountered a duplicate identifier
    :raises (~basyx.aas.model.base.AASConstraintViolation, KeyError, ValueError): Errors during
                                                                                  construction of the objects
    :raises TypeError: Encountered an undefined top-level list (e.g. ``<aas:submodels1>``)
    :return: A :class:`~basyx.ObjectStore` containing all AAS objects from the XML file
    """
    obj_store: ObjectStore[Identifiable] = ObjectStore()
    read_aas_xml_file_into(obj_store, file, **kwargs)
    return obj_store
