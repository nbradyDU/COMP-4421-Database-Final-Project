# Community Events and Participation Database (CEPD)

**Course:** COMP-4421-1 — Database Organization & Mgmt I

MySQL database showing relational database design, synthetic-data generation with Python, data importing, SQL analysis, and visualization using Jupyter, pandas, and Matplotlib.

## Repository Structure

| Location | Contents |
|---|---|
| `sql/schema.sql` | Eight MySQL tables, relationships, and constraints |
| `sql/seed.sql` | Imports generated data into MySQL |
| `sql/queries/` | Eight assignment SQL queries and `all_queries.sql` |
| `sql/results/` | Saved query outputs |
| `generator/` | Python data generator and TSV output files |
| `visualization/` | Database connector, Jupyter notebooks, and charts |
| `docs/` | Report, ER diagram, and data dictionary |
| `config/db.example.json` | Database connection template |

## Setup and Execution

**Requirements:** Python 3.11 or newer, MySQL 8.0.16 or newer, and VS Code with Python and Jupyter extensions.

Run PowerShell commands from the repository root.

1. **Install dependencies:**
   ```powershell
   python -m pip install -r requirements.txt
   ```

2. **Configure connection:**
   ```powershell
   Copy-Item config/db.example.json config/db.json
   ```
   Update `config/db.json` with your MySQL credentials and database name `cepd_db`.

3. **Generate data:**
   ```powershell
   python generator/generate_seed.py
   ```

4. **Create database:** Connect to MySQL without selecting a database:
   ```powershell
   mysql -u root -p
   ```
   At the `mysql>` prompt:
   ```sql
   SOURCE sql/schema.sql
   ```

5. **Import data:** Enable local imports on the MySQL server:
   ```sql
   SET GLOBAL local_infile = ON;
   SHOW GLOBAL VARIABLES LIKE 'local_infile';
   EXIT;
   ```
   Reconnect from PowerShell with local imports enabled:
   ```powershell
   mysql --local-infile=1 --default-character-set=utf8mb4 -u root -p cepd_db
   ```
   Import:
   ```sql
   SOURCE sql/seed.sql
   ```
   The tables must be empty before importing. The seed script sets UTC and displays row counts and warnings. Check for zero skipped records and zero warnings; the script does not automatically stop on import warnings.

   Once finished:
   ```sql
   SET GLOBAL local_infile = OFF;
   ```

6. **Verify and analyze:** Confirm the record counts below, then run:
   ```sql
   SOURCE sql/queries/all_queries.sql
   ```
   This executes all eight queries, including the group-only membership check. Saved results are available in `sql/results/`.

7. **Generate charts:** Open the following notebooks in VS Code, select your Python kernel, and use **Run All** with `visualization/` as the working directory:
   - `visualization/01_rsvp_follow_through.ipynb`
   - `visualization/02_community_overview.ipynb`

   Generated charts are saved in `visualization/output/`.

## Dataset

The generator creates synthetic data for five fictional communities.

| Table | Records |
|---|---:|
| `platform_user` | 28,080 |
| `organization` | 5 |
| `organization_membership` | 30,000 |
| `organization_group` | 25 |
| `group_membership` | 39,076 |
| `event` | 378 |
| `event_rsvp` | 27,654 |
| `event_attendance` | 17,796 |
| **Total** | **143,014** |