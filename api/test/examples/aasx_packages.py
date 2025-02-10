from aas_core3.types import AssetAdministrationShell
from aas_core3 import jsonization

json = {"id": "aasx_package_test", "assetInformation": {"assetKind": "Type"}, "modelType": "AssetAdministrationShell"}
aasx_package = jsonization.asset_administration_shell_from_jsonable(json)
