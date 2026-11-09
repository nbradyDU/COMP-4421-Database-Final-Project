# CEPD generator

Generates synthetic data for five communities, 30,000
memberships and eight TSV files. 

## Code

- `generate_seed.py`: CLI, export and summary.
- `community_data.py`: curated names, activities, parameters and columns.
- `build_data.py`: populations, events and participation.
- `validate_data.py`: validates data after creation

## Run

```powershell
python generator/generate_seed.py --seed 20260501
```

## Generated Files

The `generator/output/` directory contains eight TSV files, one for each table

| File | Contents |
|---|---|
| `platform_user.tsv` | Platform user accounts |
| `organization.tsv` | Organizations |
| `organization_membership.tsv` | User memberships in organizations |
| `organization_group.tsv` | Groups within organizations |
| `group_membership.tsv` | User memberships in groups |
| `event.tsv` | Community events |
| `event_rsvp.tsv` | Event registrations and responses |
| `event_attendance.tsv` | Event check-in records |

## Import

Use an **empty schema** created from `sql/schema.sql`. Start the client from
the repository root:

```powershell
mysql --local-infile=1 --default-character-set=utf8mb4 -u YOUR_IMPORT_USER -p cems_db
```
