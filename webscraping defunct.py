import asyncio
from requests_html import AsyncHTMLSession
import nest_asyncio
nest_asyncio.apply()

session = AsyncHTMLSession()

def only_chapters(link):
    stringified_link = str(link).lower()
    possible_chapters = ['ch_','ch-', 'ch.', 'chapter']
    is_chapter_link = False
    for word_fragment in possible_chapters:
        if word_fragment in stringified_link:
            is_chapter_link = True
            return is_chapter_link
        

async def getChaptersText():
    webpage = await session.get("https://mangadex.org/title/df361a38-eef6-4674-bec6-86d08aa1d1aa/ogami-tsumiki-to-kinichijou")
    print(webpage.html.text)
    await webpage.html.arender(sleep=10)
    print(webpage.html.text)
    all_links = webpage.html.absolute_links
    all_links = list(filter(only_chapters, all_links))
    print(all_links)
    print(len(all_links))
    

async def getNumOfChapters(website):
    try:
        webpage = await session.get(website)
    except:
        return 0
    
    all_links = webpage.html.absolute_links
    all_links = list(filter(only_chapters, all_links))
    total_link_num = len(all_links)
    if total_link_num == 0:
        await webpage.html.arender(sleep=10)
        all_links = webpage.html.absolute_links
        all_links = list(filter(only_chapters, all_links))
    
    return len(all_links)

#loop = asyncio.get_event_loop()
# run an asynchronous function until it returns a result
#result = loop.run_until_complete(getChaptersText())
#asyncio.run(getChaptersText())
#getChaptersText()
# close the event loop
#loop.close()
