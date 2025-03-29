from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import MeCab

# MeCabを使用して日本語をトークン化
mecab = MeCab.Tagger("-Owakati")                # 分かち書きモード
output_1 = "吾輩はねこである。名前はまだ無い"
output_2 = "私は猫です。名前はまだありません"

reference = mecab.parse(output_1).strip().split()  # ['吾輩', 'は', 'ねこ', 'で', 'ある', '。', '名前', 'は', 'まだ', '無い']
candidate = mecab.parse(output_2).strip().split()  # ['私', 'は', '猫', 'です', '。', '名前', 'は', 'まだ', 'あり', 'ませ', 'ん']

smoothie = SmoothingFunction().method1 
bleu_score_1 = sentence_bleu([reference], candidate, weights=(1, 0, 0, 0), smoothing_function=smoothie)                 # 1-gram
bleu_score_2 = sentence_bleu([reference], candidate, weights=(0.5, 0.5, 0, 0), smoothing_function=smoothie)             # 2-gram
bleu_score_3 = sentence_bleu([reference], candidate, weights=(0.33, 0.33, 0.33, 0), smoothing_function=smoothie)        # 3-gram
bleu_score_4 = sentence_bleu([reference], candidate, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=smoothie)     # 4-gram

print(f"BLEU-1 score: {bleu_score_1}")
print(f"BLEU-2 score: {bleu_score_2}")
print(f"BLEU-3 score: {bleu_score_3}")
print(f"BLEU-4 score: {bleu_score_4}")