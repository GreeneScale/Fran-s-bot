from playwright.async_api import async_playwright

def only_chapters(link):
    stringified_link = str(link).lower()
    possible_chapters = ['ch_','ch-', 'ch.', 'chapter']
    is_chapter_link = False
    for word_fragment in possible_chapters:
        if word_fragment in stringified_link:
            is_chapter_link = True
            return is_chapter_link
        

async def getChaptersText():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://mangadex.org/title/df361a38-eef6-4674-bec6-86d08aa1d1aa/ogami-tsumiki-to-kinichijou")
        await page.wait_for_timeout(5000)
        all_link_locators = await page.get_by_role('link').all()
        for li in all_link_locators:
            print(await li.get_attribute('href'))
        await browser.close()

async def getWebsiteChapterNums(allwebsites):
    websitesWithChapterNums = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        for website in allwebsites:
            await page.goto(website)
            await page.wait_for_timeout(5000)
            all_link_locators = await page.get_by_role('link').all()
            list_of_links = []
            for loc in all_link_locators:
                list_of_links.append(await loc.get_attribute('href'))
            list_of_links = list(filter(only_chapters, list_of_links))
            print(list_of_links)
            websitesWithChapterNums[website] = len(list_of_links)
        await browser.close()
        return websitesWithChapterNums



    

# async def getNumOfChapters(website):
#     try:
#         webpage = await session.get(website)
#     except:
#         return 0
    
#     all_links = webpage.html.absolute_links
#     all_links = list(filter(only_chapters, all_links))
#     total_link_num = len(all_links)
#     if total_link_num == 0:
#         await webpage.html.arender(sleep=10)
#         all_links = webpage.html.absolute_links
#         all_links = list(filter(only_chapters, all_links))
    
#     return len(all_links)

#loop = asyncio.get_event_loop()
# run an asynchronous function until it returns a result
#result = loop.run_until_complete(getChaptersText())
#asyncio.run(getChaptersText())
#getChaptersText()
# close the event loop
#loop.close()
