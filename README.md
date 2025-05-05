# FrameTale

## LLM-Powered Storytelling Engine

FrameTale is a Python RPG engine that enhances LLM storytelling capabilities through the use of various tools. It provides structure and game mechanics that help LLMs maintain consistency while delivering interactive stories.

Built with custom tkinter for the UI, the program focuses on improving the narrative experience by handling elements that LLMs typically struggle with, such as maintaining consistent character traits, tracking game state, and managing inventory.

## 🌟 Features

### Current Features
- [X] **Basic Summarization**: Prevents context window overload by condensing previous interactions
- [X] **Player Statistics**: Track health, stamina, money, and other attributes
- [X] **Basic Inventory System**: Manage player items and possessions
- [X] **Dual-System Prompting**: 
  - [X] Initial setup prompt to establish the narrative framework
  - [X] Ongoing reminder prompt to maintain consistency with player stats
- [X] **Response Guidelines**: Output formats for quality storytelling
- [X] **Dialogue Assistance**: Tips for creating better character dialogue
- [X] **Typing Animation**: Text rendering that mimics natural typing
- [X] **OpenRouter API Integration**: Uses OpenRouter for LLM inference

### Planned Features
- [ ] **Templates**: Customizable templates for story settings and elements
- [ ] **Character Management**: Track NPCs, their motivations, personalities, and speech patterns
- [ ] **Enhanced Narrative Consistency**: Improved systems for coherent storylines
- [ ] **Advanced Time Management**: Sophisticated in-game time tracking with consequences
- [ ] **Response Validation**: Better checks for problematic LLM outputs
- [ ] **Character Formatting**: Colored and formatted text for different characters
- [ ] **Story Pacing**: Control narrative rhythm and dramatic tension
- [ ] **Multiple API Support**: Integration with various LLM providers
- [ ] **Local LLM Support**: Ability to use locally hosted language models
- [ ] **Image Generation**: Visual representations of environments and characters
- [ ] **Advanced RPG Elements**: More sophisticated game mechanics
- [ ] **Settings UI**: User interface for configuring system prompts and settings



## 🛠️ Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/benasraudys/frametale.git

# Navigate to the project directory
cd frametale

# Create a virtual environment (recommended)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Rename `.env.example` to `.env`
2. Edit the `.env` file and add your OpenRouter API key:

```
OPENROUTER_API_KEY=your_api_key_here
```

### Running FrameTale

```bash
python main.py
```
