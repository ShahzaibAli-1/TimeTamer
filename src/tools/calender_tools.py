import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pytz
from dateutil import parser

class CalendarManager:
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
    
    def add_event(self, title: str, start_time: str, end_time: Optional[str] = None, 
                 description: str = "", location: str = "") -> str:
        """Add a new event to the calendar"""
        try:
            start_dt = parser.parse(start_time)
            end_dt = parser.parse(end_time) if end_time else start_dt + timedelta(hours=1)
            
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
        """Get events for a specific date or all events"""
        try:
            if date:
                target_date = parser.parse(date).date()
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
                    f"{event['title']}: {start.strftime('%Y-%m-%d %H:%M')} to {end.strftime('%H:%M')}"
                )
            
            return "\n".join(result)
            
        except Exception as e:
            return f"Error retrieving events: {str(e)}"
    
    def remove_event(self, event_id: int) -> str:
        """Remove an event by ID"""
        original_count = len(self.schedule["events"])
        self.schedule["events"] = [e for e in self.schedule["events"] if e["id"] != event_id]
        
        if len(self.schedule["events"]) < original_count:
            self._save_schedule()
            return f"Event {event_id} removed successfully."
        else:
            return f"Event {event_id} not found."