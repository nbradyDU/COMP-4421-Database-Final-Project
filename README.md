# Community Events and Participation Database (CEPD)

**Course:** [COMP-4421-1 — Database Organization & Mgmt I]

MySQL database showing relational database design, synthetic-data generation with Python, data importing, SQL analysis, and visualization using Jupyter, pandas, and Matplotlib.

## Repository Structure

| Location | Contents |
|---|---|
| `sql/schema.sql` | Eight MySQL tables, relationships, and constraints |
| `sql/seed.sql` | Imports generated data into MySQL |
| `sql/queries/` | Eight assignment SQL queries |
| `sql/all_queries.sql` | Runs all eight queries |
| `sql/results/` | Saved query outputs |
| `generator/` | Python data generator and eight TSV output files |
| `visualization/` | Database connector, Jupyter notebooks, and charts |
| `docs/` | Report, ER diagram, and data dictionary |
| `config/db.json` | Local database credentials (Git-ignored) |

## Setup and Execution

1. **Generate data:** Run `python generator/generate_seed.py` from the repository root.
2. **Database connection:** Copy `config/db.example.json` to `config/db.json` and update the MySQL connection information.
3. **Create database:** Execute `sql/schema.sql` in MySQL to create the `cepd_db` database and its tables.
4. **Import data:** Enable `local_infile`, set the MySQL session time zone to `'+00:00'`, and execute `sql/seed.sql`.
5. **Verify import:** Confirm 143,014 records across eight tables, with zero skipped records or warnings. Check event times, foreign key relationships, and group memberships.
6. **Run analysis:** Execute `sql/all_queries.sql` or individual queries in `sql/queries/`. Saved outputs are in `sql/results/`.
7. **Generate charts:** Configure `config/db.json` and run the notebooks in `visualization/`.


## Dataset

The generator creates synthetic data for five fictional communities.

| Data | Records |
|---|---:|
| Platform users | 28,080 |
| Organization memberships | 30,000 |
| Events | 378 |
| RSVPs | 27,654 |
| Attendance records | 17,796 |