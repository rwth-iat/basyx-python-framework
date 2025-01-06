# Server Development Status

> [!warning]
> This README tracks the development progress of the server's endpoints. Endpoints are sorted based on the
> specification's services (Submodel, AASX File Server, ...).

- **Implemented (✅)**: Currently available, but **not necessarily fully functional**.
- **Planned (📅)**: Scheduled for future implementation.
- **Not Planned (❌)**: Currently not scheduled for implementation.

> [!warning]
> The project is WIP and endpoints might be declared as 'Implemented' whilst still having issues.

Below is the status table for the endpoints, organized as specified.

## AAS Service
| Endpoint                           | Operation | Description                                     | Status |
|------------------------------------|-----------|-------------------------------------------------|--------|
| `/aas`                             | GET       | Returns the Asset Administration Shell          | 📅     |
| `/aas`                             | PUT       | Replaces the current Asset Administration Shell | 📅     |
| `/aas/submodel-refs`               | GET       | Returns all Submodel References                 | 📅     |
| `/aas/submodel-refs`               | POST      | Creates a Submodel Reference                    | 📅     |
| `/aas/submodel-refs/{submodel_id}` | DELETE    | Deletes a Submodel Reference                    | 📅     |
| `/aas/asset-information`           | GET       | Returns the Asset Information                   | 📅     |
| `/aas/asset-information`           | PUT       | Replaces the Asset Information                  | 📅     |
| `/aas/asset-information/thumbnail` | GET       | Returns the thumbnail file                      | 📅     |
| `/aas/asset-information/thumbnail` | PUT       | Replaces the thumbnail file                     | 📅     |
| `/aas/asset-information/thumbnail` | DELETE    | Deletes the thumbnail file                      | 📅     |


## Submodel Service
| Endpoint                                                                             | Operation | Description                                                                  | Status |
|--------------------------------------------------------------------------------------|-----------|------------------------------------------------------------------------------|--------|
| `/submodels/`                                                                        | GET       | Retrieve all submodels                                                       | ✅      |
| `/submodels/`                                                                        | POST      | Create a new submodel                                                        | ✅      |
| `/submodels/$metadata`                                                               | GET       | Retrieve metadata for all submodels                                          | 📅     |
| `/submodels/$reference`                                                              | GET       | Retrieve reference for all submodels                                         | 📅     |
| `/submodels/$value`                                                                  | GET       | Retrieve values of all submodels                                             | ❌      |
| `/submodels/$path`                                                                   | GET       | Retrieve submodels by a specific path                                        | ❌      |
| `/submodels/{submodel_id}`                                                           | GET       | Retrieve a submodel by ID                                                    | ✅      |
| `/submodels/{submodel_id}`                                                           | PUT       | Update a submodel by ID                                                      | ✅      |
| `/submodels/{submodel_id}`                                                           | DELETE    | Delete a submodel by ID                                                      | ✅      |
| `/submodels/{submodel_id}/$metadata`                                                 | GET       | Retrieve metadata of a specific submodel                                     | 📅     |
| `/submodels/{submodel_id}/$metadata`                                                 | PATCH     | Update metadata of a specific submodel                                       | 📅     |
| `/submodels/{submodel_id}/$value`                                                    | GET       | Retrieve values of a specific submodel                                       | ❌      |
| `/submodels/{submodel_id}/$reference`                                                | GET       | Retrieve reference of a specific submodel                                    | 📅     |
| `/submodels/{submodel_id}/$path`                                                     | GET       | Retrieve a specific submodel by path                                         | ❌      |
| `/submodels/{submodel_id}/submodel-elements`                                         | GET       | Retrieve all elements of a specific submodel                                 | ✅      |
| `/submodels/{submodel_id}/submodel-elements`                                         | POST      | Create new elements in a specific submodel                                   | 📅     |
| `/submodels/{submodel_id}/submodel-elements/$metadata`                               | GET       | Retrieve metadata for submodel elements                                      | 📅     |
| `/submodels/{submodel_id}/submodel-elements/$reference`                              | GET       | Retrieve references for submodel elements                                    | 📅     |
| `/submodels/{submodel_id}/submodel-elements/$value`                                  | GET       | Retrieve values for submodel elements                                        | ❌      |
| `/submodels/{submodel_id}/submodel-elements/$path`                                   | GET       | Retrieve elements by path in a specific submodel                             | ❌      |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}`                             | GET       | Retrieve specific elements by short ID in a submodel                         | 📅     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}`                             | POST      | Create specific elements by short ID in a submodel                           | 📅     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}`                             | PUT       | Update specific elements by short ID in a submodel                           | 📅     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}`                             | DELETE    | Delete specific elements by short ID in a submodel                           | 📅     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}`                             | PATCH     | Partially update specific elements by short ID in a submodel                 | ❌      |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/$metadata`                   | GET       | Retrieve metadata of specific elements by short ID                           | 📅     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/$metadata`                   | PATCH     | Update metadata of specific elements by short ID                             | ❌      |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/$reference`                  | GET       | Retrieve reference of specific elements by short ID                          | 📅     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/$value`                      | GET       | Retrieve values of specific elements by short ID                             | ❌      |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/$value`                      | PATCH     | Update values of specific elements by short ID                               | ❌      |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/attachment`                  | GET       | Retrieve attachments of specific elements by short ID                        | 📅     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/attachment`                  | PUT       | Update attachments of specific elements by short ID                          | 📅     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/attachment`                  | DELETE    | Delete attachments of specific elements by short ID                          | 📅     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/invoke`                      | POST      | Invoke operations on specific elements by short ID                           | ❌      |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/invoke/$value`               | POST      | Invoke operations with value on specific elements by short ID                | ❌      |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/invoke-async`                | POST      | Asynchronously invoke operations on specific elements by short ID            | ❌      |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/invoke-async/$value`         | POST      | Asynchronously invoke operations with value on specific elements by short ID | ❌      |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/qualifiers`                  | GET       | Retrieve qualifiers for specific elements by short ID                        | 📅     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/qualifiers`                  | POST      | Add qualifiers to specific elements by short ID                              | 📅     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/qualifiers/{qualifier_type}` | GET       | Retrieve qualifiers of a specific type for specific elements by short ID     | 📅     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/qualifiers/{qualifier_type}` | PUT       | Update qualifiers of a specific type for specific elements by short ID       | 📅     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/qualifiers/{qualifier_type}` | DELETE    | Delete qualifiers of a specific type for specific elements by short ID       | 📅     |

## AASX File Server Interface and Operations
| Endpoint                  | Operation | Description | Status |
|---------------------------|-----------|-------------|--------|
| `/GetAllAASXPackageIds/`  | GET       | TODO        | 📅     |
| `/GetAASXByPackageId/`    | POST      | TODO        | 📅     |
| `/PostAASXPackage/`       | POST      | TODO        | 📅     |
| `/PutAASXByPackageId/`    | PUT       | TODO        | 📅     |
| `/DeleteAASXByPackageId/` | DELETE    | TODO        | 📅     |

## AAS Registry Service
| Endpoint                             | Operation | Description                                        | Status |
|--------------------------------------|-----------|----------------------------------------------------|--------|
| `/registry/aas-descriptors`          | GET       | Returns all Asset Administration Shell Descriptors | 📅     |
| `/registry/aas-descriptors/{aas_id}` | GET       | Returns an AAS Descriptor by ID                    | 📅     |
| `/registry/aas-descriptors`          | POST      | Creates an AAS Descriptor                          | 📅     |
| `/registry/aas-descriptors/{aas_id}` | PUT       | Updates an AAS Descriptor                          | 📅     |
| `/registry/aas-descriptors/{aas_id}` | DELETE    | Deletes an AAS Descriptor                          | 📅     |

## Submodel Registry Service
| Endpoint                                       | Operation | Description                         | Status |
|------------------------------------------------|-----------|-------------------------------------|--------|
| `/registry/submodel-descriptors`               | GET       | Returns all Submodel Descriptors    | 📅     |
| `/registry/submodel-descriptors/{submodel_id}` | GET       | Returns a Submodel Descriptor by ID | 📅     |
| `/registry/submodel-descriptors`               | POST      | Creates a Submodel Descriptor       | 📅     |
| `/registry/submodel-descriptors/{submodel_id}` | PUT       | Updates a Submodel Descriptor       | 📅     |
| `/registry/submodel-descriptors/{submodel_id}` | DELETE    | Deletes a Submodel Descriptor       | 📅     |

## Discovery Service
| Endpoint                          | Operation | Description                          | Status |
|-----------------------------------|-----------|--------------------------------------|--------|
| `/discovery/aas-ids`              | GET       | Returns all AAS IDs by an Asset Link | 📅     |
| `/discovery/asset-links/{aas_id}` | GET       | Returns all Asset Links by an AAS ID | 📅     |
| `/discovery/asset-links/{aas_id}` | POST      | Posts new Asset Links                | 📅     |
| `/discovery/asset-links/{aas_id}` | DELETE    | Deletes Asset Links                  | 📅     |

## AAS Repository Service
| Endpoint                                   | Operation | Description                                 | Status |
|--------------------------------------------|-----------|---------------------------------------------|--------|
| `/shells`                                  | GET       | Returns all Asset Administration Shells     | 📅     |
| `/shells/{aas_id}`                         | GET       | Returns an Asset Administration Shell by ID | 📅     |
| `/shells/{aas_id}`                         | PUT       | Updates an Asset Administration Shell by ID | 📅     |
| `/shells/{aas_id}`                         | DELETE    | Deletes an Asset Administration Shell by ID | 📅     |
| `/shells/{aas_id}/asset-information`       | GET       | Returns Asset Information for an AAS        | 📅     |
| `/shells/{aas_id}/submodels`               | GET       | Returns all Submodels for an AAS            | 📅     |
| `/shells/{aas_id}/submodels/{submodel_id}` | GET       | Returns a Submodel by ID for an AAS         | 📅     |

## Submodel Repository Service
| Endpoint                   | Operation | Description              | Status |
|----------------------------|-----------|--------------------------|--------|
| `/submodels`               | GET       | Returns all Submodels    | 📅     |
| `/submodels/{submodel_id}` | GET       | Returns a Submodel by ID | 📅     |
| `/submodels/{submodel_id}` | PUT       | Updates a Submodel by ID | 📅     |
| `/submodels/{submodel_id}` | DELETE    | Deletes a Submodel by ID | 📅     |

## ConceptDescription Repository Service
| Endpoint                             | Operation | Description                         | Status |
|--------------------------------------|-----------|-------------------------------------|--------|
| `/concept-descriptions`              | GET       | Returns all Concept Descriptions    | 📅     |
| `/concept-descriptions/{concept_id}` | GET       | Returns a Concept Description by ID | 📅     |
| `/concept-descriptions/{concept_id}` | POST      | Creates a new Concept Description   | 📅     |
| `/concept-descriptions/{concept_id}` | PUT       | Updates a Concept Description by ID | 📅     |
| `/concept-descriptions/{concept_id}` | DELETE    | Deletes a Concept Description by ID | 📅     |