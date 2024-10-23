from lxml import etree
from typing import Callable, Dict, Optional, Type
import base64

from aas_core3 import types as model
from .. import _generic
from basyx.object_store import ObjectStore
import aas_core3.xmlization as aas_xmlization

NS_AAS = _generic.XML_NS_AAS


def _write_element(file: _generic.PathOrBinaryIO, element: etree._Element, **kwargs) -> None:
    etree.ElementTree(element).write(file, encoding="UTF-8", xml_declaration=True, method="xml", **kwargs)


def object_store_to_xml_element(data: ObjectStore) -> etree._Element:
    """
    Serialize a set of AAS objects to an Asset Administration Shell as :class:`~lxml.etree._Element`.
    This function is used internally by :meth:`write_aas_xml_file` and shouldn't be
    called directly for most use-cases.

    :param data: :class:`ObjectStore <basyx.ObjectStore>` which contains different objects of
                 the AAS meta model which should be serialized to an XML file
    """
    # separate different kind of objects
    asset_administration_shells = []
    submodels = []
    concept_descriptions = []
    for obj in data:
        if isinstance(obj, model.AssetAdministrationShell):
            asset_administration_shells.append(obj)
        elif isinstance(obj, model.Submodel):
            submodels.append(obj)
        elif isinstance(obj, model.ConceptDescription):
            concept_descriptions.append(obj)

    # serialize objects to XML
    root = etree.Element(NS_AAS + "environment", nsmap=_generic.XML_NS_MAP)
    if asset_administration_shells:
        et_asset_administration_shells = etree.Element(NS_AAS + "assetAdministrationShells")
        for aas_obj in asset_administration_shells:
            et_asset_administration_shells.append(
                etree.fromstring(aas_xmlization.to_str(aas_obj)))
        root.append(et_asset_administration_shells)
    if submodels:
        et_submodels = etree.Element(NS_AAS + "submodels")
        for sub_obj in submodels:
            et_submodels.append(etree.fromstring(aas_xmlization.to_str(sub_obj)))
        root.append(et_submodels)
    if concept_descriptions:
        et_concept_descriptions = etree.Element(NS_AAS + "conceptDescriptions")
        for con_obj in concept_descriptions:
            et_concept_descriptions.append(etree.fromstring(aas_xmlization.to_str(con_obj)))
        root.append(et_concept_descriptions)
    return root


def write_aas_xml_file(file: _generic.PathOrBinaryIO,
                       data: ObjectStore,
                       **kwargs) -> None:
    """
    Write a set of AAS objects to an Asset Administration Shell XML file according to 'Details of the Asset
    Administration Shell', chapter 5.4

    :param file: A filename or file-like object to write the XML-serialized data to
    :param data: :class:`ObjectStore <basyx.ObjectStore>` which contains different objects of
                 the AAS meta model which should be serialized to an XML file
    :param kwargs: Additional keyword arguments to be passed to :meth:`~lxml.etree._ElementTree.write`
    """
    return _write_element(file, object_store_to_xml_element(data), **kwargs)
