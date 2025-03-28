import json
import random

def sample_and_reindex_json(input_file, output_file, n):
    # 入力ファイルからJSONを読み込み
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # n個をランダムサンプリング
    random_samples = random.sample(data, n)
    
    # IDを1から順番に振り直し
    for i, item in enumerate(random_samples, 1):
        item['id'] = i
    
    # 出力ファイルに保存
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(random_samples, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    #input_filename = "./data/benchmark_data/multilingual_test_prompt.json"    
    #output_filename = "./data/benchmark_data/multilingual_test_prompt_300.json"
    input_filename = "./data/benchmark_data/multilingual_test_prompt.json"    
    output_filename = "./data/benchmark_data/multilingual_test_prompt_500.json"
    
    # サンプリングする数（例として5としています）
    sample_size = 500
    
    try:
        sample_and_reindex_json(input_filename, output_filename, sample_size)
        print(f"Successfully sampled {sample_size} items from {input_filename} to {output_filename}")
    except FileNotFoundError:
        print(f"Error: Input file {input_filename} not found")
    except ValueError as e:
        print(f"Error: {e} - Sample size might be larger than available data")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")