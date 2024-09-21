import time
import pandas as pd
import asyncio
import re
from playwright.async_api import Page, async_playwright

# Function to extract the first column's data ("ticket")
async def extract_first_column(row):
    try:
        # First, get the top-level div for the first column
        link = await row.query_selector_all('a') 
        if len(link) >= 2: 
            token_span = await link[1].query_selector('span')
            data = await token_span.inner_html()
            return data
    except Exception:
        return "N/A"

# Function to extract the second column's data ("platform") - Placeholder
async def extract_second_column(row):
        try:
            # First, get the top-level div for the first column
            link = await row.query_selector_all('a') 
            data = await link[2].inner_html()
            return data
        except Exception:
            return "N/A"

# Function to extract the third column's data ("chain") - Placeholder
async def extract_third_column(row):
            try:
                # First, get the top-level div for the first column
                link = await row.query_selector_all('a') 
                data = await link[3].get_attribute('href')
                return data.split('=')[-1]
            except Exception:
                return "N/A"

# Function to extract the fourth column's data ("TVL") - Placeholder
async def extract_fourth_column(row):
    try:
        col = await row.query_selector('> div:nth-child(3)')
        token_span = await col.query_selector('span')
        data = await token_span.inner_html()
        return data
    except Exception:
        return "N/A"
    
# Function to extract the fourth column's data ("APY") - Placeholder
async def extract_fifth_column(row):
    try:
        col = await row.query_selector('> div:nth-child(4)')
        token_span = await col.query_selector('span')
        data = await token_span.inner_text()
        return data
    except Exception:
        return "N/A"


async def capture_rows(page, captured_rows):
    # Find the third direct child div of #table-wrapper (the table contents)
    table_wrapper = await page.query_selector("#table-wrapper")
    table_content = await table_wrapper.query_selector("> div:nth-child(3)")  # Use direct child selector

    # Get all the rows (div elements representing rows inside the table content)
    table_rows = await table_content.query_selector_all("> div")

    # Store the data from the first five columns
    data = []
    
    for row in table_rows:
        row_key = await row.evaluate("(el) => el.innerText")  # Get a unique identifier for the row (e.g., innerText)
        if row_key not in captured_rows:  # Avoid duplicates
            cells = {}
            
            # Extract data for the first column
            cells["ticker"] = await extract_first_column(row)

            # Placeholder for the remaining columns (platform, chain, TVL)
            cells["platform"] = await extract_second_column(row)
            cells["chain"] = await extract_third_column(row)
            cells["tvl"] = await extract_fourth_column(row)
            cells["apy"] = await extract_fifth_column(row)

            if cells:
                data.append(cells)
                captured_rows.add(row_key)  # Track the row to avoid capturing it again
    
    return data

async def scroll_and_capture(page, scroll_limit=2):
    captured_rows = set()  # Store unique rows
    all_data = []

    for _ in range(scroll_limit):  # Set a scroll limit to avoid infinite loops
        # Capture the current visible rows
        data = await capture_rows(page, captured_rows)
        all_data.extend(data)
        
        # Scroll down the page
        await page.evaluate("window.scrollBy(0, window.innerHeight)")
        await asyncio.sleep(2)  # Wait for new rows to load

        # Check if we are still loading new rows (stop if no new rows are found)
        if not data:
            break

    return all_data

# Main function to gather data from the table
async def get_table_data(page, url: str, debug=False) -> pd.DataFrame:
    # Navigate to the webpage
    await page.goto(url)

    # Wait for 5 seconds to allow the content to load
    await asyncio.sleep(5)

    scroll_limit = 2 if debug else 20
    # Scroll and capture rows
    all_data = await scroll_and_capture(page, scroll_limit=scroll_limit)

    # Create a pandas DataFrame from the extracted data
    df = pd.DataFrame(all_data, columns=["ticker", "platform", "chain", "tvl", "apy"])

    return df


# Function to run the scraper with asyncio and async_playwright
async def main():
    async with async_playwright() as p:
        # Start Playwright and launch the browser
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()

        # URL of the page
        url = "https://defillama.com/yields?token=DAI&token=USDC&token=USDT&token=FRAX&token=GHO&token=OHM&chain=Ethereum&chain=Arbitrum&category=Lending&category=Algo-Stables"

        # Call the function with the page object
        df = await get_table_data(page, url, debug=True)

        print(df.head())
        # Close the browser
        await browser.close()

        return df

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())