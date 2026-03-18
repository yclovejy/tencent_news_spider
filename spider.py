import requests
import csv
from playwright.sync_api import sync_playwright

from config import HOT_URL, NEWS_COUNT, MAX_COMMENTS
from comment_parser import parse_comments
from utils import random_sleep

def get_hot_news():
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(HOT_URL, headers=headers)
    data = response.json()

    return data["data"][:NEWS_COUNT]

def crawl():
    hot_list = get_hot_news()
    print("\n=========今日热点新闻=========")
    for i, news in enumerate(hot_list):
        print(f"{i+1}. {news['title']}")
    print("==================================\n")

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        )
        page = context.new_page()
        with open("data/comments.csv", "w", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)
            writer.writerow(["新闻标题", "用户名", "评论"])

            for index, news in enumerate(hot_list):

                title = news["title"]
                url = news["url"]

                print("\n==================")
                print(f"第{index+1}条新闻")
                print(title)

                try:
                    page.goto(url, wait_until="commit", timeout=60000)
                    page.wait_for_timeout(2000)
                except Exception as e:
                    print("页面加载失败:", e)
                    continue

                random_sleep(3,5)

                print("实际页面:", page.url)

                try:
                    btn = page.locator("text=查看更多评论")

                    if btn.count() > 0:
                        btn.first.click()
                        print("已点击查看更多评论")
                        random_sleep(3,4)
                    else:
                        btn = page.locator("text=查看全部")
                        if btn.count() > 0:
                            btn.first.click()
                            print("已点击查看全部")
                            random_sleep(3,4)
                        else:
                            print("没有找到评论按钮")

                except Exception as e:
                    print(f"点击评论按钮失败: {e}")

                print("滚动加载评论...")

                max_click = 20
                click_count = 0

                while click_count < max_click:

                    # 如果已经加载完评论
                    if page.locator("text=已显示所有评论").count() > 0:
                        print("评论已全部加载")
                        break

                    # 如果已经达到目标评论数
                    current_count = page.locator(".qqcom-comment-item").count()

                    if current_count >= MAX_COMMENTS:
                        print("达到目标评论数量")
                        break

                    try:

                        page.mouse.wheel(0, 3000)
                        page.wait_for_timeout(600)

                        more_btn = page.locator("text=查看更多评论")

                        if more_btn.count() > 0 and more_btn.first.is_visible():
                            more_btn.first.click()
                            print(f"点击查看更多评论 {click_count + 1}")
                            page.wait_for_timeout(1200)
                            click_count += 1
                            continue

                        more_btn = page.locator("text=查看全部")

                        if more_btn.count() > 0 and more_btn.first.is_visible():
                            more_btn.first.click()
                            print(f"点击查看全部 {click_count + 1}")
                            page.wait_for_timeout(1200)
                            click_count += 1
                            continue

                    except Exception as e:
                        print("加载评论异常:", e)
                        break

                try:
                    page.locator(".qqcom-comment-item").first.wait_for(timeout=10000)
                except:
                    print("没有评论")
                    continue

                comments = parse_comments(page, MAX_COMMENTS)

                print("抓取评论:", len(comments))

                for name, content in comments:
                    print(name, ":", content)
                    writer.writerow([title, name, content])

        browser.close()