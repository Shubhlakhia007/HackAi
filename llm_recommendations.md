# 🤖 Open-Source LLM Recommendations for HackAI

## 🎯 **Best Open-Source LLMs for Security Testing**

### 🥇 **Top Recommendations**

#### 1. **Mistral 7B/8x7B** (Recommended)
- **Model**: `mistralai/Mistral-7B-Instruct-v0.2`
- **Size**: 7B parameters
- **Pros**: Excellent reasoning, security-aware, good at code analysis
- **Cons**: Requires 16GB+ RAM
- **Install**: `pip install transformers torch accelerate`

#### 2. **CodeLlama 7B/13B**
- **Model**: `codellama/CodeLlama-7b-Instruct-hf`
- **Size**: 7B-13B parameters
- **Pros**: Excellent for code analysis, reverse engineering, CTF challenges
- **Cons**: Larger model requires more resources
- **Install**: `pip install transformers torch accelerate`

#### 3. **Llama 2 7B/13B**
- **Model**: `meta-llama/Llama-2-7b-chat-hf`
- **Size**: 7B-13B parameters
- **Pros**: Good general reasoning, widely supported
- **Cons**: Requires Meta approval for commercial use
- **Install**: `pip install transformers torch accelerate`

#### 4. **Phi-2/3** (Lightweight Option)
- **Model**: `microsoft/phi-2` or `microsoft/phi-3-mini`
- **Size**: 2.7B-3.8B parameters
- **Pros**: Small, fast, good reasoning, Microsoft-backed
- **Cons**: Limited context window
- **Install**: `pip install transformers torch accelerate`

### 🚀 **Quick Setup for HackAI**

```bash
# Install dependencies
pip install transformers torch accelerate sentence-transformers

# For GPU acceleration (optional)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 🎓 **Training Your Own Security LLM**

### 📚 **Training Data Collection**

#### 1. **Security Datasets**
```python
# Security-focused datasets to collect
security_datasets = {
    "ctf_challenges": [
        "HackTheBox writeups",
        "TryHackMe walkthroughs", 
        "PicoCTF solutions",
        "OverTheWire challenges"
    ],
    "vulnerability_reports": [
        "CVE descriptions",
        "Bug bounty reports",
        "Security advisories"
    ],
    "tool_documentation": [
        "Nmap documentation",
        "Metasploit guides",
        "Burp Suite tutorials",
        "Wireshark analysis"
    ],
    "forensic_analysis": [
        "Memory dump analysis",
        "Network packet analysis",
        "Malware analysis reports"
    ]
}
```

#### 2. **Data Format for Training**
```json
{
    "instruction": "Analyze this CTF challenge and suggest tools",
    "input": "Challenge: Find the flag in this binary file. File type: ELF executable",
    "output": "For this ELF binary analysis, I recommend:\n1. strings - extract readable strings\n2. objdump - disassemble the binary\n3. gdb - dynamic analysis\n4. ltrace/strace - trace system calls\n5. hexdump - examine raw bytes\n\nStart with 'strings' to look for flag patterns."
}
```

### 🏋️ **Training Methods**

#### 1. **Fine-tuning (Recommended)**
```python
# Using LoRA (Low-Rank Adaptation)
from peft import LoraConfig, get_peft_model
from transformers import TrainingArguments, Trainer

# LoRA configuration
lora_config = LoraConfig(
    r=16,  # Rank
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Training arguments
training_args = TrainingArguments(
    output_dir="./hackai-security-model",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    warmup_steps=100,
    logging_steps=10,
    save_steps=500,
    eval_steps=500,
    evaluation_strategy="steps",
    save_strategy="steps",
    load_best_model_at_end=True,
    report_to="none"
)
```

#### 2. **QLoRA (Quantized LoRA)**
```python
# For limited hardware
from transformers import BitsAndBytesConfig

# 4-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_use_double_quant=False
)

# Load model with quantization
model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.2",
    quantization_config=bnb_config,
    device_map="auto"
)
```

### 📊 **Training Data Preparation**

#### 1. **Security Prompt Templates**
```python
security_prompts = {
    "ctf_analysis": """
    You are a cybersecurity expert. Analyze this CTF challenge:
    
    Challenge: {challenge_description}
    File: {file_info}
    Hints: {hints}
    
    Provide:
    1. Challenge type classification
    2. Recommended tools (5-10 tools)
    3. Step-by-step approach
    4. Common pitfalls to avoid
    """,
    
    "vulnerability_assessment": """
    You are a penetration tester. Assess this target:
    
    Target: {target}
    Scope: {scope}
    Tools available: {tools}
    
    Provide:
    1. Reconnaissance strategy
    2. Vulnerability scanning approach
    3. Exploitation methodology
    4. Post-exploitation steps
    """,
    
    "forensic_analysis": """
    You are a digital forensics expert. Analyze this evidence:
    
    Evidence type: {evidence_type}
    File: {file_path}
    Context: {context}
    
    Provide:
    1. Analysis methodology
    2. Tools to use
    3. Key artifacts to look for
    4. Timeline reconstruction approach
    """
}
```

#### 2. **Data Augmentation**
```python
import random

def augment_security_data(original_data):
    """Augment security training data"""
    augmented = []
    
    for item in original_data:
        # Original item
        augmented.append(item)
        
        # Add variations
        variations = [
            f"Analyze this security challenge: {item['input']}",
            f"Help me solve this CTF: {item['input']}",
            f"What tools should I use for: {item['input']}",
            f"Security assessment needed for: {item['input']}"
        ]
        
        for variation in variations:
            augmented.append({
                "instruction": item["instruction"],
                "input": variation,
                "output": item["output"]
            })
    
    return augmented
```

### 🎯 **Specialized Training for Security Tasks**

#### 1. **Tool Recommendation Training**
```python
tool_training_data = [
    {
        "input": "I need to scan a web application for vulnerabilities",
        "output": "For web application vulnerability scanning, I recommend:\n1. OWASP ZAP - automated scanning\n2. Burp Suite - manual testing\n3. Nikto - web server scanning\n4. SQLMap - SQL injection testing\n5. XSStrike - XSS detection\n\nStart with OWASP ZAP for automated scanning, then use Burp Suite for manual testing."
    },
    {
        "input": "I have a binary file to analyze for a CTF",
        "output": "For binary analysis in CTF challenges:\n1. file - identify file type\n2. strings - extract readable strings\n3. objdump - disassemble binary\n4. gdb - dynamic analysis\n5. ltrace/strace - system call tracing\n6. hexdump - examine raw bytes\n\nStart with 'file' and 'strings' to understand the binary structure."
    }
]
```

#### 2. **CTF Challenge Analysis Training**
```python
ctf_training_data = [
    {
        "input": "Challenge: Find the flag in this image file. The flag is hidden using steganography.",
        "output": "For steganography challenges:\n1. binwalk - check for hidden files\n2. steghide - extract hidden data\n3. exiftool - examine metadata\n4. strings - look for embedded text\n5. hexdump - examine file structure\n6. foremost - carve files\n\nStart with 'binwalk' to detect hidden files, then use 'steghide' to extract them."
    }
]
```

### 🔧 **Integration with HackAI**

#### 1. **Updated Local LLM Provider**
```python
# Enhanced local_llm.py for security models
class SecurityLLMProvider(BaseAIProvider):
    def __init__(self, model_name="mistralai/Mistral-7B-Instruct-v0.2"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self._initialize()
    
    def _initialize(self):
        """Initialize security-focused LLM"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map="auto"
            )
            self.available = True
        except Exception as e:
            print(f"Failed to load model: {e}")
            self.available = False
    
    async def analyze_target(self, target: str) -> Dict[str, Any]:
        """Security-focused target analysis"""
        prompt = f"""
        You are a cybersecurity expert. Analyze this target for security testing:
        
        Target: {target}
        
        Provide:
        1. Target type (web, network, binary, etc.)
        2. Risk assessment (low/medium/high/critical)
        3. Recommended tools (list 5-10 specific tools)
        4. Testing strategy
        5. Precautions and legal considerations
        
        Format as JSON.
        """
        
        response = self._generate_response(prompt)
        return self._parse_security_response(response)
```

#### 2. **Model Configuration**
```python
# config.py - Model settings
SECURITY_MODEL_CONFIG = {
    "default_model": "mistralai/Mistral-7B-Instruct-v0.2",
    "fallback_model": "microsoft/phi-2",
    "max_length": 2048,
    "temperature": 0.7,
    "top_p": 0.9,
    "repetition_penalty": 1.1
}
```

### 📈 **Performance Optimization**

#### 1. **Hardware Requirements**
```bash
# Minimum requirements
- RAM: 16GB (32GB recommended)
- GPU: RTX 3080 or better (for training)
- Storage: 50GB free space
- CPU: 8+ cores recommended

# For inference only
- RAM: 8GB minimum
- GPU: Optional (CPU inference works)
- Storage: 20GB free space
```

#### 2. **Model Optimization**
```python
# Quantization for smaller models
from transformers import BitsAndBytesConfig

# 8-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,
    bnb_8bit_compute_dtype=torch.float16
)

# 4-bit quantization (smallest)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16
)
```

### 🚀 **Deployment Recommendations**

#### 1. **For Development/Testing**
- Use Phi-2 or Phi-3 (small, fast)
- CPU inference is sufficient
- Good for prototyping

#### 2. **For Production**
- Use Mistral 7B or CodeLlama 7B
- GPU acceleration recommended
- Consider model serving (vLLM, Text Generation Inference)

#### 3. **For Training**
- Use larger models (13B+ parameters)
- Multiple GPUs recommended
- Consider cloud training (AWS, Google Cloud)

### 📝 **Next Steps**

1. **Start with Phi-2** (small, fast, good for testing)
2. **Collect security training data** from CTF writeups, tool docs
3. **Fine-tune on security tasks** using LoRA
4. **Integrate with HackAI** using the enhanced local_llm.py
5. **Test and iterate** on different security scenarios

### 🔗 **Useful Resources**

- **Hugging Face Models**: https://huggingface.co/models
- **Security Datasets**: https://github.com/security-datasets
- **CTF Writeups**: https://github.com/ctf-writeups
- **Training Guides**: https://huggingface.co/docs/transformers/training
