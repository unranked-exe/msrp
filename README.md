# MSRP - Modular Shoe Price Scraper

A modular web scraping solution designed to collect and analyze price data for size 10 men's shoes from manufacturer websites. This project was developed as an evolution of a previous internship project, with a focus on clean architecture, modularity, and separation of concerns.

## Project Overview

This scraper system is specifically designed to:

- Extract shoe product data and prices for men's size 10 shoes
- Transform and validate data using type-safe models
- Load processed data into efficient storage formats (Parquet)
- Compare prices across different sources
- Provide a modular, extensible architecture for future enhancements
- Minimize API calls during development through local caching

## Architecture

The project follows a modular design pattern with four main components:

### 1. Extraction Layer (`extract.py`)

- **Purpose**: Handles all data retrieval operations
- **Features**:
  - HTTP client with Chrome browser impersonation using `rnet`
  - Retry logic with exponential backoff for robust API calls
  - Local JSON file caching to prevent excessive API requests during development
  - Both synchronous and asynchronous fetch methods
  - Batch processing capabilities for multiple URLs

### 2. Transformation Layer (`transform.py`)

- **Purpose**: Data validation and structure conversion
- **Features**:
  - Pydantic models for type-safe data handling
  - `SearchItem` model for individual shoe products (productId, displayName, division, price, salePrice)
  - `SearchResults` model for search result collections with timestamps
  - DataFrame utilities for data manipulation
  - Clean conversion from raw JSON to structured Python objects

### 3. Loading Layer (`loader.py`)

- **Purpose**: Handles data persistence and storage
- **Features**:
  - Automatic results directory creation and management
  - Parquet file format support for efficient storage
  - Error handling and logging for data loading operations
  - Extensible design for multiple output formats

### 4. Orchestration Layer (`main.py`)

- **Purpose**: Coordinates the workflow and business logic
- **Features**:
  - Environment variable configuration for API endpoints
  - Query preparation for men's size 10 shoes
  - Integration between extraction, transformation, and loading layers
  - Comprehensive logging with `loguru`

## Key Features

- **Modular Design**: Each component (extraction, transformation, loading, orchestration) can be developed, tested, and maintained independently
- **Browser Impersonation**: Uses `rnet` with Chrome 137 impersonation for realistic requests
- **Robust Error Handling**: Retry mechanisms and comprehensive error logging
- **Development-Friendly**: Local caching prevents hitting APIs repeatedly during testing
- **Type Safety**: Pydantic models ensure data integrity and validation
- **Async Support**: Concurrent processing capabilities for better performance
- **Efficient Storage**: Parquet format for optimized data storage and analysis
- **Timestamped Data**: Automatic request timestamps for data lineage tracking

## Project Structure

```text
msrp/
├── main.py              # Main orchestration script
├── extract.py           # Data extraction module
├── transform.py         # Data transformation and models
├── loader.py            # Data loading and persistence
├── data_store/          # Local data storage
│   ├── search_res.json  # Cached search results
│   ├── products_ex.json # Product examples
│   └── *.csv           # Processed data files
├── results/             # Output directory for processed data
│   └── *.parquet       # Saved analysis results
├── exploratory_analysis.ipynb  # Data analysis notebook
├── pyproject.toml       # Project dependencies
├── uv.lock             # Dependency lock file
└── README.md           # This file
```

## Environment Setup

Required environment variables:

```bash
PRODUCT_API_URL=<your_product_api_endpoint>
SEARCH_QUERY_BASE_URL=<your_search_api_endpoint>
```

## Usage

1. **Set up environment variables** for API endpoints
2. **Run the main script**:

   ```bash
   uv run --env-file=.env main.py
   ```

3. **View results** in logs, `data_store/` directory, and `results/` directory for Parquet files

## Technologies Used

- **Python 3.13+**: Core language
- **rnet**: HTTP client with browser impersonation
- **Pydantic**: Data validation and serialization
- **loguru**: Advanced logging
- **tenacity**: Retry mechanisms
- **pandas**: Data manipulation (future analysis)

## Development Notes

- **Local Development**: The system uses cached JSON files during development to avoid hitting APIs repeatedly
- **Query Configuration**: Currently configured for men's shoes, size 10 (UK sizing)
- **Extensible Design**: Easy to extend for other product categories, sizes, or additional data sources
- **Responsible Scraping**: Tools like [Technical SEO robots.txt checker](https://technicalseo.com/tools/robots-txt/) were used to ensure responsible scraping practices

## Recent Changes

- **Added loader module (`loader.py`)**: Handles saving DataFrames to Parquet files for efficient storage and future analysis.
- **Improved transformation logic**: `transform.py` now includes request timestamps and enhanced DataFrame utilities.
- **General code tidying**: Improved error handling, logging, and modularity across the codebase.

## Future Enhancements

- Add support for multiple shoe sizes and categories
- Implement price comparison analytics
- Add database storage for historical price tracking
- Create web interface for results visualization
- Expand to multiple retailer sources
