# Zepto_data_project

## Install & Run

```bash
pip install requests beautifulsoup4 pandas
```

Open `data_pipeline/data_pipeline.ipynb` and run all calls top to bottom. This produces `data_pipeline/books.db`.


## Currency Decisions
1. price: stripped `£`, converted to float (`price_gbp`)
2. Rating: mapped text ("Three") to integer (1-5) via a lookup dictionary
3. Availability: converted to boolean `in_stock` by checking for the text "In stock"
4. Missing/unparseable values: handled via median-imputation (not dropped), to preserve row count. No rows needed imputation in this run (all 71 parsed successfully).

## Schema
1. categories(category_id PK, category_name)
2. books(book_id PK, title, price_gbp, price_inr, rating, in_stock, category_id FK)


## Dataset
71 books across 4 categories: Travel, Mystery, Historical Fiction, Squential Art.
