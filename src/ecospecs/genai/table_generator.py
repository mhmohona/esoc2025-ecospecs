# src/ecospecs/genai/table_generator.py
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from typing import List
import torch

def generate_table(
    prompt: str,
    headers: List[str],
    max_length: int = 512
) -> List[List[str]]:
    """Generate table using Phi-3-mini (4-bit quantized)"""
    try:
        # Configure 4-bit quantization
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16
        )

        # Load model and tokenizer
        model = AutoModelForCausalLM.from_pretrained(
            "microsoft/phi-3-mini-4k-instruct",
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True
        )
        tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/phi-3-mini-4k-instruct"
        )

        # Create structured prompt
        table_prompt = f"""<|system|>
        Generate a markdown table with these columns: {', '.join(headers)}.
        Follow this exact format:
        
        | {' | '.join(headers)} |
        | {' | '.join(['---']*len(headers))} |
        | ... |<|end|>
        <|user|>
        {prompt}<|end|>
        <|assistant|>
        """

        # Generate response
        inputs = tokenizer(table_prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_length,
            temperature=0.3,
            do_sample=True
        )
        
        return _parse_markdown_table(tokenizer.decode(outputs[0], skip_special_tokens=True))
    
    except Exception as e:
        raise RuntimeError(f"Generation failed: {str(e)}") from e

def _parse_markdown_table(text: str) -> List[List[str]]:
    """Robust table parsing with validation"""
    table = []
    in_table = False
    
    for line in text.split('\n'):
        if '|' in line:
            if not in_table and len(table) == 0:
                in_table = True  
                
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            if all('---' not in cell for cell in cells):  
                if len(cells) == len(table[0]) if table else True:
                    table.append(cells)
        elif in_table:
            break  # End of table
            
    return table[1:] if len(table) > 1 else table 
