# Purchase Order App

A small PyQt5 desktop app: register a customer, then place a purchase
order for one or more products and pay.

This version has been modernized from the original:

- **Database migrated from Oracle to MySQL** (`cx_Oracle` → `mysql-connector-python`).
- **No more hard-coded credentials.** Connection settings come from a `.env` file.
- **Parameterized SQL everywhere** — the original built INSERT statements with
  raw string concatenation, which was vulnerable to SQL injection.
- **Restructured into a proper package** (`app/`) instead of two loose scripts,
  with a shared `db.py` data-access layer and a `products.py` catalog module.
- Friendly error dialogs instead of crashing if the database is unreachable
  or an optional asset (like `icon.jpg`) is missing.

## Project layout

```
main.py                 # entry point
app/
  config.py              # env loading + asset path helper
  db.py                   # MySQL connection + queries
  products.py             # product catalog
  customer_form.py        # customer registration window
  purchase_order_form.py  # purchase order window
assets/                  # images used by the GUI
db/
  schema.sql             # MySQL schema + seed data
docker-compose.yml       # optional local MySQL for development
.env.example             # copy to .env and fill in
requirements.txt
```

## Setup

1. **Install dependencies** (Python 3.10+):

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Get a MySQL database.** Any free-tier option works — a local
   install, or the bundled Docker Compose file:

   ```bash
   docker compose up -d
   ```

3. **Create the schema:**

   ```bash
   mysql -h 127.0.0.1 -u root -p < db/schema.sql
   ```

4. **Configure credentials:**

   ```bash
   cp .env.example .env
   # then edit .env with your DB_HOST / DB_USER / DB_PASSWORD / DB_NAME
   ```

5. **Run the app:**

   ```bash
   python main.py
   ```

## Notes

- The original code referenced an `icon.jpg` window icon that wasn't
  actually included in the project; the app now just skips the icon if
  that file isn't present in `assets/`.
- The product catalog is defined once in `app/products.py` and also
  seeded into the `PRODUCT` table in `db/schema.sql`, so `PRODUCTORDER.pid`
  can be a real foreign key instead of a free-floating string.
