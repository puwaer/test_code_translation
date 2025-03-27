モデル llama-3.2-1B
test_name llama-3.2-1B_lora_2
deta multilingual_train_and_kyopro.json

high_para
max_seq_length = 1024                                  
dtype = None                                           
load_in_4bit = True     
r = 16,                                                         
target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
lora_alpha = 16,                                               
lora_dropout = 0,                                              
bias = "none",
use_gradient_checkpointing = "unsloth",
random_state = 3407,                                           
use_rslora = False,
loftq_config = None,
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset=dataset["train"],
    max_seq_length = max_seq_length,
    dataset_text_field="formatted_text",
    packing = False,
    args = TrainingArguments(
        per_device_train_batch_size = 4,
        gradient_accumulation_steps = 4,
        num_train_epochs = 1,
        logging_steps = 10,
        warmup_steps = 10,
        save_steps=100,
        save_total_limit=2,
        max_steps=-1,
        learning_rate = 2e-4,                   
        fp16 = not is_bfloat16_supported(),
        bf16 = is_bfloat16_supported(),
        group_by_length=True,
        seed = 3407,                            
        output_dir = model_adapter,             
        report_to = "wandb",
    ),
)

プロンプトの定型文
prompt = """### Instruction
f"Translate {input_language} to {output_language}:{input_code}\nDo not return anything including notes and the like except for one translated {output_language} code."
### Response
{}"""

