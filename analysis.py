import csv
import os
from collections import Counter

import jieba
from snownlp import SnowNLP
from wordcloud import WordCloud
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS'] #支持中文
plt.rcParams['axes.unicode_minus'] = False #负号正常显示

DATA_PATH = "data/comments.csv"
RESULT_DIR = "results"

os.makedirs(RESULT_DIR, exist_ok=True)


def load_comments():
    comments = []

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            if len(row) >= 3:
                comments.append(row[2])

    return comments


# -------------------------
# 情感分析
# -------------------------
def sentiment_analysis(comments):

    scores = []

    for text in comments:
        try:
            s = SnowNLP(text)
            scores.append(s.sentiments)
        except:
            scores.append(0.5)

    positive = sum(1 for s in scores if s > 0.6)
    neutral = sum(1 for s in scores if 0.4 <= s <= 0.6)
    negative = sum(1 for s in scores if s < 0.4)

    print("情感统计：")
    print("正面:", positive)
    print("中性:", neutral)
    print("负面:", negative)

    # 画图
    plt.figure()
    plt.pie(
        [positive, neutral, negative],
        labels=["正面", "中性", "负面"],
        autopct="%1.1f%%",
        colors = ["#66c2a5", "#ffd92f", "#fc8d62"]
    )
    plt.title("情感分析")
    plt.savefig(os.path.join(RESULT_DIR, "sentiment.png"))
    plt.close()


# -------------------------
# 高频词统计
# -------------------------
def word_frequency(comments):

    words = []

    for text in comments:
        seg = jieba.lcut(text)

        for w in seg:
            if len(w) > 1:
                words.append(w)

    counter = Counter(words)

    top_words = counter.most_common(20)

    print("\n高频词：")
    for w, c in top_words:
        print(w, c)

    with open(os.path.join(RESULT_DIR, "top_words.txt"), "w", encoding="utf-8") as f:
        for w, c in top_words:
            f.write(f"{w}: {c}\n")

    return words


# -------------------------
# 词云
# -------------------------
def generate_wordcloud(words):

    text = " ".join(words)

    wc = WordCloud(
        font_path="/System/Library/Fonts/STHeiti Medium.ttc",  # Mac用这个
        width=800,
        height=400,
        background_color="white"
    )

    wc.generate(text)

    plt.figure()
    plt.imshow(wc)
    plt.axis("off")

    plt.savefig(os.path.join(RESULT_DIR, "wordcloud.png"))
    plt.close()


def main():

    comments = load_comments()

    print("总评论数:", len(comments))

    sentiment_analysis(comments)

    words = word_frequency(comments)

    generate_wordcloud(words)

    print("\n分析完成！结果在 results 文件夹")


if __name__ == "__main__":
    main()