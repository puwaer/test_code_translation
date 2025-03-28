import json
from collections import Counter

def process_json(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"エラー: 入力ファイル {input_file} が見つかりません")
        return
    except json.JSONDecodeError:
        print(f"エラー: {input_file} は有効なJSONファイルではありません")
        return

    combinations = [(item["input_language"], item["output_language"]) for item in data]
    combination_counts = Counter(combinations)
    
    # 各組み合わせごとのbleu_score_4のリストを作成
    bleu_scores = {}
    all_bleu_scores = []  
    for item in data:
        key = (item["input_language"], item["output_language"])
        if key not in bleu_scores:
            bleu_scores[key] = []
        bleu_scores[key].append(item["bleu_score_4"])
        all_bleu_scores.append(item["bleu_score_4"])  

    bleu_averages = {
        key: sum(scores) / len(scores)
        for key, scores in bleu_scores.items()
    }

    # 全体のbleu_score_4の平均を計算
    overall_bleu_avg = sum(all_bleu_scores) / len(all_bleu_scores) if all_bleu_scores else 0

    sorted_combinations = sorted(
        combination_counts.items(),
        key=lambda x: (-x[1], x[0][0], x[0][1])
    )

    result = {
        "combination_counts_and_bleu4_avg": {
            f"{input_lang} -> {output_lang}": {
                "count": count,
                "bleu_score_4_average": round(bleu_averages[(input_lang, output_lang)],6)
            }
            for (input_lang, output_lang), count in sorted_combinations
        },
        "total_unique_combinations": len(combination_counts),
        "overall_bleu_score_4_average": round(overall_bleu_avg,6)
    }

    print("Input-Output言語の組み合わせとその出現回数・BLEUスコア4の平均（多い順）:")
    for (input_lang, output_lang), count in sorted_combinations:
        avg_bleu = bleu_averages[(input_lang, output_lang)]
        print(f"{input_lang} -> {output_lang}: {count}回, BLEU-4平均: {avg_bleu:.6f}")
    print(f"\nユニークな組み合わせの総数: {len(combination_counts)}")
    print(f"全体のBLEUスコア4の平均: {overall_bleu_avg:.6f}")

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n結果を {output_file} に保存しました")
    except Exception as e:
        print(f"エラー: 出力ファイルの保存に失敗しました - {str(e)}")

if __name__ == "__main__":
    input_file = "./benchmark_result/bleu_score/bleu_score_llama-3.2-1B_lora_2.json"
    output_file = "./benchmark_result/analysis_program_bleu/avg_bleu_score_llama-3.2-1B_lora_2.json"
    process_json(input_file, output_file)