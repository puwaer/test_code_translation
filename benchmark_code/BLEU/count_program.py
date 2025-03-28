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

    # input_languageとoutput_languageの組み合わせを抽出
    combinations = [(item["input_language"], item["output_language"]) for item in data]
    combination_counts = Counter(combinations)

    # 出現回数の多い順にソート
    sorted_combinations = dict(sorted(
        combination_counts.items(),
        key=lambda x: (-x[1], x[0][0], x[0][1])  # カウント降順、入力言語、出力言語の順でソート
    ))

    result = {
        "combination_counts(input_language -> output_language)": {
            f"{input_lang} -> {output_lang}": count 
            for (input_lang, output_lang), count in sorted_combinations.items()
        },
        "total_unique_combinations": len(combination_counts)
    }

    print("Input-Output言語の組み合わせとその出現回数（多い順）:")
    for (input_lang, output_lang), count in sorted_combinations.items():
        print(f"{input_lang} -> {output_lang}: {count}回")
    print(f"\nユニークな組み合わせの総数: {len(combination_counts)}")

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n結果を {output_file} に保存しました")
    except Exception as e:
        print(f"エラー: 出力ファイルの保存に失敗しました - {str(e)}")

if __name__ == "__main__":
    input_file = "./benchmark_result/multilingual_test_prompt_300.json"
    output_file = "./benchmark_result/analysis_bleu_program/multilingual_test_prompt_300_count_program.json"
    #input_file = "./data/benchmark_data/multilingual_test_prompt.json"
    #output_file = "./benchmark_result/analysis_bleu_program/multilingual_test_prompt_count_program.json"

    process_json(input_file, output_file)