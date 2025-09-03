import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import SchedulingAgent

def main():
    # Initialize the scheduling agent
    agent = SchedulingAgent()
    
    print("📅 Scheduling Agent initialized!")
    print("I can help you with:")
    print("  • Scheduling events and meetings")
    print("  • Managing tasks and reminders")
    print("  • Finding available time slots")
    print("  • Viewing your calendar")
    print("\nType 'quit' to exit, 'clear' to clear conversation")
    print("-" * 60)
    
    # Demo examples
    demo_examples = [
        "Schedule a meeting called 'Project Review' at 3 PM today",
        "Add a task called 'Finish report' with high priority",
        "Show me my events for today",
        "What tasks do I have pending?",
        "Find available time for a 1-hour meeting tomorrow"
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
            
            # Get response from agent
            response = agent.chat(user_input)
            print(f"\n📅 Agent: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()