FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    tree-sitter==0.23.2 \
    tree-sitter-java==0.23.5 \
    tree-sitter-python==0.23.6 \
    numpy

# プロジェクト全体をコピー
COPY . /app/

CMD ["python", "run_score.py", "--input_file", "./benchmark_data/test_data.json", "--source_names", "Python", "--target_names", "Java", "--codebleu"]