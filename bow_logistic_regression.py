#!/usr/bin/env python
# -*- coding:utf-8 -*-

from natsume_loader import token_generator
from gensim import corpora, matutils
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

doc_list = [
    list(token_generator('みずほ銀行が10月上旬にもワシントンに駐在員事務所を開設することが13日、明らかになった。融資業務に影響を与えるトランプ政権の金融規制改革や北米自由貿易協定（NAFTA）再交渉などの情報を収集するのが狙い。同行が米首都に拠点を置くのは初めて')),
    list(token_generator('パナソニックは13日、国内で販売した液晶テレビ計約11万台について、テレビ本体が転倒する恐れがあるとしてリコール（無料点検・部品交換）を行うと発表した。子どもの体に当たる事故があった1件を含め、転倒などに伴い計12件の修理を既に実施。けが人はいないという。')),
    list(token_generator('３日目に立ち合いのミスで自滅した横綱・日馬富士は、東前頭２枚目・北勝富士に不覚を取り、連敗で通算３７個目の金星を配給した。')),
    list(token_generator('日本ハム・大谷翔平投手（２３）が今オフ、右足かかと部分にある「三角骨骨棘（こっきょく）」の除去手術を受ける見込みとなっていることが１３日、分かった。昨秋から悩まされていた右足首痛の原因となっていた。また、今季終了後にポスティングシステムを利用して、米大リーグに挑戦することが同日、濃厚となった。昨年１２月の契約更改交渉で、球団も本人の意思を尊重することを表明しており、シーズン終了後に本人と話し合い、最終的な決断を下す。')),
    list(token_generator('東芝が、「日米韓連合」を軸に東芝メモリの売却交渉に臨む方針に転じたのは、本命だった「日米連合」を主導するＷＤが条件闘争で譲らず、合意が難しいと判断したからだ。債務超過の解消に残された時間の少ない東芝の弱みを見透かし、強気な姿勢を貫くＷＤへの不信感が改めて浮き彫りになった。ただ、日米韓連合と契約しても、東芝がＷＤとの訴訟に負ければ売却自体が暗礁に乗り上げる。')),
]
category_list = ['経済', '経済', '経済でない', '経済でない', '経済']

dictionary = corpora.Dictionary(doc_list)

corpus = [dictionary.doc2bow(doc) for doc in doc_list]

# ロジスティック回帰


doc_matrix = matutils.corpus2csc(corpus).transpose()
X = doc_matrix
y = np.array([1, 1, 0, 0, 1])

reg = LogisticRegression()
reg.fit(X, y)

# 結果を見る

result_df = pd.DataFrame([
    (token, reg.coef_[0][token_id]) for token_id, token in dictionary.iteritems()
])
result_df.columns = ['token', 'coef']
print('学習したパラメータ(特徴的なもの)')
print(result_df.ix[result_df['coef'].abs() > 0.1].sort_values('coef'))

# 経済の記事かどうかを予測

input_text = '東芝は１３日、半導体子会社「東芝メモリ」の売却について、政府系の産業革新機構や米ファンドのベインキャピタル、韓国半導体のＳＫハイニックスなどの「日米韓連合」と、９月下旬の契約締結を目指して覚書を結んだ、と発表した。ただ、日米韓連合を「排他的な交渉先としない」ともしており、他の売却先も引き続き検討する模様だ。'
print('入力テキスト:')
print(input_text)

input_bow = dictionary.doc2bow(list(token_generator(input_text)))
test_x = matutils.corpus2csc([input_bow], X.shape[1]).transpose()
pred_y = reg.predict_proba(test_x)

print(['経済でない', '経済'])
print(pred_y[0])
