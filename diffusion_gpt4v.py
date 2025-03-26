import base64
import requests
from openai import OpenAI
from voyager_creative import Voyager
import argparse 
from base import round2, check, block_dict
import google.generativeai as genai
import PIL.Image
import os
from dotenv import load_dotenv
load_dotenv()

with open("./prompt/prompt_gpt4v_first_round.txt", "r") as f:
  first_round_text = f.read()
with open("./prompt/prompt_gpt4v_first_round2.txt", "r") as f:
  first_round_text2 = f.read()
with open("./prompt/prompt_gpt4v_second_round.txt", "r") as f:
  second_round_text = f.read()

# "gpt-4-vision-preview"  
# "gpt-4-1106-preview"

def generate_vision_response(model_name, text_prompt, image_path):
  if model_name.startswith("gpt"):
      api_key = os.getenv('OPENAI_API_KEY')
      
      # Encode image to base64
      def encode_image(image_path):
          with open(image_path, "rb") as image_file:
              return base64.b64encode(image_file.read()).decode('utf-8')

      base64_image = encode_image(image_path)

      headers = {
          "Content-Type": "application/json",
          "Authorization": f"Bearer {api_key}"
      }

      payload = {
          "model": model_name,
          "messages": [
              {
                  "role": "user",
                  "content": [
                      {"type": "text", "text": text_prompt},
                      {"type": "image_url", "image_url": {"url": f"data:image/jpg;base64,{base64_image}"}}
                  ]
              }
          ],
          "max_tokens": 4096
      }

      response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
      return response.json()['choices'][0]['message']['content']
  
  elif model_name.startswith("gemini"):
      api_key = os.getenv('GEMINI_API_KEY')
      genai.configure(api_key=api_key)
      model = genai.GenerativeModel(model_name)
      image = PIL.Image.open(image_path)
      response = model.generate_content([text_prompt, image])
      return response.text
  
  else:
      raise ValueError("Unsupported model name!")

def round1(vision_model_name=None, image_path=None):
  assert image_path is not None, "Please provide an image path!"
  
  prompt = "You are an architect designing houses and buildings. Here is an image of building from Minecraft. \n Based on the image, you should answer these questions: \n"

  first_round_output = generate_vision_response(
      vision_model_name, 
      f"{prompt} {first_round_text}", 
      image_path
  )
  
  first_round_output2 = generate_vision_response(
      vision_model_name, 
      f"{prompt} {first_round_text2}", 
      image_path
  )
  
  return first_round_output, first_round_output2

def main(model_name=None, vision_model_name = None, image_path=None, mc_port=None):
  assert model_name is not None, "Please provide an model_name!"
  assert vision_model_name is not None, "Please provide a vision model name"
  assert image_path is not None, "Please provide an image path!"
  assert mc_port is not None, "Please provide a Minecraft port!"

  second_round_output = ""
  while not check(second_round_output):
    first_round_output, first_round_output2 = round1(vision_model_name=vision_model_name, image_path=image_path)
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
  parser.add_argument("--vision_model_name", type=str, default=None)
  parser.add_argument("--image_path", type=str, default="./image.jpg")
  parser.add_argument("--mc_port", type=int, default=None)
  args = parser.parse_args()
  main(model_name=args.model_name, vision_model_name = args.vision_model_name, image_path=args.image_path, mc_port=args.mc_port)
  
# python diffusion_gpt4v.py --model_name gemini-2.0-flash-thinking-exp-01-21 --vision_model_name gemini-2.0-flash-thinking-exp-01-21 --image_path building_castle.webp --mc_port 50070
# python diffusion_gpt4v.py --model_name gpt-4o-2024-11-20 --vision_model_name gpt-4o-2024-11-20 --image_path building_castle.webp --mc_port 50070

# python diffusion_gpt4v.py --model_name gemini-2.0-flash-thinking-exp-01-21 --vision_model_name gemini-2.0-flash-thinking-exp-01-21 --image_path image1.png --mc_port 50070 
