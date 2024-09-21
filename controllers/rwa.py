import time
import pandas as pd
import asyncio
import re
from playwright.async_api import Page, async_playwright

async def clean_column_value(value: str) -> float:
    """Clean the string by removing newlines, arrows, dollar signs, and extra characters, then convert to float."""
    # Remove newlines, arrows, dollar signs, and commas
    cleaned_value = re.sub(r'[\n▲▼$]', '', value).strip()
    cleaned_value = cleaned_value.replace(',', '')
    
    # Convert the cleaned string to a float (or return None if conversion fails)
    try:
        return float(cleaned_value)
    except ValueError:
        return None  # Return None if the conversion to float fails

async def get_mc_table_data(page: Page, url: str) -> pd.DataFrame:
    # Start Playwright and launch the browser
    
    # Navigate to the webpage
    await page.goto(url)
    await asyncio.sleep(5)  # Wait for 5 seconds (increase or decrease based on your needs)

    table_selector = "table:nth-of-type(1)"
    # Option 2: Wait for the second table to appear (more dynamic approach)
    await page.wait_for_selector(table_selector, timeout=50000)  # Wait up to 10 seconds for the table

    # Extract rows of the second table
    table_rows = await page.query_selector_all(f'{table_selector} tr')
    
    # Store the data from the second and fourth columns
    data = []
    for row in table_rows[1:]:  # Skip the header
        cells = await row.query_selector_all("td")
        if len(cells) >= 4:  # Ensure that the row has at least 4 columns
            second_column = (await cells[1].inner_text()).strip()  # Clean the second column if needed
            fourth_column = (await cells[3].inner_text()).strip()
            cleaned_fourth_column = await clean_column_value(fourth_column)
            if cleaned_fourth_column is None or '%' in fourth_column:
                continue
            data.append([second_column, cleaned_fourth_column])
    
    return pd.DataFrame(data, columns=["ticker", "mc"])

async def main():
    async with async_playwright() as p:
        # Start Playwright and launch the browser
        browser = await p.firefox.launch(headless=False)
        
        # Create a new page (browser tab)
        page = await browser.new_page()

        # URL of the page
        url = "https://app.rwa.xyz/stablecoins"

        # Call the function with the page object
        df = await get_mc_table_data(page, url)

        # Print the dataframe
        print(df)

        # Close the browser
        await browser.close()

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())