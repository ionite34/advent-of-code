| Field              | Previously | Now                                                                     |     |
|--------------------|------------|-------------------------------------------------------------------------|-----|
| inserted_at        | set by db  | sent in infraction post, = last_applied at first                        |     |
| last_applied (new) | --         | sent in infraction post, updated in updated infraction duration changes |     |
| expires_at         |            |                                                                         |     |
