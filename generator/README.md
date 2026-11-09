# CEPD Generator

Generates synthetic data for five fictional communities, including 30,000 organization memberships and eight TSV files.

## Code

- `generate_seed.py`: CLI, export, and summary.
- `community_data.py`: Community names, activities, parameters, and columns.
- `build_data.py`: Generates users, memberships, events, and participation.
- `validate_data.py`: Validates generated records.

## Run

From the repository root:

```powershell
python generator/generate_seed.py --seed 20260501
```

## Generated Files

The `generator/output/` directory contains eight TSV files, one for each database table.

| File | Contents |
|---|---|
| `platform_user.tsv` | Platform user accounts |
| `organization.tsv` | Organizations |
| `organization_membership.tsv` | Organization memberships |
| `organization_group.tsv` | Groups within organizations |
| `group_membership.tsv` | Group memberships |
| `event.tsv` | Community events |
| `event_rsvp.tsv` | Event registrations and responses |
| `event_attendance.tsv` | Attendance and absence records |

## Import

After creating the empty `cepd_db` database using `sql/schema.sql`, enable MySQL `LOCAL INFILE` as described in the root README.

From the repository root:

```powershell
mysql --local-infile=1 --default-character-set=utf8mb4 -u root -p cepd_db
```

Inside MySQL:

```sql
SOURCE sql/seed.sql
```

Confirm all 143,014 records imported with zero skipped rows or warnings. See the root `README.md` for complete setup instructions.