# Event Scheduling Python Agent

An intelligent AI-powered scheduling assistant that helps you manage events, meetings, tasks, and calendar activities using natural language processing.

## 🚀 Features

- **Smart Event Scheduling**: Schedule meetings and events using natural language
- **Task Management**: Create, prioritize, and track tasks with due dates
- **Calendar Integration**: View and manage your schedule efficiently
- **Natural Language Processing**: Interact with the agent using everyday language
- **Memory System**: Maintains conversation context for better assistance
- **Time Slot Finding**: Automatically find available time slots for meetings
- **Flexible Time Parsing**: Supports various time formats and relative dates

## 🏗️ Architecture

The project follows a modular architecture with the following components:

- **`src/agent.py`**: Main scheduling agent with conversation handling
- **`src/memory.py`**: Conversation memory management system
- **`src/tools/`**: Specialized tools for calendar, tasks, and scheduling
- **`src/utils.py`**: Utility functions and helpers
- **`scheduling_agent_simple.py`**: Standalone implementation for quick testing

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Virtual environment (recommended)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Event_Scheduling_python
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-3.5-turbo
   ```

## 🚀 Quick Start

### Option 1: Run the Demo
```bash
python examples/schedule_demo.py
```

### Option 2: Use the Simple Agent
```bash
python scheduling_agent_simple.py
```

### Option 3: Import and Use in Your Code
```python
from src.agent import SchedulingAgent

# Initialize the agent
agent = SchedulingAgent()

# Start scheduling!
response = agent.chat("Schedule a meeting called 'Team Standup' at 9 AM tomorrow")
print(response)
```

## 💬 Usage Examples

The scheduling agent understands natural language commands:

### Scheduling Events
- "Schedule a meeting called 'Project Review' at 3 PM today"
- "Book an appointment for 'Dentist' tomorrow at 2:30 PM"
- "Create an event called 'Team Lunch' on Friday at noon"

### Managing Tasks
- "Add a task called 'Finish report' with high priority"
- "Create a reminder to 'Call client' due tomorrow"
- "Set a task 'Review code' for next week"

### Viewing Information
- "Show me my events for today"
- "What tasks do I have pending?"
- "Display my schedule for this week"
- "Find available time for a 1-hour meeting tomorrow"

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: AI model to use (default: gpt-3.5-turbo)

### Data Storage
- Events and tasks are stored in `data/schedule.json`
- The system automatically creates the data directory if it doesn't exist

## 📁 Project Structure

```
Event_Scheduling_python/
├── config/
│   └── settings.py          # Configuration settings
├── data/
│   └── schedule.json        # Data storage
├── examples/
│   └── schedule_demo.py     # Interactive demo
├── src/
│   ├── agent.py            # Main scheduling agent
│   ├── memory.py           # Conversation memory
│   ├── tools/              # Specialized tools
│   │   ├── calender_tools.py
│   │   ├── scheduling_tools.py
│   │   └── task_tools.py
│   └── utils.py            # Utility functions
├── scheduling_agent_simple.py  # Standalone implementation
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🧪 Testing

Run the demo to test the system:
```bash
python examples/schedule_demo.py
```

The demo provides interactive examples and allows you to test various scheduling scenarios.

## 🔍 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure your `.env` file contains the correct API key
   - Verify the API key has sufficient credits

2. **Import Errors**
   - Make sure you're running from the project root directory
   - Ensure all dependencies are installed

3. **Data File Issues**
   - The system will automatically create the data directory
   - Check file permissions if you encounter write errors

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with OpenAI's GPT models for natural language understanding
- Uses python-dateutil for flexible time parsing
- Inspired by modern AI-powered productivity tools

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the example code in `examples/schedule_demo.py`
3. Open an issue on the repository

---

**Happy Scheduling! 📅✨**
