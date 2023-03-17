import os
from typing import List
from datetime import datetime
import requests

import openai
import asyncio
from bs4 import BeautifulSoup
import telegram
from dotenv import load_dotenv


load_dotenv()


OPEN_API_KEY = os.getenv('OPEN_API_KEY')

BASE_URL = 'https://www.ptt.cc'
URL = f'{BASE_URL}/bbs/Gossiping/index.html'
COOKIE = {'over18': '1'}
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

NOW_DT = datetime.now()
PUSH_THRESHOLD = 50


def is_post_date_valid(post_date: str) -> bool:
    now_dt = NOW_DT.strftime('%m/%d').lstrip('0')
    return post_date == now_dt


def get_article_ds(url: str = URL) -> List[dict]:    
    ptt_article_ds = []
    
    page_count = 1
    to_continue = True
    while to_continue:
        res = requests.get(url, headers=HEADERS, cookies=COOKIE)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        articles = soup.select('div.r-ent')
        for article in articles:
            post_date = article.select_one('div.date').text.strip()
            if not is_post_date_valid(post_date):
                
                # skip some pinned article in first page
                to_continue = False if page_count != 1 else True
                continue
            
            try:
                push_count_text = article.select_one('div.nrec span.hl').text
                push_count = int(push_count_text)
            except (AttributeError, ValueError):
                if push_count_text == '爆':
                    push_count = 100
                else:
                    push_count = -1
                
            if push_count <= PUSH_THRESHOLD:
                continue

            title = article.select_one('div.title a')
            article_title = title.text
            ptt_article_ds.append(
                dict(
                    title=article_title,
                    url=BASE_URL + title['href'],
                    push_count=push_count,
                    post_date=post_date
                )
            )

        next_page_button = soup.select_one('div.btn-group-paging a:nth-of-type(2)')
        if not next_page_button:
            break
        url = BASE_URL + next_page_button['href']
        page_count += 1
    
    return ptt_article_ds


async def send_to_telegram(article_ds: List[dict]):
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    for article_d in article_ds:
        message = f'標題: {article_d["title"]}\n\n總結: {article_d["summary"]}\n\n推文: {article_d["push_count"]}\n\n連結: {article_d["url"]}'
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)


def get_summary(content: str) -> str:
    openai.api_key = OPEN_API_KEY
    summary = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f'請用 50 個中文字總結以下段落: {content[:500]}',
        max_tokens=128
    ).choices[0].text.strip()
    return summary


def get_summarized_article_ds(article_ds: List[dict]) -> List[dict]:
    summarized_article_ds = []

    for article_d in article_ds:
        if not (article_url := article_d.get('url')):
            continue
        
        article_response = requests.get(article_url, cookies=COOKIE)
        
        article_soup = BeautifulSoup(article_response.text, 'html.parser')
        content = article_soup.find('div', {'id': 'main-content'}).text.strip()
        
        article_d['summary'] = get_summary(content)
        summarized_article_ds.append(article_d)
    
    return summarized_article_ds


def run():
    article_ds_from_gossip = get_article_ds()
    print(f'Total article count: {len(article_ds_from_gossip)}')
    if article_ds_from_gossip:
        summarized_article_ds = get_summarized_article_ds(article_ds_from_gossip)
        asyncio.run(send_to_telegram(summarized_article_ds))


if __name__ == '__main__':
    print(f'Post time is {NOW_DT}')
    run()
