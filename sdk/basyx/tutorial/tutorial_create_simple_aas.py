import json
import aas_core3.types as aas_types
import aas_core3.jsonization as aas_jsonization
from basyx.object_store import ObjectStore
from basyx.aasx import AASXWriter, AASXReader, DictSupplementaryFileContainer
import pyecma376_2  # The base library for Open Packaging Specifications. We will use the OPCCoreProperties class.
import datetime
from pathlib import Path  # Used for easier handling of auxiliary file's local path

Referencetype = aas_types.ReferenceTypes("ModelReference")

key_types = aas_types.KeyTypes("Submodel")

key = aas_types.Key(value="some-unique-global-identifier", type=key_types)

reference = aas_types.Reference(type=Referencetype, keys=[key])

submodel = aas_types.Submodel(
    id="some-unique-global-identifier",
    submodel_elements=[
        aas_types.Property(
            id_short="some_property",
            value_type=aas_types.DataTypeDefXSD.INT,
            value="1984",
            semantic_id=reference
        )
    ]
)

file_store = DictSupplementaryFileContainer()

with open(Path(__file__).parent / 'data' / 'TestFile.pdf', 'rb') as f:
    actual_file_name = file_store.add_file("/aasx/suppl/MyExampleFile.pdf", f, "application/pdf")

if submodel.submodel_elements is not None:
    submodel.submodel_elements.append(aas_types.File(id_short="documentationFile",
                                                     content_type="application/pdf",
                                                     value=actual_file_name))

aas = aas_types.AssetAdministrationShell(id="urn:x-test:aas1",
                                         asset_information=aas_types.AssetInformation(
                                             asset_kind=aas_types.AssetKind.TYPE),
                                         submodels=[reference])

obj_store: ObjectStore = ObjectStore()
obj_store.add(aas)
obj_store.add(submodel)


# Serialize to a JSON-able mapping
jsonable = aas_jsonization.to_jsonable(submodel)


meta_data = pyecma376_2.OPCCoreProperties()
meta_data.creator = "Chair of Process Control Engineering"
meta_data.created = datetime.datetime.now()

with AASXWriter("./MyAASXPackage.aasx") as writer:
    writer.write_aas(aas_ids=["urn:x-test:aas1"],
                     object_store=obj_store,
                     file_store=file_store,
                     write_json=False)
    writer.write_core_properties(meta_data)

new_object_store: ObjectStore = ObjectStore()
new_file_store = DictSupplementaryFileContainer()

with AASXReader("./MyAASXPackage.aasx") as reader:
    # Read all contained AAS objects and all referenced auxiliary files
    reader.read_into(object_store=new_object_store,
                     file_store=new_file_store)

print(new_object_store.__len__())
for item in file_store.__iter__():
    print(item)

for item in new_file_store.__iter__():
    print(item)
