"""
PyPal - Advanced Python Chatbot with GUI
========================================

PORTFOLIO PROJECT: GUI Chatbot with Name Memory and Conversation Logging

HOW TO RUN:
1. Make sure you have Python installed (Python 3.6 or higher)
2. Save this file as 'pypal_chatbot.py'
3. Open your terminal/command prompt
4. Navigate to the folder containing this file
5. Run: python pypal_chatbot.py
6. The GUI window will open - start chatting with PyPal!

FEATURES:
- Clean GUI interface using tkinter
- Remembers your name throughout the session
- Responds to greetings, time requests, and casual conversation
- Logs all conversations to a file with timestamps
- Scrollable chat window
- Random response variations for natural conversation
- Professional code structure with clear functions

REQUIREMENTS:
- Python 3.6+ (tkinter comes built-in)
- No external libraries needed for basic functionality
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import datetime
import random
import os

class PyPalChatbot:
    def __init__(self):
        """
        Initialize the PyPal chatbot with GUI and core variables
        """
        # Chatbot personality
        self.bot_name = "PyPal"
        self.user_name = None
        self.conversation_started = False
        
        # Set up the main window
        self.setup_gui()
        
        # Create log file for conversation history
        self.setup_logging()
        
        # Start the conversation
        self.start_conversation()
    
    def setup_gui(self):
        """
        Create and configure the GUI interface
        """
        # Main window setup
        self.root = tk.Tk()
        self.root.title(f"{self.bot_name} - Your Friendly AI Assistant")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # Make window resizable
        self.root.resizable(True, True)
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title label
        title_label = tk.Label(
            main_frame, 
            text=f"🤖 {self.bot_name} - AI Chatbot Assistant",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 10))
        
        # Chat display area (scrollable)
        self.chat_display = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=('Arial', 10),
            bg='white',
            fg='black',
            state=tk.DISABLED,  # Make it read-only
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg='#f0f0f0')
        input_frame.pack(fill=tk.X, pady=(0, 5))
        
        # User input field
        self.user_input = tk.Entry(
            input_frame,
            font=('Arial', 11),
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Send button
        self.send_button = tk.Button(
            input_frame,
            text="Send 📤",
            command=self.handle_send,
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            relief=tk.RAISED,
            borderwidth=2,
            cursor='hand2'
        )
        self.send_button.pack(side=tk.RIGHT)
        
        # Bind Enter key to send message
        self.user_input.bind('<Return>', lambda event: self.handle_send())
        
        # Status bar
        self.status_label = tk.Label(
            main_frame,
            text="Ready to chat! Type your message above and press Enter or click Send.",
            font=('Arial', 9),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        self.status_label.pack(pady=(5, 0))
        
        # Focus on input field
        self.user_input.focus()
    
    def setup_logging(self):
        """
        Set up conversation logging to file
        """
        # Create logs directory if it doesn't exist
        if not os.path.exists('chat_logs'):
            os.makedirs('chat_logs')
        
        # Create log filename with current date
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.log_filename = f"chat_logs/pypal_conversation_{current_date}.log"
        
        # Write session start to log
        self.log_message("SYSTEM", f"{self.bot_name} chatbot session started")
    
    def log_message(self, sender, message):
        """
        Log a message to the conversation file with timestamp
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {sender}: {message}\n"
        
        try:
            with open(self.log_filename, 'a', encoding='utf-8') as log_file:
                log_file.write(log_entry)
        except Exception as e:
            print(f"Error logging message: {e}")
    
    def display_message(self, sender, message, color='black'):
        """
        Display a message in the chat window
        """
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        # Format message with sender and timestamp
        if sender == self.bot_name:
            formatted_message = f"🤖 {sender} [{timestamp}]: {message}\n\n"
        else:
            formatted_message = f"👤 {sender} [{timestamp}]: {message}\n\n"
        
        # Insert message
        self.chat_display.insert(tk.END, formatted_message)
        
        # Auto-scroll to bottom
        self.chat_display.see(tk.END)
        
        # Make read-only again
        self.chat_display.config(state=tk.DISABLED)
    
    def start_conversation(self):
        """
        Initialize the conversation with a welcome message
        """
        welcome_messages = [
            f"Hello! I'm {self.bot_name}, your friendly AI assistant! 😊",
            f"Hi there! {self.bot_name} here, ready to help and chat!",
            f"Welcome! I'm {self.bot_name}, your personal chatbot companion!"
        ]
        
        welcome = random.choice(welcome_messages)
        name_request = "What's your name? I'd love to get to know you better!"
        
        full_welcome = f"{welcome}\n{name_request}"
        
        self.display_message(self.bot_name, full_welcome)
        self.log_message(self.bot_name, full_welcome)
    
    def handle_send(self):
        """
        Handle user input when Send button is clicked or Enter is pressed
        """
        user_message = self.user_input.get().strip()
        
        # Handle empty input
        if not user_message:
            messagebox.showwarning("Empty Message", "Please type a message before sending!")
            return
        
        # Display user message
        display_name = self.user_name if self.user_name else "You"
        self.display_message(display_name, user_message)
        self.log_message(display_name, user_message)
        
        # Generate and display bot response
        response = self.generate_response(user_message)
        self.display_message(self.bot_name, response)
        self.log_message(self.bot_name, response)
        
        # Clear input field and focus
        self.user_input.delete(0, tk.END)
        self.user_input.focus()
        
        # Update status
        self.status_label.config(text=f"Last message sent at {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    def get_current_time(self):
        """
        Returns the current time in a friendly format
        """
        now = datetime.datetime.now()
        return now.strftime("It's currently %I:%M %p on %B %d, %Y")
    
    def detect_greeting(self, user_input):
        """
        Checks if the user's input contains a greeting
        """
        greetings = ['hi', 'hello', 'hey', 'hiya', 'good morning', 'good afternoon', 'good evening', 'sup', 'yo']
        user_input_lower = user_input.lower()
        
        return any(greeting in user_input_lower for greeting in greetings)
    
    def detect_how_are_you(self, user_input):
        """
        Checks if the user is asking how the bot is doing
        """
        how_are_you_phrases = ['how are you', 'how do you do', 'how are things', 'how\'s it going', 'how you doing']
        user_input_lower = user_input.lower()
        
        return any(phrase in user_input_lower for phrase in how_are_you_phrases)
    
    def detect_time_request(self, user_input):
        """
        Checks if the user is asking for the current time
        """
        time_keywords = ['time', 'clock', 'what time is it', 'current time', 'time is it', 'what time']
        user_input_lower = user_input.lower()
        
        return any(keyword in user_input_lower for keyword in time_keywords)
    
    def detect_goodbye(self, user_input):
        """
        Checks if the user wants to end the conversation
        """
        goodbye_phrases = ['bye', 'goodbye', 'see you', 'farewell', 'exit', 'quit', 'stop', 'close', 'end']
        user_input_lower = user_input.lower().strip()
        
        return any(phrase in user_input_lower for phrase in goodbye_phrases)
    
    def detect_name_in_message(self, user_input):
        """
        Try to extract a name from the user's message
        Simple approach: assume single word names or first word after common phrases
        """
        user_input = user_input.strip()
        
        # Common patterns for name introduction
        name_patterns = [
            "my name is", "i'm", "i am", "call me", "name's", "i go by"
        ]
        
        user_lower = user_input.lower()
        
        for pattern in name_patterns:
            if pattern in user_lower:
                # Find the pattern and extract what comes after
                start_idx = user_lower.find(pattern) + len(pattern)
                name_part = user_input[start_idx:].strip()
                if name_part:
                    # Take first word as name (simple approach)
                    potential_name = name_part.split()[0].strip('.,!?')
                    if potential_name.isalpha():
                        return potential_name.title()
        
        # If no pattern found, assume the whole message might be a name (if it's short and alphabetic)
        if len(user_input.split()) <= 2 and user_input.replace(' ', '').isalpha():
            return user_input.title()
        
        return None
    
    def generate_response(self, user_input):
        """
        Main function that determines what response to give based on user input
        """
        # Handle name collection on first interaction
        if not self.user_name and not self.conversation_started:
            potential_name = self.detect_name_in_message(user_input)
            if potential_name:
                self.user_name = potential_name
                self.conversation_started = True
                name_responses = [
                    f"Nice to meet you, {self.user_name}! 😊 How can I help you today?",
                    f"Great to meet you, {self.user_name}! I'm excited to chat with you!",
                    f"Hello {self.user_name}! What a lovely name. What would you like to talk about?",
                    f"Wonderful, {self.user_name}! Thanks for introducing yourself. How are you doing today?"
                ]
                return random.choice(name_responses)
            else:
                self.conversation_started = True
                return "I didn't quite catch your name there. That's okay though! What would you like to chat about? You can always tell me your name later! 😊"
        
        # Check for goodbye (highest priority)
        if self.detect_goodbye(user_input):
            goodbye_responses = [
                f"Goodbye{', ' + self.user_name if self.user_name else ''}! It was wonderful chatting with you! 👋",
                f"See you later{', ' + self.user_name if self.user_name else ''}! Have a fantastic day! 😊",
                f"Bye{', ' + self.user_name if self.user_name else ''}! Thanks for the great conversation!",
                f"Take care{', ' + self.user_name if self.user_name else ''}! Chat with me again anytime!"
            ]
            # Note: In a real app, you might want to close the window or disable input here
            return random.choice(goodbye_responses)
        
        # Check for time request
        elif self.detect_time_request(user_input):
            time_responses = [
                self.get_current_time(),
                f"{self.get_current_time()} ⏰",
                f"Sure thing{', ' + self.user_name if self.user_name else ''}! {self.get_current_time()}"
            ]
            return random.choice(time_responses)
        
        # Check for greetings
        elif self.detect_greeting(user_input):
            if self.user_name:
                greeting_responses = [
                    f"Hello again, {self.user_name}! How can I help you? 😊",
                    f"Hi {self.user_name}! Great to hear from you!",
                    f"Hey there, {self.user_name}! What's on your mind?",
                    f"Hello {self.user_name}! How are you doing today?"
                ]
            else:
                greeting_responses = [
                    "Hello there! How can I help you today? 😊",
                    "Hi! Great to meet you! What's on your mind?",
                    "Hey! I'm here and ready to chat!",
                    "Hello! How are you doing today?"
                ]
            return random.choice(greeting_responses)
        
        # Check for "how are you" questions
        elif self.detect_how_are_you(user_input):
            how_are_you_responses = [
                f"I'm doing great, thank you for asking{', ' + self.user_name if self.user_name else ''}! How are you?",
                f"I'm wonderful{', ' + self.user_name if self.user_name else ''}! Thanks for checking in. How about you?",
                f"I'm having a fantastic day{', ' + self.user_name if self.user_name else ''}! How are things with you?",
                f"I'm doing well{', ' + self.user_name if self.user_name else ''}! Ready to help with whatever you need!"
            ]
            return random.choice(how_are_you_responses)
        
        # Default response for unrecognized input
        else:
            if self.user_name:
                default_responses = [
                    f"That's interesting, {self.user_name}! Tell me more about that.",
                    f"I'm not sure I understand, {self.user_name}, but I'm here to listen!",
                    f"Hmm, {self.user_name}, I'd love to learn more about what you mean.",
                    f"I'm still learning, {self.user_name}! Can you try asking in a different way?",
                    f"That's cool, {self.user_name}! What else would you like to talk about?",
                    f"I'm here to chat, {self.user_name}! Try asking me about the time, or just say hello!"
                ]
            else:
                default_responses = [
                    "That's interesting! Tell me more about that.",
                    "I'm not sure I understand, but I'm here to listen!",
                    "Hmm, I'd love to learn more about what you mean.",
                    "I'm still learning! Can you try asking in a different way?",
                    "That's cool! What else would you like to talk about?",
                    "I'm here to chat! Try asking me about the time, or just say hello!"
                ]
            return random.choice(default_responses)
    
    def run(self):
        """
        Start the GUI application
        """
        # Handle window closing
        def on_closing():
            if messagebox.askokcancel("Quit", f"Do you want to quit {self.bot_name}?"):
                self.log_message("SYSTEM", f"{self.bot_name} chatbot session ended")
                self.root.destroy()
        
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Start the GUI main loop
        self.root.mainloop()

def main():
    """
    Main function to start the PyPal chatbot
    """
    print("🤖 Starting PyPal Chatbot GUI...")
    print("📝 Conversation logging enabled")
    print("🚀 Launching interface...")
    
    # Create and run the chatbot
    chatbot = PyPalChatbot()
    chatbot.run()

# Run the application
if __name__ == "__main__":
    main()

"""
FUTURE ENHANCEMENTS AND NLP UPGRADES:
=====================================

🔬 NATURAL LANGUAGE PROCESSING UPGRADES:

1. **NLTK Integration** (Natural Language Toolkit):
   ```bash
   pip install nltk
   ```
   
   Enhancements you could add:
   - **Sentiment Analysis**: Detect if user is happy, sad, angry
   - **Named Entity Recognition**: Better name detection
   - **Stemming/Lemmatization**: Handle word variations (run, running, ran)
   - **Part-of-Speech Tagging**: Understand grammar structure
   
   Example NLTK implementation:
   ```python
   import nltk
   from nltk.sentiment import SentimentIntensityAnalyzer
   
   # Download required NLTK data
   nltk.download('vader_lexicon')
   
   # Initialize sentiment analyzer
   sia = SentimentIntensityAnalyzer()
   
   def analyze_sentiment(text):
       scores = sia.polarity_scores(text)
       return scores['compound']  # Returns -1 (negative) to 1 (positive)
   ```

2. **spaCy Integration** (Industrial-strength NLP):
   ```bash
   pip install spacy
   python -m spacy download en_core_web_sm
   ```
   
   Advanced features:
   - **Better Named Entity Recognition**
   - **Dependency parsing**
   - **Advanced tokenization**
   - **Multiple language support**
   
   Example spaCy usage:
   ```python
   import spacy
   
   nlp = spacy.load("en_core_web_sm")
   
   def extract_entities(text):
       doc = nlp(text)
       return [(ent.text, ent.label_) for ent in doc.ents]
   ```

3. **HuggingFace Transformers** (State-of-the-art AI):
   ```bash
   pip install transformers torch
   ```
   
   For truly intelligent responses:
   ```python
   from transformers import pipeline, Conversation
   
   # Initialize conversational AI
   chatbot_pipeline = pipeline("conversational", 
                              model="microsoft/DialoGPT-medium")
   
   def get_ai_response(user_input, conversation_history):
       conversation = Conversation(user_input)
       conversation = chatbot_pipeline(conversation)
       return conversation.generated_responses[-1]
   ```

🚀 OTHER ADVANCED FEATURES TO ADD:

4. **Database Integration** (SQLite for persistence):
   ```python
   import sqlite3
   
   # Store user preferences, conversation history, learned information
   def setup_database():
       conn = sqlite3.connect('pypal_memory.db')
       # Create tables for users, conversations, preferences
   ```

5. **Web Integration**:
   - Weather API integration
   - News feeds
   - Wikipedia searches
   - Calculator functions

6. **Voice Capabilities**:
   ```bash
   pip install pyttsx3 speech_recognition
   ```
   
   Add text-to-speech and speech-to-text functionality

7. **Advanced GUI Features**:
   - Custom themes and colors
   - Emoji reactions
   - File sharing capabilities
   - Settings panel
   - Multiple chat tabs

8. **Machine Learning Personalization**:
   - Learn user preferences over time
   - Adapt conversation style
   - Remember important information

📚 LEARNING RESOURCES:
- NLTK Book: https://www.nltk.org/book/
- spaCy Documentation: https://spacy.io/usage
- HuggingFace Course: https://huggingface.co/course
- Tkinter GUI Programming: https://docs.python.org/3/library/tkinter.html

🎯 PORTFOLIO ENHANCEMENT TIPS:
- Add unit tests for your functions
- Create proper documentation
- Implement error handling and logging
- Add configuration files for easy customization
- Create a proper README.md with screenshots
- Consider packaging as a standalone executable with PyInstaller
"""
