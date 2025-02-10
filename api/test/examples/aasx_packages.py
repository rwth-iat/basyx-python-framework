from aas_core3 import jsonization

aasx_package_json = {"id": "aasx_package_test", "assetInformation": {"assetKind": "Type"}, "modelType": "AssetAdministrationShell"}
aasx_package = jsonization.asset_administration_shell_from_jsonable(aasx_package_json)
