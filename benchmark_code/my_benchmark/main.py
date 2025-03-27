import json
import subprocess
import os

def execute_code_in_container(code, language):
    """指定されたコードを対応するコンテナで実行"""
    try:
        # 言語ごとの正しいファイル拡張子
        ext_map = {
            "Python": "py",
            "C": "c",
            "C++": "cpp",
            "VB": "vb",
            "GO": "go",
            "PHP": "php",
            "Java": "java",
            "C#": "cs"
        }
        
        if language not in ext_map:
            return {"error": f"Unsupported language: {language}"}
        
        # 一時ファイル名を正しい拡張子で生成
        temp_file = f"temp.{ext_map[language]}"
        temp_path = os.path.join("app", temp_file)
        
        # ディレクトリが存在するか確認
        os.makedirs("app", exist_ok=True)
        
        # コードを一時ファイルに書き込み
        print(f"Writing code to {temp_path}")
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(code)
        
        # ファイルが作成されたか確認
        if not os.path.exists(temp_path):
            return {"error": f"Failed to create file: {temp_path}"}
        
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
            cmd = ["docker-compose", "exec", "-T", service, "sh", "-c", "javac temp.java && java temp"]
        elif language == "C#":
            cmd = ["docker-compose", "exec", "-T", service, "sh", "-c", "csc temp.cs && mono temp.exe"]
        
        print(f"Executing command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        
        # 一時ファイルを削除
        os.remove(temp_path)
        
        return {
            "output": result.stdout,
            "error": result.stderr if result.stderr else None,
            "return_code": result.returncode
        }
    
    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out"}
    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}

def process_json(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to load input file: {str(e)}")
        return
    
    results = []
    for entry in data:
        code = entry["output"]
        language = entry["output_language"]
        
        execution_result = execute_code_in_container(code, language)
        
        result_entry = {
            "id": entry["id"],
            "language": language,
            "input_code": code,
            "execution_result": execution_result
        }
        results.append(result_entry)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    input_file = "input.json"  # 修正: app/内に配置
    output_file = "output.json"
    process_json(input_file, output_file)
    print(f"Results have been written to {output_file}")

