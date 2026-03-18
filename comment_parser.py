#解析评论DOM
#提取用户名
#提取评论内容
def parse_comments(page, max_comments):

    comments = page.locator(".qqcom-comment-item")
    count = comments.count()

    results = []

    for i in range(min(count, max_comments)):
        comment = comments.nth(i)

        try:
            name = comment.locator(".qnc-comment__nickname").inner_text()
            content = comment.locator(".qnc-comment__content").first.inner_text().strip()

            results.append((name, content))

        except:
            continue

    return results