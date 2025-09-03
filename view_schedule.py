import json
import os
from datetime import datetime

def view_schedule():
    schedule_file = "data/schedule.json"
    
    if not os.path.exists(schedule_file):
        print("No schedule file found. Schedule some events first!")
        return
    
    try:
        with open(schedule_file, 'r') as f:
            schedule = json.load(f)
        
        print("📅 YOUR SCHEDULE")
        print("=" * 50)
        
        # Display Events
        print("\n🎯 EVENTS:")
        print("-" * 30)
        if schedule.get("events"):
            for event in schedule["events"]:
                start_time = datetime.fromisoformat(event["start_time"])
                end_time = datetime.fromisoformat(event["end_time"])
                print(f"• {event['title']}")
                print(f"  📅 {start_time.strftime('%Y-%m-%d')}")
                print(f"  ⏰ {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}")
                if event.get("description"):
                    print(f"  📝 {event['description']}")
                if event.get("location"):
                    print(f"  📍 {event['location']}")
                print()
        else:
            print("No events scheduled yet.")
        
        # Display Tasks
        print("\n✅ TASKS:")
        print("-" * 30)
        if schedule.get("tasks"):
            for task in schedule["tasks"]:
                status_emoji = "🟢" if task["status"] == "completed" else "🟡" if task["status"] == "in_progress" else "⚪"
                priority_emoji = "🔥" if task["priority"] == "high" else "⚠️" if task["priority"] == "medium" else "📌"
                
                print(f"{status_emoji} {priority_emoji} {task['title']}")
                print(f"   Status: {task['status']}")
                if task.get("due_date"):
                    due_date = datetime.fromisoformat(task["due_date"])
                    print(f"   Due: {due_date.strftime('%Y-%m-%d')}")
                if task.get("description"):
                    print(f"   Notes: {task['description']}")
                print()
        else:
            print("No tasks created yet.")
            
    except Exception as e:
        print(f"Error reading schedule: {e}")

if __name__ == "__main__":
    view_schedule()