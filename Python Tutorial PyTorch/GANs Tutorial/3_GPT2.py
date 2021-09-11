# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

"""
Open this file using VS Code to use intereactive shell
"""

#%%
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2-xl")
model = GPT2LMHeadModel.from_pretrained("gpt2-xl")
# %%

# %%
sequence = "Jesus"

inputs = tokenizer.encode(sequence, return_tensors="pt")
outputs = model.generate(inputs, do_sample=True, max_length=100) # avoid repeats, temperature is amount of randomness, top_k is top rated
text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("\n", text)


# %%
