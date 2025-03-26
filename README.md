# Modified Creative Agents
modified version of creative agents
This project is based on “[CreativeAgents](https://github.com/PKU-RL/Creative-Agents)”.  
The original README can be found [here](https://github.com/PKU-RL/Creative-Agents/blob/main/README.md).

## Modification
- Add option for immediate placement by command (use_command= True)
- Added utility functions for placing primitive shapes
- Fixed to reflect the human evaluation input to Voyager's Critic to Actor.

## Installation
Voyager requires Python ≥ 3.9 and Node.js ≥ 16.13.0. I have tested on Windows 11.

### Python Install
```
git clone https://github.com/tomomimu12345/ModifiedCreativeAgents
cd Voyager
pip install -e .
pip install langchain-community langchain-core langchain-google-genai chromadb
pip install -U langchain-community langchain-chroma
```

### Node.js Install
```
cd voyager_creative/env/mineflayer
npm install -g npx
npm install
cd mineflayer-collectblock
npx tsc
cd ..
npm install
```
## Minecraft Instance Install

Voyager depends on Minecraft game. You need to install Minecraft game and set up a Minecraft instance.

Follow the instructions in [Minecraft Login Tutorial](https://github.com/MineDojo/Voyager/blob/main/installation/minecraft_instance_install.md) to set up your Minecraft Instance.

## Fabric Mods Install

You need to install fabric mods to support all the features in Voyager. Remember to use the correct Fabric version of all the mods. 

Follow the instructions in [Fabric Mods Install](https://github.com/MineDojo/Voyager/blob/main/installation/fabric_mods_install.md) to install the mods.

## API KEY
Create a `.env` file in the root of your project and add the following variables:

| Variable Name                   | Description                                        |
|--------------------------------|----------------------------------------------------|
| `OPENAI_API_KEY`                | Your OpenAI API key (if required).                  |
| `GOOGLE_API_KEY`                | Your Google API key (if required).                  |

## Get Started
### text to build
```
python cot_gpt4.py --model_name gemini-2.0-flash-thinking-exp-01-21 --task "create a beautiful building" --mc_port 50070
```
### image to build
```
python diffusion_gpt4v.py --model_name gemini-2.0-flash-thinking-exp-01-21 --vision_model_name gemini-2.0-flash-thinking-exp-01-21 --image_path image1.png --mc_port 50070
```

## Acknowledgement
- [CreativeAgents](https://github.com/PKU-RL/Creative-Agents)