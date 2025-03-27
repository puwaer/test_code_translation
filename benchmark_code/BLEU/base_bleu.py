import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# 2つのコードを文字列として定義
output_1 = "package main\n\nimport (\n\t\"fmt\"\n\t\"math/rand\"\n)\n\nfunc main() {\n\tlist := []int{1, 3, 6, 9, 11, 18}\n\trand.Seed(int(time.Now().UnixNano()))\n\tvar sum, mod uint64; bestCount, h, e = 0, list[0], 0;\n\tfor i := 0;i < 10000;i++ {\n\t\tmod = uint64(rand.Intn(10))\n\t\t\n\t\tsum += list[rand.Intn(len(list))]\n\t\t\n\t\t\n\t\tif mod + sum!= 45 {\n\t\t\ti -= 1\n\t\t\tcontinue \n\t\t}\n\n\t\t\n\t\te += 1 \n\n\t\t\n\t\th = rand.Uint64()%uint32(list[len(list)-1])\n\t\t\n\n\t\tif h > sum {\n\t\t\tbestCount++\n\t\t\t\n\t\t\tfmt.Printf(\"%d \", list[h])\n\n\t\t\t\n\t\t\t\n\t\t\tif bestCount >= 3 {\n\t\t\t\th = rand.Uint64()%uint32(list[len(list)-1])  \n\t\t\t\t\n\t\t\t\tbreak\n\t\t\t}\t\n\t\t}\n\t}\n\tfmt.Println(\"\\nfound\", bestCount, \"out of\", 10000)\n\tfmt.Printf(\"\\nThe unique numbers are:\\n %v\\n\", fmt.Split(list[:bestCount], \"\\n\"))\n}\n"
output_2 = "package main\n\nimport (\n    \"fmt\"\n    \"math\"\n    \"math/rand\"\n    \"strings\"\n    \"time\"\n)\n\nfunc rng(modifier func(x float64) float64) float64 {\n    for {\n        r1 := rand.Float64()\n        r2 := rand.Float64()\n        if r2 < modifier(r1) {\n            return r1\n        }\n    }\n}\n\nfunc commatize(n int) string {\n    s := fmt.Sprintf(\"%d\", n)\n    if n < 0 {\n        s = s[1:]\n    }\n    le := len(s)\n    for i := le - 3; i >= 1; i -= 3 {\n        s = s[0:i] + \",\" + s[i:]\n    }\n    if n >= 0 {\n        return s\n    }\n    return \"-\" + s\n}\n\nfunc main() {\n    rand.Seed(time.Now().UnixNano())\n    modifier := func(x float64) float64 {\n        if x < 0.5 {\n            return 2 * (0.5 - x)\n        }\n        return 2 * (x - 0.5)\n    }\n    const (\n        N              = 100000\n        NUM_BINS       = 20\n        HIST_CHAR      = \"■\"\n        HIST_CHAR_SIZE = 125\n    )\n    bins := make([]int, NUM_BINS) \n    binSize := 1.0 / NUM_BINS\n    for i := 0; i < N; i++ {\n        rn := rng(modifier)\n        bn := int(math.Floor(rn / binSize))\n        bins[bn]++\n    }\n\n    fmt.Println(\"Modified random distribution with\", commatize(N), \"samples in range [0, 1):\\n\")\n    fmt.Println(\"    Range           Number of samples within that range\")\n    for i := 0; i < NUM_BINS; i++ {\n        hist := strings.Repeat(HIST_CHAR, int(math.Round(float64(bins[i])/HIST_CHAR_SIZE)))\n        fi := float64(i)\n        fmt.Printf(\"%4.2f ..< %4.2f  %s %s\\n\", binSize*fi, binSize*(fi+1), hist, commatize(bins[i]))\n    }\n}\n"

reference = output_1.split()
candidate = output_2.split()

# BLEUスコアの計算（1-gramから4-gramまで）
smoothie = SmoothingFunction().method1 
bleu_score_1 = sentence_bleu([reference], candidate, weights=(1, 0, 0, 0), smoothing_function=smoothie)                 # 1-gram
bleu_score_2 = sentence_bleu([reference], candidate, weights=(0.5, 0.5, 0, 0), smoothing_function=smoothie)             # 2-gram
bleu_score_3 = sentence_bleu([reference], candidate, weights=(0.33, 0.33, 0.33, 0), smoothing_function=smoothie)        # 3-gram
bleu_score_4 = sentence_bleu([reference], candidate, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=smoothie)     # 4-gram

# 結果の出力
print(f"BLEU-1 score: {bleu_score_1}")
print(f"BLEU-2 score: {bleu_score_2}")
print(f"BLEU-3 score: {bleu_score_3}")
print(f"BLEU-4 score: {bleu_score_4}")