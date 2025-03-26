import json
from collections import Counter
import os

# 言語と拡張子のマッピング
LANGUAGE_EXTENSIONS = {
    "C": ".c",
    "C++": ".cpp",
    "Python": ".py",
    "Crystal": ".cr",
    "Go": ".go",
    "Rust": ".rs",
    "Ruby": ".rb",
    "Kotlin": ".kn",
    "C#": ".cs",
    "Swift": ".swift",
    "Java": ".java",
    "JavaScript": ".js",
    "TypeScript": ".ts",
    "PHP": ".php",
}

def analyze_language_combinations(json_filename, output_filename="language_analysis_result.json"):
    # ファイルの存在確認
    if not os.path.exists(json_filename):
        print(f"エラー: ファイル '{json_filename}' が見つかりません。")
        return

    # JSONファイルを読み込む
    try:
        with open(json_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"エラー: '{json_filename}' は有効なJSONファイルではありません。")
        return
    except Exception as e:
        print(f"エラー: ファイルの読み込み中に問題が発生しました - {e}")
        return

    # 言語の組み合わせをカウントするためのリスト
    language_combinations = []

    # 各エントリをチェック
    for entry in data:
        languages = []
        for lang in LANGUAGE_EXTENSIONS.keys():
            if lang in entry and entry[lang]:  # 言語キーが存在し、空でない場合
                languages.append(lang)
        # 言語の組み合わせをタプルとして追加（ソートして一貫性を持たせる）
        language_combinations.append(tuple(sorted(languages)))

    # 組み合わせの出現頻度をカウント
    combination_counts = Counter(language_combinations)

    # 結果を整形（言語名と拡張子付き）
    combinations_result = {}
    for combo, count in combination_counts.items():
        if combo:
            combo_key = " と ".join(f"{lang} ({LANGUAGE_EXTENSIONS[lang]})" for lang in combo)
            combinations_result[combo_key] = count
        else:
            combinations_result["言語なし"] = count

    # 個々の言語の出現頻度も計算
    language_counts = {lang: 0 for lang in LANGUAGE_EXTENSIONS.keys()}
    for entry in data:
        for lang in LANGUAGE_EXTENSIONS.keys():
            if lang in entry and entry[lang]:
                language_counts[lang] += 1

    # 個々の言語の結果を整形
    individual_result = {
        f"{lang} ({LANGUAGE_EXTENSIONS[lang]})": count 
        for lang, count in language_counts.items() if count > 0
    }

    # JSON用の結果オブジェクトを作成
    result = {
        "language_combinations": combinations_result,
        "individual_languages": individual_result
    }

    # JSONファイルに出力
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"分析結果を '{output_filename}' に保存しました。")
    except Exception as e:
        print(f"エラー: JSONファイルの保存中に問題が発生しました - {e}")

    # コンソールにも結果を表示
    print(f"\n'{json_filename}' 内の言語の組み合わせとその出現頻度:")
    for combo, count in combinations_result.items():
        print(f"{combo}: {count} 回")

    print("\n個々の言語の出現頻度:")
    for lang, count in individual_result.items():
        print(f"{lang}: {count} 回")

# メイン処理
if __name__ == "__main__":
    filename = "./data/benchmark_data/multilingual_test_fix.json"
    output_filename = "./data/backup_data/language_analysis_result.json"
    analyze_language_combinations(filename,output_filename)