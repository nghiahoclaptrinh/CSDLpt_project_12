# Query Localization Engine: Regional Sales

A distributed database system demonstrating **query localization** and **selection pushdown** optimization techniques for horizontally fragmented data across multiple sites.

## Project Overview

This project implements a query optimization engine that:
- Fragments a global `Sales` table horizontally across 3 regional sites (North, South, West)
- Parses incoming SQL queries and applies **selection pushdown** to reduce data transfer
- Routes queries to only the necessary sites based on WHERE conditions
- Logs all query execution details for performance analysis

**Key Concept:** Instead of broadcasting queries to all sites, the engine detects region predicates (e.g., `Region='North'`) and sends site-specific queries only to the relevant database.

## Project Structure

```
.
├── engine/
│   ├── fragmenter.py           # Fragment global Sales table into regional CSVs
│   ├── create_database.py      # Load fragments into SQLite databases
│   ├── localizer.py            # Query localization engine (main entry point)
│   ├── executor.py             # Execute queries across all sites (broadcast)
│   ├── api.py                  # Flask API for query submission
│   └── benchmark.py            # Performance benchmarking
│
├── databases/                  # SQLite databases (3 regional sites)
│   ├── sales_north.db
│   ├── sales_south.db
│   └── sales_west.db
│
├── datasets/
│   ├── fragments/              # Fragmented CSV files
│   │   ├── sales_north.csv
│   │   ├── sales_south.csv
│   │   └── sales_west.csv
│   └── sales.csv               # Original global dataset
│
├── logs/
│   ├── query.log               # Query execution log
│   ├── benchmark.csv           # Performance metrics
│   └── comparison_benchmark.csv # Broadcast vs Localization comparison
│
├── docs/                       # Design documentation
│   ├── PHÂN TÍCH THIẾT KẾ HỆ THỐNG DỰA TRÊN LÝ THUYẾT ÖZSU.docx
│   ├── TÀI LIỆU THIẾT KẾ HỆ THỐNG.docx
│   └── ĐỀ XUẤT ĐỒ ÁN MÔN CƠ SỞ DỮ LIỆU PHÂN TÁN.docx
│
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose setup
└── README.md                   # This file
```

## Requirements

- Python 3.11+
- pandas
- flask
- sqlite3 (included with Python)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nghiahoclaptrinh/CSDLpt_project_12.git
   cd "Distributed project 12"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup & Initialization

### Step 1: Fragment the Global Sales Table
```bash
python engine/fragmenter.py
```
This creates 3 CSV fragments in `datasets/fragments/`:
- `sales_north.csv`
- `sales_south.csv`
- `sales_west.csv`

### Step 2: Create Regional Databases
```bash
python engine/create_database.py
```
This loads each fragment into a separate SQLite database in `databases/`:
- `sales_north.db`
- `sales_south.db`
- `sales_west.db`

## Running the Query Localization Engine

### Interactive Mode
```bash
python engine/localizer.py
```
The engine will:
1. Detect target sites from the query
2. Apply selection pushdown optimization
3. Execute site-specific queries
4. Log all operations to `logs/query.log`
5. Return aggregated results

**Example Queries:**
```sql
-- Query only North region
SELECT * FROM Sales WHERE Region='North'

-- Query all sites matching amount condition
SELECT * FROM Sales WHERE Amount > 1000

-- Broadcast to all sites
SELECT COUNT(*) FROM Sales
```

### Using the API
```bash
python engine/api.py
```
Access the API at `http://localhost:5000` and submit queries via POST requests.

### Benchmarking
Run performance tests comparing broadcast vs localization:
```bash
python engine/benchmark.py
python engine/compare_benchmark.py
```

Results are saved to:
- `logs/benchmark.csv` – Single query performance
- `logs/comparison_benchmark.csv` – Broadcast vs Localization comparison

## How Selection Pushdown Works

**Without Pushdown (Broadcast):**
```
Global Query
    ↓
[Query to North DB] → 10 rows
[Query to South DB] → 15 rows
[Query to West DB]  → 8 rows
    ↓
Network Transfer: 33 rows
    ↓
Filter on client side
Result: 10 rows (only North)
```

**With Selection Pushdown (Localization):**
```
Global Query (WHERE Region='North')
    ↓
Parse & Detect Region='North'
    ↓
[Query to North DB only] → 10 rows
    ↓
Network Transfer: 10 rows
    ↓
Result: 10 rows
```

**Performance Benefit:** Reduces network traffic and query execution time by avoiding unnecessary site access.

## Logging & Monitoring

All queries are logged to `logs/query.log` with:
- Timestamp
- Original query
- Target sites selected
- Rows returned
- Execution time

Example log entry:
```
============================
TIME: 2026-06-02 14:30:45.123456
QUERY: SELECT * FROM Sales WHERE Region='North'
TARGET SITES: ['North']
ROWS RETURNED: 10
EXECUTION TIME: 0.045623
```

## Docker Support (Optional)

To run the project in Docker:

**Using Docker Compose:**
```bash
docker compose up --build
```

**Manual Docker:**
```bash
docker build -t csdlpt_project_12 .
docker run --rm -it -v ${PWD}/logs:/app/logs csdlpt_project_12
```

## Design Principles

This project demonstrates key concepts from **Özsu & Valduriez's Distributed Database Design**:

1. **Horizontal Fragmentation** – Sales table split by Region
2. **Selection Pushdown** – Move filtering conditions to fragment sites
3. **Query Localization** – Route queries to relevant fragments
4. **Distributed Optimization** – Minimize network I/O and computation

## Project Team

- Course: Distributed Database Systems (Cơ Sở Dữ Liệu Phân Tán)
- Institution: [Your University]
- Date: 2026

## License

This project is for educational purposes.
