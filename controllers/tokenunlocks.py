import asyncio
from playwright.async_api import async_playwright
import pandas as pd

async def extract_first_column(page):
    """Extracts Total Locked Tokens from page."""
    try:
        divs = await page.query_selector_all("body > div")
        unlock_progress_div = divs[4]

        if unlock_progress_div:
            p_elements = await unlock_progress_div.query_selector_all("p")
            if len(p_elements) >= 3:
                text = (await p_elements[3].inner_text()).strip()
                return text
            else:
                return "N/A"
        else:
            print("Fourth div not found.")
            return "N/A"
    except Exception as e:
        print(f"Error extracting first column: {e}")
        return "N/A"

async def extract_second_column(page):
    """Extracts Total Unlocked Tokens from page."""
    try:
        divs = await page.query_selector_all("body > div")
        unlock_progress_div = divs[4]

        if unlock_progress_div:
            p_elements = await unlock_progress_div.query_selector_all("p")
            if len(p_elements) >= 3:
                text = (await p_elements[6].inner_text()).strip()
                return text
            else:
                return "N/A"
        else:
            print("Fourth div not found.")
            return "N/A"
    except Exception as e:
        print(f"Error extracting first column: {e}")
        return "N/A"

async def extract_third_column(page):
    """Extracts Total Untracked Tokens from page."""
    try:
        divs = await page.query_selector_all("body > div")
        unlock_progress_div = divs[4]

        if unlock_progress_div:
            p_elements = await unlock_progress_div.query_selector_all("p")
            if len(p_elements) >= 3:
                text = (await p_elements[9].inner_text()).strip()
                return text
            else:
                return "N/A"
        else:
            print("Fourth div not found.")
            return "N/A"
    except Exception as e:
        print(f"Error extracting first column: {e}")
        return "N/A"

async def extract_fourth_column(page):
    return "N/A"

async def capture_data(page, url_slug: str):
    first_column = await extract_first_column(page)
    second_column = await extract_second_column(page)
    third_column = await extract_third_column(page)

    row_data = {
        "name": url_slug,
        "locked": first_column,
        "unlocked": second_column,
        "untracked": third_column
    }

    return row_data

async def get_page_data(page, url_slug: str) -> pd.DataFrame:
    base_url = "https://token.unlocks.app/"
    url = f"{base_url}{url_slug}"
    await page.goto(url)
    await asyncio.sleep(5)
    row_data = await capture_data(page, url_slug)
    df = pd.DataFrame([row_data])
    return df

async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        url_slugs = ["balancer", "pendle", "worldcoin-wld"]
        page = await browser.new_page()
        page.goto("https://token.unlocks.app/")
        await asyncio.sleep(10) # wait for login credentials
        all_dfs = []

        for slug in url_slugs:
            url = f"https://token.unlocks.app/{slug}"
            print(f"Fetching data from: {url}")
            await page.goto(url)
            df = await get_page_data(page, slug)
            all_dfs.append(df)

        await browser.close()
        final_df = pd.concat(all_dfs, ignore_index=True)
        print(final_df)

if __name__ == "__main__":
    asyncio.run(main())