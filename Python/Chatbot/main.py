import re
import random
import time

class Chatbot:
    def __init__(self):
        self.context = {}
        self.mode = "standard"  # standard, support
        
        self.responses = {
            r'hello|hi|hey': ["Hello there!", "Hi! How can I help?", "Greetings!"],
            r'how are you': ["I'm just a script, but I'm running perfectly!", "Doing well, thanks for asking.", "System status: Nominal."],
            r'bye|exit|quit': ["Goodbye!", "See you later!", "Shutting down..."],
            r'your name': ["I am PyBot v1.0.", "Call me PyBot.", "I don't have a name, but you can call me Bot."],
            r'help': ["I can chat with you or help with basic tech support. Type 'support' to switch modes.", "Try asking me about myself!"]
        }
        
        self.support_responses = {
            r'slow|lag': ["Have you tried restarting your device?", "Check your internet connection.", "Close unused background applications."],
            r'crash|error': ["What is the error code?", "Try reinstalling the application.", "Check the logs for more details."],
            r'password|login': ["Click 'Forgot Password' to reset it.", "Ensure Caps Lock is off.", "Contact your admin if locked out."],
            r'exit|back': ["Exiting support mode.", "Returning to standard chat."]
        }

    def get_response(self, user_input):
        user_input = user_input.lower()
        
        # Mode Switching
        if self.mode == "standard":
            if "support" in user_input:
                self.mode = "support"
                return "Switching to Tech Support Mode. What seems to be the problem? (Type 'back' to exit)"
        elif self.mode == "support":
            if "back" in user_input or "exit" in user_input:
                self.mode = "standard"
                return "Returning to Standard Mode. How can I help?"

        # Response Matching
        current_responses = self.support_responses if self.mode == "support" else self.responses
        
        for pattern, replies in current_responses.items():
            if re.search(pattern, user_input):
                return random.choice(replies)
        
        return "I'm not sure I understand. Could you rephrase that?"

def main():
    bot = Chatbot()
    print("🤖 PyBot Online. Type 'bye' to exit.")
    print("Tip: Type 'support' for tech help.")
    
    while True:
        user_input = input("\nYou: ")
        if not user_input:
            continue
            
        response = bot.get_response(user_input)
        
        print(f"Bot: {response}")
        
        if re.search(r'bye|exit|quit', user_input.lower()) and bot.mode == "standard":
            break
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()
