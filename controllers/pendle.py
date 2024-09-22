import asyncio
from playwright.async_api import async_playwright
import pandas as pd

# Function to extract the first column's data (first <td> child in the row)
async def extract_first_column(row):
    try:
        tds = await row.query_selector_all('td')
        content_div = await tds[0].query_selector_all('div')
        if content_div and len(content_div) > 5:
            text = (await content_div[4].inner_text()).strip()
            return text
        return "N/A"
    except Exception as e:
        return "N/A"

# Function to extract the second column's data - Placeholder (returning "N/A")
async def extract_second_column(row):
    try:
        tds = await row.query_selector_all('td')
        content_div = await tds[1].query_selector_all('span')
        if content_div:
            text = (await content_div[0].inner_text()).strip()
            return text
        return "N/A"
    except Exception as e:
        return "N/A"

# Function to extract the third column's data - Placeholder (returning "N/A")
async def extract_third_column(row):
    try:
        tds = await row.query_selector_all('td')
        content_div = await tds[2].query_selector_all('span')
        if content_div:
            text = (await content_div[0].inner_text()).strip()
            return text
        return "N/A"
    except Exception as e:
        return "N/A"


# Function to extract the fourth column's data - Placeholder (returning "N/A")
async def extract_fourth_column(row):
    try:
        tds = await row.query_selector_all('td')
        content_div = await tds[4].query_selector_all('span')
        if content_div:
            text = (await content_div[1].inner_text()).strip()
            return f'{text}%'
        return "N/A"
    except Exception as e:
        return "N/A"

# Function to capture all rows (<tr> elements) and process each column
async def capture_rows(page, debug=True):
    """
    Asynchronously captures rows from a table on a web page.
    Args:
        page (Page): The web page object to interact with.
        debug (bool, optional): If True, limits the number of rows captured to 10 for debugging purposes. Defaults to True.
    Returns:
        list: A list of dictionaries, each containing data from a row in the table. The dictionary keys are:
            - "ticker": The value from the first column.
            - "close": The value from the second column.
            - "liquidity": The value from the third column.
            - "apy": The value from the fourth column.
    """
    # Wait for the table to appear
    await page.wait_for_selector("table.pp-table", timeout=10000)

    # Get all the <tr> elements inside the table
    table_rows = await page.query_selector_all("tr")

    data = []
    count = 0
    for row in table_rows:
        cells = {}
        if count > 10 and debug:
            break
        # Extract the first column
        cells["ticker"] = await extract_first_column(row)

        # For now, return "N/A" for the other columns
        cells["close"] = await extract_second_column(row)
        cells["liquidity"] = await extract_third_column(row)
        cells["apy"] = await extract_fourth_column(row)
        
        if cells:
            data.append(cells)
        count += 1
    return data

# Main function to gather data from the table
async def get_table_data(page, url: str, debug=True) -> pd.DataFrame:
    """
    Fetches table data from a specified URL and returns it as a pandas DataFrame.

    Args:
        page: The browser page object to interact with.
        url (str): The URL of the webpage to navigate to.
        debug (bool, optional): If True, enables debug mode. Defaults to True.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted table data with columns ["ticker", "close", "liquidity", "apy"].

    Raises:
        Exception: If there is an issue with navigating to the URL or extracting the data.
    """
    # Navigate to the webpage
    await page.goto(url)

    # Wait for 5 seconds to allow the content to load
    await asyncio.sleep(5)

    target_text = "Show All"
    button = await page.query_selector(f'button:has-text("{target_text}")')
    await button.click()

    # Capture rows and process columns
    all_data = await capture_rows(page, debug=debug)
    # Create a pandas DataFrame from the extracted data
    df = pd.DataFrame(all_data, columns=["ticker", "close", "liquidity", "apy"])
    return df

# Function to run the scraper with asyncio and async_playwright
async def main():
    async with async_playwright() as p:
        # Start Playwright and launch the browser
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()

        # URL of the page
        url = "https://app.pendle.finance/trade/markets"

        # Call the function with the page object
        df = await get_table_data(page, url, debug=True)
        
        # Close the browser
        await browser.close()

        print(df.head())

if __name__ == "__main__":
    asyncio.run(main())
