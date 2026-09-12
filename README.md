# zepto_data_project

## install & Run
```bash
pip install requests beautifulsoup4 pandas
```
open `data_pipeline/data_pipeline.ipynb` and run all cell top to bottom. This produces `data_pipeline/books.db`.

## currency coversion
Fixed baseline rate used: **1 GBP = 105.50 INR** (project-defined constant, not a live rate).

## Cleaning Decisions
1.price: stripped `£` ,converted to float (`price_gbp`)
2.rating: mapped text ("Three") to  integer (1-5) via a lookup dictionary
3.Availability: converted to Boolean `in_stock` by checking for text 'In stock'
4.Missing/unparseable values: handled via median-imputation (not dropped), to preserve row count. no rows needed imputation in this run (all 71 parsed successfully).

## Schema
1.categories(category_id PK, category_name)
2.books(book_id PK, title,price_gbp, price_inr, rating, in_stock, category_id FK)

## Dataset
71 books across 4 categories: Travel, Mystery, Historical Fiction, Sequential Art.

## concusion 
-done with module-1

Repository maintained by vishnuvardhan
