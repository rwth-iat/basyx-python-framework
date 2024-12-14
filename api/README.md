# Server Development Status

> [!warning]
> This README tracks the development progress of the server's endpoints. Endpoints are sorted based on the
> specification's services (Submodel, AASX File Server, ...).

- **Implemented**: Currently available, but **not necessarily fully functional**.
- **Planned**: Scheduled for future implementation.
- **Not Planned**: Currently not scheduled for implementation.

> [!warning]
> The project is WIP and endpoints might be declared as 'Implemented' whilst still having problems.

Below is the status table for the endpoints, organized as specified.

## Submodel Service
| Endpoint                                                                             | Operation | Description | Status      |
|--------------------------------------------------------------------------------------|-----------|-------------|-------------|
| `/submodels/`                                                                        | GET       | TODO        | Implemented |
| `/submodels/`                                                                        | POST      | TODO        | Planned     |
| `/submodels/$metadata`                                                               | GET       | TODO        | Planned     |
| `/submodels/$reference`                                                              | GET       | TODO        | Planned     |
| `/submodels/$value`                                                                  | GET       | TODO        | Not Planned |
| `/submodels/$path`                                                                   | GET       | TODO        | Not Planned |
| `/submodels/{submodel_id}`                                                           | GET       | TODO        | Implemented |
| `/submodels/{submodel_id}`                                                           | PUT       | TODO        | Implemented |
| `/submodels/{submodel_id}`                                                           | DELETE    | TODO        | Implemented |
| `/submodels/{submodel_id}/$metadata`                                                 | GET       | TODO        | Planned     |
| `/submodels/{submodel_id}/$metadata`                                                 | PATCH     | TODO        | Planned     |
| `/submodels/{submodel_id}/$value`                                                    | GET       | TODO        | Not Planned |
| `/submodels/{submodel_id}/$reference`                                                | GET       | TODO        | Planned     |
| `/submodels/{submodel_id}/$path`                                                     | GET       | TODO        | Not Planned |
| `/submodels/{submodel_id}/submodel-elements`                                         | GET       | TODO        | Implemented |
| `/submodels/{submodel_id}/submodel-elements`                                         | POST      | TODO        | Planned     |
| `/submodels/{submodel_id}/submodel-elements/$metadata`                               | GET       | TODO        | Planned     |
| `/submodels/{submodel_id}/submodel-elements/$reference`                              | GET       | TODO        | Planned     |
| `/submodels/{submodel_id}/submodel-elements/$value`                                  | GET       | TODO        | Not Planned |
| `/submodels/{submodel_id}/submodel-elements/$path`                                   | GET       | TODO        | Not Planned |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}`                             | GET       | TODO        | Planned     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}`                             | POST      | TODO        | Planned     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}`                             | PUT       | TODO        | Planned     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}`                             | DELETE    | TODO        | Planned     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}`                             | PATCH     | TODO        | Not Planned |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/$metadata`                   | GET       | TODO        | Planned     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/$metadata`                   | PATCH     | TODO        | Not Planned |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/$reference`                  | GET       | TODO        | Planned     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/$value`                      | GET       | TODO        | Not Planned |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/$value`                      | PATCH     | TODO        | Not Planned |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/attachment`                  | GET       | TODO        | Planned     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/attachment`                  | PUT       | TODO        | Planned     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/attachment`                  | DELETE    | TODO        | Planned     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/invoke`                      | POST      | TODO        | Not Planned |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/invoke/$value`               | POST      | TODO        | Not Planned |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/invoke-async`                | POST      | TODO        | Not Planned |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/invoke-async/$value`         | POST      | TODO        | Not Planned |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/qualifiers`                  | GET       | TODO        | Planned     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/qualifiers`                  | POST      | TODO        | Planned     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/qualifiers/{qualifier_type}` | GET       | TODO        | Planned     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/qualifiers/{qualifier_type}` | PUT       | TODO        | Planned     |
| `/submodels/{submodel_id}/submodel-elements/{id_shorts}/qualifiers/{qualifier_type}` | DELETE    | TODO        | Planned     |

Tables for the remaining services will follow.