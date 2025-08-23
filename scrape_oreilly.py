import asyncio
from playwright.async_api import async_playwright
import csv


async def scrape_oreilly():
    url = "https://www.oreilly.com/search/skills/?rows=100"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)

        # Close cookie banner
        try:
            await page.wait_for_selector('button.onetrust-close-btn-handler', timeout=5000)
            await page.click('button.onetrust-close-btn-handler')
        except:
            pass

        # Hide or remove potential overlay interceptors (like chat messenger iframe)
        await page.evaluate("""
            const overlays = document.querySelectorAll("#q-messenger-frame, iframe[src*='qualified.com']");
            overlays.forEach(el => el.style.display = 'none');
        """)

        fieldnames = ['title', 'category', 'author', 'page_count_or_duration', 'publisher']
        with open('oreilly_full_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            page_num = 1
            while True:
                print(f"Scraping page {page_num}...")
                await page.wait_for_selector("article", timeout=10000)
                articles = await page.query_selector_all("article")

                for article in articles:
                    # Title
                    title = await article.eval_on_selector("[data-testid^='title-link-'] a", 'el => el.innerText') \
                        if await article.query_selector("[data-testid^='title-link-'] a") else ''
                    # Category
                    category_raw = await article.eval_on_selector(
                        "strong[data-testid^='format-label-']", 'el => el.innerText'
                    ) if await article.query_selector("strong[data-testid^='format-label-']") else ''
                    category = category_raw.replace('Format:', '').strip().replace('\n', '').replace('\r', '')

                    # Author
                    author = await article.eval_on_selector(
                        "div[data-testid^='search-card-authors-']", 'el => el.innerText'
                    ) if await article.query_selector("div[data-testid^='search-card-authors-']") else ''
                    author = author.strip().replace('\n', ', ').replace('\r', '')

                    # Page count or duration
                    meta_content = await article.query_selector("[data-testid^='search-card-meta-content-']")
                    page_count = ''
                    publisher = ''
                    if meta_content:
                        page_count_span = await meta_content.query_selector("span.css-1ok1nmx")
                        if page_count_span:
                            page_count = await page_count_span.inner_text()
                        publisher_a = await meta_content.query_selector("a")
                        if publisher_a:
                            publisher = await publisher_a.inner_text()

                    if title and category:
                        row = {
                            'title': title,
                            'category': category,
                            'author': author,
                            'page_count_or_duration': page_count,
                            'publisher': publisher
                        }
                        writer.writerow(row)
                        print(f"{title} | {category} | {author} | {page_count} | {publisher}")

                # Pagination handling
                next_arrow = await page.query_selector("button svg path[d='M12 8L0 0V16L12 8Z']")
                if next_arrow:
                    next_button = await next_arrow.evaluate_handle('el => el.closest("button")')

                    if next_button:
                        first_title = ""
                        if articles:
                            first_title = await articles[0].eval_on_selector(
                                "[data-testid^='title-link-'] a", 'el => el.innerText'
                            ) if await articles[0].query_selector("[data-testid^='title-link-'] a") else ''

                        try:
                            # Ensure button is visible in viewport
                            await next_button.scroll_into_view_if_needed()
                            # Try normal click
                            await next_button.click(timeout=5000)
                        except:
                            # Fall back to JS click if intercepted
                            await page.evaluate("(btn) => btn.click()", next_button)

                        # Wait for next page to load (detect change in first title)
                        for _ in range(20):
                            await page.wait_for_timeout(500)
                            new_articles = await page.query_selector_all("article")
                            if new_articles:
                                new_first_title = await new_articles[0].eval_on_selector(
                                    "[data-testid^='title-link-'] a", 'el => el.innerText'
                                ) if await new_articles[0].query_selector("[data-testid^='title-link-'] a") else ''
                                if new_first_title != first_title:
                                    break

                        page_num += 1
                    else:
                        break
                else:
                    break

        await browser.close()


if __name__ == "__main__":
    asyncio.run(scrape_oreilly())
