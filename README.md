# DeFi Analytics Web Scraping

This project is focused on web scraping data from various dynamic websites using Python and Playwright. The extracted data is processed and saved in a structured format using Pandas, and Jupyter Notebooks are used to run and analyze the scraped data.

## Project Description

This project scrapes data from various websites, capturing specific elements and content. The scraping logic is built using Playwright with asynchronous execution for better performance. The data is processed into a structured format using Pandas DataFrames and further analyzed within Jupyter Notebooks.

## Requirements

- Python 3.7+
- [Poetry](https://python-poetry.org/) (for dependency management)
- [Playwright](https://playwright.dev/python/docs/intro)
- [Pandas](https://pandas.pydata.org/)
- [Jupyter](https://jupyter.org/)

## Installation

1. After cloning the repo, install dependencies using Poetry.

Poetry is used for managing dependencies. To install the project dependencies, run the following commands:

   ```bash
   poetry install
   ```

2. Set up Playwright.

Playwright needs to install browser binaries. Run the following command to install them:


    ```bash
    poetry run playwright install
    ```

## Running Jupyter notebooks

Jupyter should be installed in the poetry dependencies. To run a jupyter lab and manipulate data using notebooks,
run `jupyter notebook`.

## License

WTFPL. This is just browser automation do so what you want.