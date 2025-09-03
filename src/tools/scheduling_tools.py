from datetime import datetime, timedelta
from typing import List, Dict, Any
from dateutil import parser

class SchedulingTools:
    @staticmethod
    def find_available_time(events: List[Dict[str, Any]], duration_hours: float = 1, 
                          start_date: str = None, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """Find available time slots"""
        try:
            if start_date:
                start_dt = parser.parse(start_date)
            else:
                start_dt = datetime.now()
            
            end_dt = start_dt + timedelta(days=days_ahead)
            duration = timedelta(hours=duration_hours)
            
            # Convert events to datetime objects
            busy_slots = []
            for event in events:
                busy_start = parser.parse(event["start_time"])
                busy_end = parser.parse(event["end_time"])
                busy_slots.append((busy_start, busy_end))
            
            # Find available slots
            available_slots = []
            current_time = start_dt.replace(hour=9, minute=0, second=0)  # Start at 9 AM
            
            while current_time.date() <= end_dt.date():
                # Check if current day is weekend (optional)
                if current_time.weekday() < 5:  # Monday-Friday
                    # Check business hours (9 AM - 5 PM)
                    if 9 <= current_time.hour < 17:
                        slot_end = current_time + duration
                        
                        # Check if slot overlaps with any busy time
                        is_available = True
                        for busy_start, busy_end in busy_slots:
                            if not (slot_end <= busy_start or current_time >= busy_end):
                                is_available = False
                                break
                        
                        if is_available and slot_end.hour <= 17:  # Within business hours
                            available_slots.append({
                                "start": current_time.isoformat(),
                                "end": slot_end.isoformat()
                            })
                
                current_time += timedelta(minutes=30)  # Check every 30 minutes
            
            return available_slots[:10]  # Return first 10 available slots
            
        except Exception as e:
            return f"Error finding available time: {str(e)}"
    
    @staticmethod
    def suggest_meeting_time(events: List[Dict[str, Any]], duration_hours: float = 1) -> str:
        """Suggest the next available meeting time"""
        available_slots = SchedulingTools.find_available_time(events, duration_hours)
        
        if available_slots:
            first_slot = available_slots[0]
            start_time = parser.parse(first_slot["start"])
            return f"Next available slot: {start_time.strftime('%Y-%m-%d %H:%M')}"
        else:
            return "No available slots found in the next 7 days."