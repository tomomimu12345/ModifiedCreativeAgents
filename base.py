import os
from openai import OpenAI
import google.generativeai as genai
from block2num import block2num


def round2(first_round_text, first_round_text2, first_round_output, first_round_output2, second_input, model_name=None):
  if model_name.startswith("gpt"):
    api_key = os.getenv('OPENAI_API_KEY')
    conversation_history = [
        {"role": "system", "content": "Hello, I am a chatbot that can talk about anything. What would you like to talk about today?"},
        {"role": "user", "content": first_round_text + first_round_text2},
        {"role": "assistant", "content": first_round_output + first_round_output2},
        {"role": "user", "content": second_input}
    ]

    client = OpenAI(api_key=api_key)

    # Sending the message to the API including the entire conversation history
    response = client.chat.completions.create(
        model=model_name,       # can change to your own choice
        messages=conversation_history     # Include the conversation history
    )

    # Extracting the completion response
    second_round_output = response.choices[0].message.content
  elif model_name.startswith("gemini"):
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    
    conversation_history = [
        {"role": "model", "parts": "Hello, I am a chatbot that can talk about anything. What would you like to talk about today?"},
        {"role": "user", "parts": first_round_text + first_round_text2},
        {"role": "model", "parts": first_round_output + first_round_output2}
    ]

    model = genai.GenerativeModel(model_name)
    chat = model.start_chat(
        history=conversation_history
    )
    response = chat.send_message(second_input)

    # Extracting the completion response
    second_round_output = response.text
  return second_round_output

def check(second_round_output):
  # Check if the output is well-formed
  if "Explain:" in second_round_output and "Plan:" in second_round_output and "Code:" in second_round_output:
    return True
  else:
    return False
  
def block_dict(second_round_text, second_round_output, model_name=None):
  if model_name.startswith("gpt"):
    api_key = os.getenv('OPENAI_API_KEY')
    # Extract the block name and number from the output
    conversation_history = [
        {"role": "system", "content": "Hello, I am a chatbot that can talk about anything. What would you like to talk about today?"},
        {"role": "user", "content": second_round_text},
        {"role": "assistant", "content": second_round_output},
        {"role": "user", "content": "From your last response, please list all the blocks you used in your code. You should answer in the format as: block_1, block_2, block_3, ..."}
    ]
    client = OpenAI(api_key=api_key)

    # Sending the message to the API including the entire conversation history
    response = client.chat.completions.create(
        model=model_name,       # can change to your own choice
        messages=conversation_history     # Include the conversation history
    )

    blocks_list = response.choices[0].message.content
    
  elif model_name.startswith("gemini"):
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    
    conversation_history = [
        {"role": "model", "parts": "Hello, I am a chatbot that can talk about anything. What would you like to talk about today?"},
        {"role": "user", "parts": second_round_text},
        {"role": "model", "parts": second_round_output}
    ]

    model = genai.GenerativeModel(model_name)
    chat = model.start_chat(
        history=conversation_history
    )
    response = chat.send_message("From your last response, please list all the blocks you used in your code. You should answer in the format as: block_1, block_2, block_3, ...")

    # Extracting the completion response
    blocks_list = response.text
  if blocks_list.startswith("RESPONSE FORMAT:\n"):
    blocks_list = blocks_list.replace("RESPONSE FORMAT:\n","")
  blocks_list = blocks_list.split(", ")
  blocks_dict = {"diamond_pickaxe": 1}
  for block in blocks_list:
    blocks_dict[block] = block2num(block)
  return blocks_dict