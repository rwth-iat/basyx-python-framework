# Copyright (c) 2024 the Eclipse BaSyx Authors
#
# This program and the accompanying materials are made available under the terms of the MIT License, available in
# the LICENSE file of this project.
#
# SPDX-License-Identifier: MIT

import unittest

from basyx.object_store import ObjectStore, ObjectProviderMultiplexer  # type: ignore
from aas_core3.types import Identifiable, AssetAdministrationShell, AssetInformation, AssetKind
import aas_core3.types as aas_types


class ProvidersTest(unittest.TestCase):
    def setUp(self) -> None:
        self.aas1 = AssetAdministrationShell(id="urn:x-test:aas1",
                                             asset_information=AssetInformation(asset_kind=AssetKind.TYPE))

        self.aas2 = AssetAdministrationShell(id="urn:x-test:aas2",
                                             asset_information=AssetInformation(asset_kind=AssetKind.TYPE))

        some_element = aas_types.Property(
            id_short="some_property",
            value_type=aas_types.DataTypeDefXSD.INT,
            value="1984"
        )

        another_element = aas_types.Blob(
            id_short="some_blob",
            content_type="application/octet-stream",
            value=b'\xDE\xAD\xBE\xEF'
        )

        self.list_element = aas_types.Blob(
            id_short="list_1",
            content_type="application/octet-stream",
            value=b'\xDE\xAD\xBE\xEF'
        )

        self.another_list_element = aas_types.Blob(
            id_short="list_2",
            content_type="application/octet-stream",
            value=b'\xDE\xAD\xBE\xEF'
        )

        self.element_list = aas_types.SubmodelElementList(id_short='ExampleSubmodelList',
                                                          type_value_list_element=aas_types.AASSubmodelElements.
                                                          SUBMODEL_ELEMENT_LIST,
                                                          value=[self.list_element, self.another_list_element])

        self.submodel1 = aas_types.Submodel(
            id="urn:x-test:submodel1",
            submodel_elements=[
                some_element,
                another_element,
                self.element_list
            ]
        )
        self.submodel2 = aas_types.Submodel(
            id="urn:x-test:submodel2",
            submodel_elements=[
                some_element
            ]
        )

    def test_store_retrieve(self) -> None:
        object_store: ObjectStore[Identifiable] = ObjectStore()
        object_store.add(self.aas1)
        object_store.add(self.aas2)
        self.assertIn(self.aas1, object_store)
        property = aas_types.Property('test')  # type: ignore
        self.assertFalse(property in object_store)
        aas3 = AssetAdministrationShell(id="urn:x-test:aas1", asset_information=AssetInformation(
            global_asset_id="http://acplt.org/TestAsset/", asset_kind=AssetKind.NOT_APPLICABLE))
        with self.assertRaises(KeyError) as cm:
            object_store.add(aas3)
        self.assertEqual("'Identifiable object with same id urn:x-test:aas1 is already "
                         "stored in this store'", str(cm.exception))
        self.assertEqual(2, len(object_store))
        self.assertIs(self.aas1,
                      object_store.get_identifiable("urn:x-test:aas1"))
        self.assertIs(self.aas1,
                      object_store.get("urn:x-test:aas1"))
        object_store.discard(self.aas1)
        object_store.discard(self.aas1)
        with self.assertRaises(KeyError) as cm:
            object_store.get_identifiable("urn:x-test:aas1")
        self.assertIsNone(object_store.get("urn:x-test:aas1"))
        self.assertEqual("'urn:x-test:aas1'", str(cm.exception))
        self.assertIs(self.aas2, object_store.pop())
        self.assertEqual(0, len(object_store))

    def test_store_update(self) -> None:
        object_store1: ObjectStore[Identifiable] = ObjectStore()
        object_store1.add(self.aas1)
        object_store2: ObjectStore[Identifiable] = ObjectStore()
        object_store2.add(self.aas2)
        object_store1.update(object_store2)
        self.assertIsInstance(object_store1, ObjectStore)
        self.assertIn(self.aas2, object_store1)

    def test_provider_multiplexer(self) -> None:
        aas_object_store: ObjectStore[Identifiable] = ObjectStore()
        aas_object_store.add(self.aas1)
        aas_object_store.add(self.aas2)
        submodel_object_store: ObjectStore[aas_types.Submodel] = ObjectStore()
        submodel_object_store.add(self.submodel1)
        submodel_object_store.add(self.submodel2)

        multiplexer = ObjectProviderMultiplexer([aas_object_store, submodel_object_store])
        self.assertIs(self.aas1, multiplexer.get_identifiable("urn:x-test:aas1"))
        self.assertIs(self.submodel1, multiplexer.get_identifiable("urn:x-test:submodel1"))
        with self.assertRaises(KeyError) as cm:
            multiplexer.get_identifiable("urn:x-test:submodel3")
        self.assertEqual("'Identifier could not be found in any of the 2 consulted registries.'",
                         str(cm.exception))

    def test_get_children_referable(self) -> None:
        object_store: ObjectStore[Identifiable] = ObjectStore()
        object_store.add(self.submodel1)
        children = object_store.get_children_referable("urn:x-test:submodel1", 'ExampleSubmodelList')
        assert self.list_element in children
        assert self.another_list_element in children

    def test_get_parent_identifiable(self) -> None:
        object_store: ObjectStore[Identifiable] = ObjectStore()
        object_store.add(self.submodel1)
        object_store.add(self.submodel2)
        parent_referable = object_store.get_parent_referable("list_1")
        assert parent_referable == self.element_list
