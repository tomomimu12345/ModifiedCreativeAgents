
from openai import OpenAI
import google.generativeai as genai

from base import round2, check, block_dict
import argparse 
from dotenv import load_dotenv
import os


from voyager_creative import Voyager
load_dotenv()

with open("./prompt/prompt_gpt4_first_round.txt", "r") as f:
  first_round_text = f.read()
with open("./prompt/prompt_gpt4_first_round2.txt", "r") as f:
  first_round_text2 = f.read()
with open("./prompt/prompt_gpt4_second_round.txt", "r") as f:
  second_round_text = f.read()
  
# "gpt-4-1106-preview"

def generate_response_gpt(api_key, model_name, task, text_prompt):
    conversation_history = [
        {"role": "system", "content": "Hello, I am a chatbot that can talk about anything. What would you like to talk about today?"},
        {"role": "user", "content": f"You are an architect designing houses and buildings. Here is a building you should design: {task}. \n You should answer these questions below based on your design and imagination: \n {text_prompt}"}
    ]
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model_name,
        messages=conversation_history
    )
    return response.choices[0].message.content

def generate_response_gemini(api_key, model_name, task, text_prompt):
    genai.configure(api_key=api_key)
    conversation_history = [
        {"role": "model", "parts": "Hello, I am a chatbot that can talk about anything. What would you like to talk about today?"}
    ]
    model = genai.GenerativeModel(model_name)
    chat = model.start_chat(history=conversation_history)
    response = chat.send_message(f"You are an architect designing houses and buildings. Here is a building you should design: {task}. \n You should answer these questions below based on your design and imagination: \n {text_prompt}")
    return response.text

def round1(model_name=None, task=None):
  assert task is not None, "Please provide a task!"
  # 選択されたモデルに基づいて処理
  if model_name.startswith("gpt"):
      api_key = os.getenv('OPENAI_API_KEY')
      first_round_output = generate_response_gpt(api_key, model_name, task, first_round_text)
      first_round_output2 = generate_response_gpt(api_key, model_name, task, first_round_text2)
  elif model_name.startswith("gemini"):
      api_key = os.getenv('GEMINI_API_KEY')
      first_round_output = generate_response_gemini(api_key, model_name, task, first_round_text)
      first_round_output2 = generate_response_gemini(api_key, model_name, task, first_round_text2)
  else:
      raise ValueError("Unsupported model name!")

  return first_round_output, first_round_output2

def main(model_name=None, task=None, mc_port=None):
  assert model_name is not None, "Please provide a model name!"
  assert task is not None, "Please provide a task!"
  assert mc_port is not None, "Please provide a Minecraft port!"

  second_round_output = ""
  while not check(second_round_output):
    first_round_output, first_round_output2 = round1(model_name=model_name, task=task)
    second_round_output = round2(first_round_text, first_round_text2, first_round_output, first_round_output2, second_round_text, model_name=model_name)
    
  print("init_message: "+second_round_output)
  
  blocks_dict = block_dict(second_round_text, second_round_output, model_name=model_name)
  
  sub_model_name = "gpt-3.5-turbo" if(model_name.startswith("gpt")) else model_name

  voyager = Voyager(
    mc_port = int(mc_port),
    action_agent_model_name = model_name,
    curriculum_agent_model_name = model_name,
    curriculum_agent_qa_model_name = sub_model_name,
    critic_agent_model_name = model_name,
    skill_manager_model_name = sub_model_name,
    reset_placed_if_failed=False,
    action_agent_task_max_retries=100,
    action_agent_show_chat_log=False,
    curriculum_agent_mode="manual",
    critic_agent_mode="manual",
    use_command= True,
    env_request_timeout = 1e5
  )

  print(blocks_dict)

  # start lifelong learning
  voyager.learn(init_inventory=blocks_dict, init_message=second_round_output)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--model_name", type=str, default=None)
  parser.add_argument("--task", type=str, default=None)
  parser.add_argument("--mc_port", type=int, default=None)
  args = parser.parse_args()
  main(model_name=args.model_name, task=args.task, mc_port=args.mc_port)
  
  # python cot_gpt4.py --model_name gemini-2.0-flash-thinking-exp-01-21 --task "create castle" --mc_port 50070
  # python cot_gpt4.py --model_name gemini-2.0-flash-thinking-exp-01-21 --task "create a beautiful building" --mc_port 50070
  # python cot_gpt4.py --model_name gpt-4o-2024-11-20 --task "create castle" --mc_port 50070