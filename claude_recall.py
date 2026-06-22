import os
import json
from anthropic import Anthropic

# Load environment variables for API key
# Ensure you have ANTHROPIC_API_KEY set in your environment
# export ANTHROPIC_API_KEY='your-api-key'

client = Anthropic()

# Define the file to store conversation history (the 'recall' mechanism)
CONVERSATION_HISTORY_FILE = "claude_conversation_history.json"

def load_conversation_history():
    """Loads conversation history from a JSON file."""
    if os.path.exists(CONVERSATION_HISTORY_FILE):
        with open(CONVERSATION_HISTORY_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # Handle empty or corrupted file
                return []
    return []

def save_conversation_history(history):
    """Saves conversation history to a JSON file."""
    with open(CONVERSATION_HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def get_claude_response(user_input, conversation_history):
    """Gets a response from Claude, maintaining conversation context."""

    # Add user's message to the history
    conversation_history.append({"role": "user", "content": user_input})

    # Prepare messages for the API call, including the full history
    messages = conversation_history

    try:
        response = client.messages.create(
            model="claude-3-opus-20240229", # Or another suitable Claude model
            max_tokens=1000,
            messages=messages
        )

        # Extract Claude's response and add it to the history
        claude_message = response.content[0].text
        conversation_history.append({"role": "assistant", "content": claude_message})

        # Save the updated history to persist the conversation
        save_conversation_history(conversation_history)

        return claude_message

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Sorry, I encountered an error."

if __name__ == "__main__":
    print("Welcome to Claude's Persistent Conversation!")
    print("Type 'quit' or 'exit' to end the session.")

    # Load previous conversation history to maintain context
    current_history = load_conversation_history()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        # Get response from Claude, passing the entire conversation history
        claude_response = get_claude_response(user_input, current_history)
        print(f"Claude: {claude_response}")

    print("Session ended.")
