import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskManager:
    def __init__(self, data_file: str = "data/schedule.json"):
        self.data_file = data_file
        self.schedule = self._load_schedule()
    
    def _load_schedule(self) -> Dict[str, Any]:
        """Load schedule from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return {"events": [], "tasks": []}
        return {"events": [], "tasks": []}
    
    def _save_schedule(self):
        """Save schedule to JSON file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.schedule, f, indent=2)
    
    def add_task(self, title: str, due_date: Optional[str] = None, 
                priority: str = "medium", description: str = "") -> str:
        """Add a new task"""
        try:
            due_dt = parser.parse(due_date) if due_date else None
            
            task = {
                "id": len(self.schedule["tasks"]) + 1,
                "title": title,
                "due_date": due_dt.isoformat() if due_dt else None,
                "priority": priority,
                "description": description,
                "status": Status.PENDING.value,
                "created_at": datetime.now().isoformat()
            }
            
            self.schedule["tasks"].append(task)
            self._save_schedule()
            
            due_info = f" due {due_dt.strftime('%Y-%m-%d')}" if due_dt else ""
            return f"Task '{title}' added{due_info} with {priority} priority."
            
        except Exception as e:
            return f"Error adding task: {str(e)}"
    
    def get_tasks(self, status: Optional[str] = None) -> str:
        """Get tasks with optional status filter"""
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
    
    def update_task_status(self, task_id: int, status: str) -> str:
        """Update task status"""
        try:
            for task in self.schedule["tasks"]:
                if task["id"] == task_id:
                    task["status"] = status
                    self._save_schedule()
                    return f"Task {task_id} status updated to {status}."
            return f"Task {task_id} not found."
        except Exception as e:
            return f"Error updating task: {str(e)}"