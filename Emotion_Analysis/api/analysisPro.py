import konlpy
from collections import Counter

import matplotlib
from konlpy.tag import Okt, Twitter, Kkma
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import pytagcloud
import seaborn as sns
import pandas as pd
import numpy as np
from math import pi
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
from threading import Thread
import pygame
pygame.init()

matplotlib.use('Agg')


# api/static/wordcloud.jpg
# 감정사전 불러오기


def load_emolex(emolex):
    emolex_df = pd.read_excel(emolex)
    return emolex_df


# 감정 사전에서 감정 간의 상관관계


def corr_emotion(emolex_df, dir):
    f, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(emolex_df.corr(), annot=True, linewidths=0.6, fmt=".4f", ax=ax)
    plt.savefig(dir, dpi=100, facecolor=("#EAEAE3"), transparent=True, bbox_inches='tight')
    plt.close()


# 게시글 하나 불러와서 형태소 분석


def load_content(board):
    target = board.contents
    okt = Okt()
    nouns = okt.nouns(target)
    return nouns


def group_content(contents):
    okt = Okt()
    nouns_list = []
    for data in contents:
        nouns = okt.nouns(data)
        for noun in nouns:
            nouns_list.append(noun)
    return nouns_list


# 형태소 분석한 결과 가져와서 워드 클라우드 생성

def wordcloud(nouns, root, number):
    count = Counter(nouns)
    tag = count.most_common(30)
    taglist = pytagcloud.make_tags(tag)
    save = root + "wordcloud" + str(number) + ".png"
    pytagcloud.create_tag_image(taglist, save,
                                size=(300, 200), background=(234, 234, 227, 255), fontname='Korean', rectangular=False)


# 감정사전의 단어와 분석할 대상의 명사가 같은 것들을 뽑아 데이터프레임 생성


def emo_dataframe(nouns, emolex_df):
    analysis_df = emolex_df[emolex_df["Korean (ko)"].isin(nouns)]
    # 감정별로 합산
    emotion_sum = analysis_df[
        ["Positive", "Negative", "Anger", "Anticipation", "Disgust", "Fear", "Joy", "Sadness", "Surprise",
         "Trust"]].sum()
    return emotion_sum


def emo_board(nouns, emolex_df):
    analysis_df = emolex_df[emolex_df["Korean (ko)"].isin(nouns)]
    emotion_sum = analysis_df[["Anger", "Anticipation", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust"]].sum()
    emotion = emotion_sum.idxmax()
    return emotion


# 감정분석 결과 바 그래프


def bar_graph(emotion_sum, root, number):
    x = ["Positive", "Negative", "Anger", "Anticipation",
         "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust"]
    plt.barh(x, emotion_sum, color='blue')
    plt.xlim(0, emotion_sum.sum(axis=0))
    plt.savefig(root + "bar" + str(number) + ".png", dpi=100, facecolor=("#EAEAE3"), transparent=True,
                bbox_inches='tight')
    plt.close()


# 선그래프


def line_graph(emotion_sum, root, number):
    x = ["Positive", "Negative", "Anger", "Anticipation",
         "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust"]
    plt.plot(x, emotion_sum)
    plt.savefig(root + "line" + str(number) + ".png", dpi=100, facecolor=("#EAEAE3"), transparent=True,
                bbox_inches='tight')
    plt.close()


# 파이그래프


def pie_graph(emotion_sum, root, number):
    x = ["Positive", "Negative", "Anger", "Anticipation",
         "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust"]
    plt.pie(emotion_sum, labels=x, autopct='%.1f%%')
    plt.savefig(root + "pie" + str(number) + ".png", dpi=100, facecolor=("#EAEAE3"), transparent=True,
                bbox_inches='tight')
    plt.close()


# 레이더 그래프


def raider_graph(emotion_sum, root, number):
    # plotThread = Thread(target=raider_graph)
    # plotThread.daemon = True
    # plotThread.start()
    result_df = pd.DataFrame(emotion_sum).T
    labels = result_df.columns[0:]
    num_labels = len(labels)
    angles = [x / float(num_labels) * (2 * pi) for x in range(num_labels)]
    angles += angles[:1]
    my_palette = plt.cm.get_cmap("Set2", len(result_df.index))
    fig = plt.figure(figsize=(20, 20))
    fig.set_facecolor("#EAEAE3")
    for i, row in result_df.iterrows():
        color = my_palette(i)
        data = result_df.iloc[i].tolist()
        data += data[:1]

        ax = plt.subplot(3, 2, i + 1, polar=True)
        ax.set_theta_offset(pi / 2)  # 시작점
        ax.set_theta_direction(-1)  # 그려지는 방향 시계방향

        plt.xticks(angles[:-1], labels, fontsize=13)  # x축 눈금 라벨
        ax.tick_params(axis='x', which='major', pad=15)  # x축과 눈금 사이에 여백을 준다.

        ax.set_rlabel_position(0)  # y축 각도 설정(degree 단위)
        index = []
        counter = emotion_sum.sum(axis=0)
        print("rader",emotion_sum.sum(axis=0))
        for i in range(0,emotion_sum.sum(axis=0)):
            index.append(i*5)
        plt.yticks(index,fontsize=10)  # y축 눈금 설정
        # plt.ylim(0, emotion_sum.sum(axis=0))

        ax.plot(angles, data, color=color, linewidth=2,
                linestyle='solid')  # 레이더 차트 출력
        ax.fill(angles, data, color=color, alpha=0.4)  # 도형 안쪽에 색을 채워준다.

        # 타이틀은 캐릭터 클래스로 한다.
        plt.title('test', size=20, color=color, x=-0.2, y=1.2, ha='left')

    plt.tight_layout(pad=5)  # subplot간 패딩 조절
    plt.savefig(root + "raider" + str(number) + ".png", dpi=100, facecolor=("#EAEAE3"), transparent=True,
                bbox_inches='tight')
    plt.close()
    # plotThread.join()

    # 게시글 하나 분석


def analysisOneContent(board, emolex, root):
    # 게시글 호출, 형태소 분석
    nouns = load_content(board)
    # 워드클라우드 생성
    wordcloud(nouns, root, board)
    # 감정사전 호출
    emolex_df = load_emolex(emolex)
    # 감정사전으로 분석
    emotion_sum = emo_dataframe(nouns, emolex_df)
    # 바 그래프
    bar_graph(emotion_sum, root, board)
    # 파이 그래프
    pie_graph(emotion_sum, root, board)
    # 선그래프
    line_graph(emotion_sum, root, board)
    # 레이더 그래프
    raider_graph(emotion_sum, root, board)
