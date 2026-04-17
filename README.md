# FurniSearch

A document-store application for managing and searching IKEA furniture data, built with Python and MongoDB. FurniSearch supports bulk data loading, keyword and category-based search with pagination, discount detection, and inventory management through an interactive CLI.

## Features

- **Discount Check** — Look up any furniture item by name and instantly see if it's on sale (compares `old_price` vs current `price`). Handles duplicate names by prompting for item ID selection.
- **Keyword Search** — Search furniture by keyword using MongoDB's `$regex` operator for substring matching. Results display name, category, price, and description with paginated navigation.
- **Category Browse** — View all available categories, select one, and browse items sorted by price (descending). Drill into any item to see full details including designer info.
- **Add New Item** — Insert new furniture into the database with input validation (unique ID enforcement, numeric price checks).
- **Bulk Data Loading** — Load JSON datasets into MongoDB in batches of 100 for efficient ingestion.
- **Paginated Results** — All search results are displayed 5 per page with next/previous/quit navigation.

## Tech Stack

- **Python 3** — application logic and CLI interface
- **MongoDB** — document store for flexible furniture data
- **PyMongo** — Python driver for MongoDB queries, regex search, and aggregations

## Getting Started

**Prerequisites:** Python 3 and a running MongoDB instance.

**1. Clone the repository**

```bash
git clone https://github.com/git-samia/furnisearch.git
cd furnisearch
```

**2. Install dependencies**

```bash
pip install pymongo
```

**3. Load furniture data**

```bash
python load_json.py data/sample_2000.json <port_number>
```

Three sample datasets are included: `sample_10.json`, `sample_100.json`, and `sample_2000.json`.

**4. Run the application**

```bash
python main.py <port_number>
```

Replace `<port_number>` with your MongoDB port (typically `27017`).

## Project Structure

```
furnisearch/
├── main.py           # CLI application — menu, search, and CRUD operations
├── load_json.py      # JSON-to-MongoDB bulk loader (batch insert)
└── data/
    ├── sample_10.json
    ├── sample_100.json
    └── sample_2000.json
```
