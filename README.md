# MSRP - Modular Shoe Price Scraper

A modular web scraping solution designed to collect and analyze price data for size 10 men's shoes from manufacturer websites. This project was developed as an evolution of a previous internship project, with a focus on clean architecture, modularity, and separation of concerns.

## Project Overview

This scraper system is specifically designed to:

- Extract shoe product data and prices for men's size 10 shoes
- Compare prices across different sources
- Provide a modular, extensible architecture for future enhancements
- Minimize API calls during development through local caching

## Architecture

The project follows a modular design pattern with three main components:

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
  - `SearchItem` model for individual shoe products (productId, displayName, division, price)
  - `SearchResults` model for search result collections
  - Clean conversion from raw JSON to structured Python objects

### 3. Orchestration Layer (`main.py`)

- **Purpose**: Coordinates the workflow and business logic
- **Features**:
  - Environment variable configuration for API endpoints
  - Query preparation for men's size 10 shoes
  - Integration between extraction and transformation layers
  - Comprehensive logging with `loguru`

## Key Features

- **Modular Design**: Each component can be developed, tested, and maintained independently
- **Browser Impersonation**: Uses `rnet` with Chrome 137 impersonation for realistic requests
- **Robust Error Handling**: Retry mechanisms and comprehensive error logging
- **Development-Friendly**: Local caching prevents hitting APIs repeatedly during testing
- **Type Safety**: Pydantic models ensure data integrity and validation
- **Async Support**: Concurrent processing capabilities for better performance

## Project Structure

```text
msrp/
├── main.py              # Main orchestration script
├── extract.py           # Data extraction module
├── transform.py         # Data transformation and models
├── data_store/          # Local data storage
│   ├── search_res.json  # Cached search results
│   ├── products_ex.json # Product examples
│   └── *.csv           # Processed data files
├── exploratory_analysis.ipynb  # Data analysis notebook
├── pyproject.toml       # Project dependencies
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
   python main.py
   ```

3. **View results** in logs and `data_store/` directory

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

## Future Enhancements

- Add support for multiple shoe sizes and categories
- Implement price comparison analytics
- Add database storage for historical price tracking
- Create web interface for results visualization
- Expand to multiple retailer sources
