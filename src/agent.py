import sys
import os
from typing import Dict, List, Any, Optional
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Import tools
from src.tools import CalendarManager, TaskManager, SchedulingTools
from src.memory import ConversationMemory
from src.utils import validate_response, retryable_api_call, format_messages

class SchedulingAgent:
    def __init__(self, system_prompt: Optional[str] = None):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL
        self.memory = ConversationMemory()
        self.calendar = CalendarManager()
        self.task_manager = TaskManager()
        
        # Enhanced system prompt for scheduling
        self.system_prompt = system_prompt or """You are a scheduling assistant. You can:
        - Schedule events and meetings
        - Manage tasks with priorities and due dates
        - Find available time slots
        - View calendar events and tasks
        - Suggest meeting times
        
        Always be helpful and proactive in managing schedules."""
        
        self.memory.add_message("system", self.system_prompt)
    
    def chat(self, user_input: str) -> str:
        """Process user input with scheduling capabilities"""
        self.memory.add_message("user", user_input)
        messages = self.memory.get_conversation_history()
        
        # Check for scheduling commands
        tool_response = self._handle_scheduling_commands(user_input)
        
        if tool_response:
            # Add tool response to context and generate final response
            self.memory.add_message("assistant", f"I handled your scheduling request: {tool_response}")
            messages = self.memory.get_conversation_history()
        
        # Generate final response
        final_response = self._generate_response(messages)
        self.memory.add_message("assistant", final_response)
        
        return final_response
    
    def _handle_scheduling_commands(self, user_input: str) -> Optional[str]:
        """Handle scheduling-related commands"""
        input_lower = user_input.lower()
        
        # Schedule event patterns
        if any(word in input_lower for word in ['schedule', 'meeting', 'appointment', 'event', 'calendar']):
            return self._handle_calendar_commands(user_input)
        
        # Task patterns
        elif any(word in input_lower for word in ['task', 'todo', 'reminder', 'due']):
            return self._handle_task_commands(user_input)
        
        # View patterns
        elif any(word in input_lower for word in ['show', 'view', 'list', 'get', 'what\'s on']):
            return self._handle_view_commands(user_input)
        
        return None
    
    def _handle_calendar_commands(self, user_input: str) -> str:
        """Handle calendar-related commands"""
        try:
            # Extract event details using simple pattern matching
            # In a real implementation, you'd use more sophisticated NLP
            patterns = {
                'title': r'(?:schedule|meeting|appointment|event) (?:called|named|for) ["\']?([^"\']+)["\']?',
                'time': r'(?:at|on) (.*?)(?:\.|$|for|with)',
                'duration': r'(?:for|duration) (\d+) (?:hour|hr|minute|min)'
            }
            
            title_match = re.search(patterns['title'], user_input, re.IGNORECASE)
            time_match = re.search(patterns['time'], user_input, re.IGNORECASE)
            
            if title_match and time_match:
                title = title_match.group(1).strip()
                time_str = time_match.group(1).strip()
                
                # Add common time phrases if missing
                if not any(word in time_str for word in ['am', 'pm', 'today', 'tomorrow']):
                    time_str += " today"  # Default to today
                
                return self.calendar.add_event(title, time_str)
            
            elif 'show events' in user_input.lower() or 'view calendar' in user_input.lower():
                # Extract date if specified
                date_match = re.search(r'(?:on|for) (.*?)(?:\.|$|please)', user_input, re.IGNORECASE)
                date_str = date_match.group(1).strip() if date_match else None
                return self.calendar.get_events(date_str)
            
            elif 'available time' in user_input.lower() or 'free slot' in user_input.lower():
                events = self.calendar.schedule.get("events", [])
                available_slots = SchedulingTools.find_available_time(events)
                if available_slots:
                    return f"Available slots: {available_slots[:3]}"  # Show first 3
                else:
                    return "No available slots found."
            
        except Exception as e:
            return f"Error handling calendar command: {str(e)}"
        
        return ""
    
    def _handle_task_commands(self, user_input: str) -> str:
        """Handle task-related commands"""
        try:
            if 'add task' in user_input.lower() or 'create task' in user_input.lower():
                # Extract task details
                task_match = re.search(r'(?:add|create) task ["\']?([^"\']+)["\']?', user_input, re.IGNORECASE)
                if task_match:
                    title = task_match.group(1).strip()
                    return self.task_manager.add_task(title)
            
            elif 'show tasks' in user_input.lower() or 'list tasks' in user_input.lower():
                status_match = re.search(r'(?:with status|that are) (\w+)', user_input, re.IGNORECASE)
                status = status_match.group(1).strip() if status_match else None
                return self.task_manager.get_tasks(status)
            
        except Exception as e:
            return f"Error handling task command: {str(e)}"
        
        return ""
    
    def _handle_view_commands(self, user_input: str) -> str:
        """Handle view commands"""
        if 'events' in user_input.lower():
            return self.calendar.get_events()
        elif 'tasks' in user_input.lower():
            return self.task_manager.get_tasks()
        return ""
    
    def _generate_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate response using OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            if validate_response(response):
                return response.choices[0].message.content
            else:
                return "Sorry, I encountered an error processing your request."
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.memory.clear_memory()
        self.memory.add_message("system", self.system_prompt)
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.memory.get_conversation_history()