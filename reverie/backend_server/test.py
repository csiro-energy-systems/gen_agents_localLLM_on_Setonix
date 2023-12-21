"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: gpt_structure.py
Description: Wrapper functions for calling OpenAI APIs.
"""
import json
import random
import time 

import openai
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel

from utils import *
openai.api_key = openai_api_key

def ChatGPT_request(prompt): 
  """
  Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
  server and returns the response. 
  ARGS:
    prompt: a str prompt
    gpt_parameter: a python dictionary with the keys indicating the names of  
                   the parameter and the values indicating the parameter 
                   values.   
  RETURNS: 
    a str of GPT-3's response. 
  """
  # temp_sleep()
  try: 
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": prompt}]
    )
    return completion["choices"][0]["message"]["content"]
  
  except: 
    print ("ChatGPT ERROR")
    return "ChatGPT ERROR"


### added by Yusuke 18/12/2023
  
def local_LLM(prompt, model_param=None): 
  """
  Given a prompt and a dictionary of parameters, run LLM text generation and returns the response. 
  ARGS:
    prompt: a str prompt
    model_parameter: a python dictionary with the keys indicating the names of  
                   the parameter and the values indicating the parameter 
                   values.   
  RETURNS: 
    a str of local_LLM's response. 
  """
  # temp_sleep()

  # specify LLM params
  if model_param is not None:
    max_new_tokens = model_param["max_tokens"]
    temperature = model_param["temperature"]
    
    # may remove this chuck later, https://discuss.huggingface.co/t/help-with-llama-2-finetuning-setup/50035/8
    if temperature == 0:
      do_sample=False
    else:
      do_sample=True

  else:
    max_new_tokens = 100
    temperature = 0.5
    do_sample=True
  
  #try: 
  # Loading model and tokenizer
    
  ## TODO calling tokenizer and model in every function call may be redundant
  tokenizer = AutoTokenizer.from_pretrained(checkpoint)
  model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device) # device_map="auto" distributes LLM accross multiple GPUs (DON'T SET DEVICE MAP FOR TRAINING; ONLY FOR INFERENCING)
  inputs = tokenizer(prompt, return_tensors="pt").to(device) # Tokenize
  start_index = inputs["input_ids"].shape[-1]
  outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=do_sample, temperature=temperature) # Generate output  
  generation_output = outputs[0][start_index:]

  return tokenizer.decode(generation_output, skip_special_tokens=True)
  
  
  #except: 
  #  print ("Local LLM ERROR")
  #  return "Local LLM ERROR"


def get_embedding(text):
  text = text.replace("\n", " ")
  if not text: 
    text = "this is blank"

  model = AutoModel.from_pretrained(embedding_checkpoint, trust_remote_code=True).to(device) # trust_remote_code is needed to use the encode method
  embedding = model.encode([text])[0]
  return embedding




prompt = """
---
Character 1: Maria Lopez is working on her physics degree and streaming games on Twitch to make some extra money. She visits Hobbs Cafe for studying and eating just about everyday.
Character 2: Klaus Mueller is writing a research paper on the effects of gentrification in low-income communities.

Past Context: 
138 minutes ago, Maria Lopez and Klaus Mueller were already conversing about conversing about Maria's research paper mentioned by Klaus This context takes place after that conversation.

Current Context: Maria Lopez was attending her Physics class (preparing for the next lecture) when Maria Lopez saw Klaus Mueller in the middle of working on his research paper at the library (writing the introduction).
Maria Lopez is thinking of initating a conversation with Klaus Mueller.
Current Location: library in Oak Hill College

(This is what is in Maria Lopez's head: Maria Lopez should remember to follow up with Klaus Mueller about his thoughts on her research paper. Beyond this, Maria Lopez doesn't necessarily know anything more about Klaus Mueller) 

(This is what is in Klaus Mueller's head: Klaus Mueller should remember to ask Maria Lopez about her research paper, as she found it interesting that he mentioned it. Beyond this, Klaus Mueller doesn't necessarily know anything more about Maria Lopez) 

Here is their conversation. 

Maria Lopez: "
---
Output the response to the prompt above in json. The output should be a list of list where the inner lists are in the form of ["<Name>", "<Utterance>"]. Output multiple utterances in ther conversation until the conversation comes to a natural conclusion.
Example output json:
{"output": "[["Jane Doe", "Hi!"], ["John Doe", "Hello there!"] ... ]"}
"""

#device = "cuda" if torch.cuda.is_available() else "cpu"
gpt_param = {"engine": "text-davinci-003", "max_tokens": 20, 
             "temperature": 0, "top_p": 1, "stream": False,
             "frequency_penalty": 0, "presence_penalty": 0, "stop": None}

#print (ChatGPT_request(prompt))
print (local_LLM(prompt))

#print(get_embedding(prompt))
