import json
import subprocess
import os

def execute_code_in_container(code, language):
    """指定されたコードを対応するコンテナで実行"""
    try:
        # 一時ファイルにコードを書き込み
        temp_file = f"temp.{language.lower()}"
        with open(f"app/{temp_file}", "w") as f:
            f.write(code)
        
        # 言語に応じたコンテナで実行
        service_map = {
            "Python": "python",
            "C": "c",
            "C++": "cpp",
            "VB": "vb",
            "GO": "go",
            "PHP": "php",
            "Java": "java",
            "C#": "csharp"
        }
        
        if language not in service_map:
            return {"error": "Unsupported language"}
        
        service = service_map[language]
        
        # コンテナ内でコードを実行
        if language == "Python":
            cmd = ["docker-compose", "exec", "-T", service, "python", temp_file]
        elif language == "C":
            cmd = ["docker-compose", "exec", "-T", service, "sh", "-c", "gcc -o temp temp.c && ./temp"]
        elif language == "C++":
            cmd = ["docker-compose", "exec", "-T", service, "sh", "-c", "g++ -o temp temp.cpp && ./temp"]
        elif language == "VB":
            cmd = ["docker-compose", "exec", "-T", service, "sh", "-c", "vbnc temp.vb"]
        elif language == "GO":
            cmd = ["docker-compose", "exec", "-T", service, "go", "run", "temp.go"]
        elif language == "PHP":
            cmd = ["docker-compose", "exec", "-T", service, "php", temp_file]
        elif language == "Java":
            cmd = ["docker-compose", "exec", "-T", service, "sh", "-c", "javac Temp.java && java Temp"]
        elif language == "C#":
            cmd = ["docker-compose", "exec", "-T", service, "sh", "-c", "csc temp.cs && mono temp.exe"]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        
        # 一時ファイルを削除
        os.remove(f"app/{temp_file}")
        
        return {
            "output": result.stdout,
            "error": result.stderr if result.stderr else None,
            "return_code": result.returncode
        }
    
    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out"}
    except Exception as e:
        return {"error": str(e)}

def process_json(input_file, output_file):
    # JSONファイルを読み込む
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 結果を格納するリスト
    results = []
    
    # 各エントリを処理
    for entry in data:
        code = entry["output"]
        language = entry["output_language"]
        
        # コードをコンテナで実行
        execution_result = execute_code_in_container(code, language)
        
        # 結果を整形
        result_entry = {
            "id": entry["id"],
            "language": language,
            "output_code": code,
            "execution_result": execution_result
        }
        results.append(result_entry)
    
    # 結果をJSONファイルに書き込む
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    input_file = "input.json"
    output_file = "output.json"
    process_json(input_file, output_file)
    print(f"Results have been written to {output_file}")