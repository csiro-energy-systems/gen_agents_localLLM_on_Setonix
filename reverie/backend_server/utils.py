# Copy and paste your OpenAI API Key
openai_api_key = "" # keep this empty as we use LocalLLM
# Put your name
key_owner = "" # keep this empty

# huggingface key to load localLLM
from huggingface_hub import login
# change this to your key
hf_hey = "" 
login(hf_hey)

embedding_checkpoint = "jinaai/jina-embeddings-v2-base-en"

# declare model here so function do not have to call this part everytime
import os
import torch

# Set the desired GPU device index (0, 1, 2, etc.)
desired_gpu_index = 0
# Set the CUDA_VISIBLE_DEVICES environment variable
os.environ["CUDA_VISIBLE_DEVICES"] = str(desired_gpu_index)

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device: ",device)

## added by Phoebe 1/2025
if torch.cuda.is_available():
    print("CUDA is available.")
    print(f"Current GPU: {torch.cuda.get_device_name(0)}")
    print(f"Allocated memory at utils: {torch.cuda.memory_allocated(0) / 1024**2:.2f} MB")
    print(f"Cached memory at utils: {torch.cuda.memory_reserved(0) / 1024**2:.2f} MB")
else:
    print("CUDA is not available.")

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig



'''
4 bit model

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

checkpoint = "meta-llama/Llama-2-70b-chat-hf" #"TheBloke/Llama-2-70B-Chat-fp16"  
model = AutoModelForCausalLM.from_pretrained(checkpoint, quantization_config=bnb_config, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
tokenizer.pad_token_id = tokenizer.eos_token_id    # for open-ended generation
'''


torch.cuda.empty_cache()
def set_cuda_alloc_conf(max_split_size_mb):
    os.environ['PYTORCH_CUDA_ALLOC_CONF'] = f'max_split_size_mb:{max_split_size_mb},{max_split_size_mb},{max_split_size_mb}'

# Check if the key exists before deleting it
if 'PYTORCH_CUDA_ALLOC_CONF' in os.environ:
    del os.environ['PYTORCH_CUDA_ALLOC_CONF']

# change this to your desired model
checkpoint = "mistralai/Mistral-7B-Instruct-v0.1"  
# checkpoint = "mistralai/Ministral-8B-Instruct-2410"
#checkpoint = "mistralai/Mixtral-8x7B-Instruct-v0.1"
#checkpoint = "meta-llama/Llama-2-13b-chat-hf"
print(f"Checkpoint: {checkpoint}")
model = AutoModelForCausalLM.from_pretrained(checkpoint, trust_remote_code=True, torch_dtype=torch.bfloat16).to(device)#, device_map="auto") 


tokenizer = AutoTokenizer.from_pretrained(checkpoint)
tokenizer.pad_token_id = tokenizer.eos_token_id    # for open-ended generation
print(f"PAD Token ID: {tokenizer.pad_token_id}, EOS Token ID: {tokenizer.eos_token_id}")



maze_assets_loc = "../../environment/frontend_server/static_dirs/assets"
env_matrix = f"{maze_assets_loc}/the_ville/matrix"
env_visuals = f"{maze_assets_loc}/the_ville/visuals"

fs_storage = "../../environment/frontend_server/storage"
fs_temp_storage = "../../environment/frontend_server/temp_storage"

collision_block_id = "32125"

# Verbose 
debug = True
