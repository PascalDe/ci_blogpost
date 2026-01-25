import os
from huggingface_hub import hf_hub_download

repo_id   = "TheBloke/TinyLlama-1.1B-Chat-v0.3-GGUF"
filename  = "tinyllama-1.1b-chat-v0.3.Q4_K_M.gguf"
save_dir  = os.path.expanduser("./models")

os.makedirs(save_dir, exist_ok=True)

# Huggingface token
token = "[YOUR_TOKEN_HERE]" # <-- Enter your token here!

path = hf_hub_download(
    repo_id=repo_id,
    filename=filename,
    cache_dir=save_dir,
    token=token
)

print("Model saved here:", path)