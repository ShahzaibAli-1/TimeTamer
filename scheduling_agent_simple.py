import os
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from openai import OpenAI
from dotenv import load_dotenv
from dateutil import parser

# Load environment variables
load_dotenv()

# Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Memory System
@dataclass
class Message:
    role: str
    content: str

class ConversationMemory:
    def __init__(self, max_messages: int = 20):
        self.messages: List[Message] = []
        self.max_messages = max_messages
    
    def add_message(self, role: str, content: str):
        message = Message(role=role, content=content)
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        return [{"role": msg.role, "content": msg.content} for msg in self.messages]
    
    def clear_memory(self):
        self.messages = []

# Calendar Manager with improved time parsing
class CalendarManager:
    def __init__(self, data_file: str = "data/schedule.json"):
        self.data_file = data_file
        self.schedule = self._load_schedule()
    
    def _load_schedule(self) -> Dict[str, Any]:
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return {"events": [], "tasks": []}
        return {"events": [], "tasks": []}
    
    def _save_schedule(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.schedule, f, indent=2)
    
    def _preprocess_time_string(self, time_str: str) -> str:
        """Preprocess natural language time strings for better parsing"""
        time_str = time_str.lower().strip()
        
        # Handle relative days
        if 'tomorrow' in time_str:
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            time_str = time_str.replace('tomorrow', tomorrow)
        elif 'today' in time_str:
            today = datetime.now().strftime('%Y-%m-%d')
            time_str = time_str.replace('today', today)
        
        # Handle time formats
        if 'pm' in time_str:
            time_str = time_str.replace('pm', '').strip() + ' PM'
        elif 'am' in time_str:
            time_str = time_str.replace('am', '').strip() + ' AM'
        
        # If no date specified, assume today
        if not any(char.isdigit() and len(part) == 4 for part in time_str.split() for char in part):
            # No year found, add today's date
            today = datetime.now().strftime('%Y-%m-%d ')
            time_str = today + time_str
        
        return time_str
    
    def add_event(self, title: str, start_time: str, end_time: Optional[str] = None, 
                 description: str = "", location: str = "") -> str:
        """Add a new event to the calendar with better natural language parsing"""
        try:
            # Preprocess the time string
            processed_time = self._preprocess_time_string(start_time)
            
            # Parse the processed time
            start_dt = parser.parse(processed_time)
            
            # Set end time (default to 1 hour later if not specified)
            if end_time:
                processed_end_time = self._preprocess_time_string(end_time)
                end_dt = parser.parse(processed_end_time)
            else:
                end_dt = start_dt + timedelta(hours=1)
            
            event = {
                "id": len(self.schedule["events"]) + 1,
                "title": title,
                "start_time": start_dt.isoformat(),
                "end_time": end_dt.isoformat(),
                "description": description,
                "location": location,
                "created_at": datetime.now().isoformat()
            }
            
            self.schedule["events"].append(event)
            self._save_schedule()
            
            return f"Event '{title}' scheduled for {start_dt.strftime('%Y-%m-%d %H:%M')}"
            
        except Exception as e:
            return f"Error adding event: {str(e)}"
    
    def get_events(self, date: Optional[str] = None) -> str:
        try:
            if date:
                processed_date = self._preprocess_time_string(date)
                target_date = parser.parse(processed_date).date()
                events = [
                    event for event in self.schedule["events"]
                    if parser.parse(event["start_time"]).date() == target_date
                ]
            else:
                events = self.schedule["events"]
            
            if not events:
                return "No events found."
            
            result = []
            for event in sorted(events, key=lambda x: x["start_time"]):
                start = parser.parse(event["start_time"])
                end = parser.parse(event["end_time"])
                result.append(
                    f"{event['id']}. {event['title']}: {start.strftime('%Y-%m-%d %H:%M')} to {end.strftime('%H:%M')}"
                )
            
            return "\n".join(result)
            
        except Exception as e:
            return f"Error retrieving events: {str(e)}"

# Task Manager (unchanged)
class TaskManager:
    def __init__(self, data_file: str = "data/schedule.json"):
        self.data_file = data_file
        self.schedule = self._load_schedule()
    
    def _load_schedule(self) -> Dict[str, Any]:
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return {"events": [], "tasks": []}
        return {"events": [], "tasks": []}
    
    def _save_schedule(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.schedule, f, indent=2)
    
    def add_task(self, title: str, due_date: Optional[str] = None, 
                priority: str = "medium", description: str = "") -> str:
        try:
            due_dt = parser.parse(due_date) if due_date else None
            
            task = {
                "id": len(self.schedule["tasks"]) + 1,
                "title": title,
                "due_date": due_dt.isoformat() if due_dt else None,
                "priority": priority,
                "description": description,
                "status": "pending",
                "created_at": datetime.now().isoformat()
            }
            
            self.schedule["tasks"].append(task)
            self._save_schedule()
            
            due_info = f" due {due_dt.strftime('%Y-%m-%d')}" if due_dt else ""
            return f"Task '{title}' added{due_info} with {priority} priority."
            
        except Exception as e:
            return f"Error adding task: {str(e)}"
    
    def get_tasks(self, status: Optional[str] = None) -> str:
        try:
            if status:
                tasks = [task for task in self.schedule["tasks"] if task["status"] == status]
            else:
                tasks = self.schedule["tasks"]
            
            if not tasks:
                return "No tasks found."
            
            result = []
            for task in tasks:
                due_info = f" (Due: {parser.parse(task['due_date']).strftime('%Y-%m-%d')})" if task["due_date"] else ""
                result.append(
                    f"{task['id']}. {task['title']} [{task['priority']}] - {task['status']}{due_info}"
                )
            
            return "\n".join(result)
            
        except Exception as e:
            return f"Error retrieving tasks: {str(e)}"

# Enhanced Scheduling Agent
class SchedulingAgent:
    def __init__(self, system_prompt: Optional[str] = None):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL
        self.memory = ConversationMemory()
        self.calendar = CalendarManager()
        self.task_manager = TaskManager()
        
        self.system_prompt = system_prompt or """You are a scheduling assistant. You can:
        - Schedule events and meetings
        - Manage tasks with priorities and due dates
        - Find available time slots
        - View calendar events and tasks
        - Suggest meeting times
        
        Always be helpful and proactive in managing schedules."""
        
        self.memory.add_message("system", self.system_prompt)
    
    def chat(self, user_input: str) -> str:
        self.memory.add_message("user", user_input)
        
        # Handle scheduling commands first
        tool_response = self._handle_scheduling_commands(user_input)
        
        if tool_response:
            # If we handled it with tools, use that response
            final_response = tool_response
        else:
            # Otherwise, use OpenAI
            messages = self.memory.get_conversation_history()
            final_response = self._generate_response(messages)
        
        self.memory.add_message("assistant", final_response)
        return final_response
    
    def _handle_scheduling_commands(self, user_input: str) -> Optional[str]:
        input_lower = user_input.lower()
        
        # Schedule event patterns
        if any(word in input_lower for word in ['schedule', 'meeting', 'appointment', 'event', 'calendar']):
            return self._handle_calendar_commands(user_input)
        
        # Task patterns
        elif any(word in input_lower for word in ['task', 'todo', 'reminder', 'due', 'add task']):
            return self._handle_task_commands(user_input)
        
        # View patterns
        elif any(word in input_lower for word in ['show', 'view', 'list', 'get', 'what\'s on', 'events', 'tasks']):
            return self._handle_view_commands(user_input)
        
        return None
    
    def _handle_calendar_commands(self, user_input: str) -> str:
        try:
            input_lower = user_input.lower()
            
            # Extract meeting details using improved pattern matching
            if 'schedule' in input_lower or 'meeting' in input_lower or 'appointment' in input_lower:
                # Extract title - look for phrases after schedule/meeting
                title_match = re.search(r'(?:schedule|meeting|appointment) (?:called|named|for|with|about) ["\']?([^"\']+)["\']?', input_lower)
                if not title_match:
                    # Alternative pattern for "schedule meeting with X at Y"
                    title_match = re.search(r'(?:schedule|meeting|appointment) (?:with|for) ([^\.]+?)(?:at|on|for|$)', input_lower)
                
                # Extract time
                time_match = re.search(r'(?:at|on) ([^\.]+?)(?:\.|$|for|with|about)', input_lower)
                
                # Extract participants
                participants = []
                people_match = re.findall(r'(?:with|meeting) (\w+)', input_lower)
                if people_match:
                    participants = [name.capitalize() for name in people_match if name not in ['at', 'on', 'for', 'about', 'schedule', 'meeting']]
                
                # Extract purpose/topic
                purpose_match = re.search(r'(?:about|regarding|related to) ([^\.]+)', input_lower)
                
                if time_match:
                    title = title_match.group(1).strip() if title_match else "Meeting"
                    time_str = time_match.group(1).strip()
                    
                    # Build description with participants and purpose
                    description_parts = []
                    if participants:
                        description_parts.append(f"Participants: {', '.join(participants)}")
                    if purpose_match:
                        purpose = purpose_match.group(1).strip()
                        description_parts.append(f"Topic: {purpose}")
                    
                    description = ". ".join(description_parts) if description_parts else ""
                    
                    return self.calendar.add_event(title, time_str, description=description)
                
            # View events
            elif 'show events' in input_lower or 'view calendar' in input_lower:
                date_match = re.search(r'(?:on|for) (.*?)(?:\.|$|please)', input_lower)
                date_str = date_match.group(1).strip() if date_match else None
                return self.calendar.get_events(date_str)
                
        except Exception as e:
            return f"Error handling calendar command: {str(e)}"
        
        return ""
    
    def _handle_task_commands(self, user_input: str) -> str:
        try:
            # Add task
            if 'add task' in user_input.lower() or 'create task' in user_input.lower():
                task_match = re.search(r'(?:add|create) task ["\']?([^"\']+)["\']?', user_input, re.IGNORECASE)
                if task_match:
                    title = task_match.group(1).strip()
                    return self.task_manager.add_task(title)
            
            # View tasks
            elif 'show tasks' in user_input.lower() or 'list tasks' in user_input.lower():
                status_match = re.search(r'(?:with status|that are) (\w+)', user_input, re.IGNORECASE)
                status = status_match.group(1).strip() if status_match else None
                return self.task_manager.get_tasks(status)
                
        except Exception as e:
            return f"Error handling task command: {str(e)}"
        
        return ""
    
    def _handle_view_commands(self, user_input: str) -> str:
        if 'events' in user_input.lower():
            return self.calendar.get_events()
        elif 'tasks' in user_input.lower():
            return self.task_manager.get_tasks()
        return ""
    
    def _generate_response(self, messages: List[Dict[str, str]]) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            if response and hasattr(response, 'choices') and len(response.choices) > 0:
                return response.choices[0].message.content
            else:
                return "Sorry, I encountered an error processing your request."
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear_conversation(self):
        self.memory.clear_memory()
        self.memory.add_message("system", self.system_prompt)
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        return self.memory.get_conversation_history()

# Main function
def main():
    agent = SchedulingAgent()
    
    print("📅 Scheduling Agent initialized!")
    print("I can help you with:")
    print("  • Scheduling events and meetings")
    print("  • Managing tasks and reminders")
    print("  • Viewing your calendar and tasks")
    print("\nType 'quit' to exit, 'clear' to clear conversation")
    print("-" * 60)
    
    # Demo examples
    demo_examples = [
        "Schedule a meeting called 'Project Review' at 3 PM tomorrow",
        "Schedule meeting with Ali and Ahmad at 4pm tomorrow about car service",
        "Add a task called 'Finish report'",
        "Show me my events",
        "What tasks do I have?"
    ]
    
    print("\nTry these examples:")
    for i, example in enumerate(demo_examples, 1):
        print(f"{i}. {example}")
    
    print("\n" + "-" * 60)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'clear':
                agent.clear_conversation()
                print("Conversation cleared.")
                continue
            elif user_input.lower() == 'examples':
                for i, example in enumerate(demo_examples, 1):
                    print(f"{i}. {example}")
                continue
            
            response = agent.chat(user_input)
            print(f"\n📅 Agent: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()