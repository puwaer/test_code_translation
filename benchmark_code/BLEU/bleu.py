import json
import os
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def bleu_score(input_1, input_2):
    reference = input_1.split()
    candidate = input_2.split()
    smoothie = SmoothingFunction().method1 
    bleu_score_4 = sentence_bleu([reference], candidate, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=smoothie)
    return bleu_score_4

def process_json(input_file_1, input_file_2, output_file):
    try:
        with open(input_file_1, 'r', encoding='utf-8') as f:
            data_1 = json.load(f)
        with open(input_file_2, 'r', encoding='utf-8') as f:
            data_2 = json.load(f)
    except Exception as e:
        print(f"Failed to load input file: {str(e)}")
        return
    
    # IDをキーにしてdata_2のエントリをマッピング
    data_2_map = {entry["id"]: entry for entry in data_2}
    
    results = []
    for entry_1 in data_1:
        entry_id = entry_1["id"]
        code = entry_1["output"]
        input_language = entry_1["input_language"]
        output_language = entry_1["output_language"]
        
        # 対応するdata_2のエントリを取得
        entry_2 = data_2_map.get(entry_id)
        if entry_2 is None:
            print(f"Warning: No matching entry found for id {entry_id} in input_2.json")
            continue
            
        # 両方の"output"を比較
        text_1 = entry_1["output"]
        text_2 = entry_2["output"]
        
        execution_result = bleu_score(text_1, text_2)
        
        result_entry = {
            "id": entry_id,
            "input_language": input_language,            
            "output_language": output_language,
            "execution_result": execution_result
        }
        results.append(result_entry)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    input_file_1 = "./benchmark_result/multilingual_test_prompt_300.json"  
    input_file_2 = "./benchmark_result/llm_llama-3.2-1B_lora_1_output.json"  
    output_file = "./benchmark_result/bleu_score.json"
    process_json(input_file_1, input_file_2, output_file)



