import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class EmailReplyGeneratorApp:
    """
    A GUI application for generating email replies using OpenAI's GPT models.
    This application allows users to input an email, select a tone, and generate
    a response in the selected tone using AI.
    """
    
    def __init__(self, root):
        """Initialize the application with UI components."""
        self.root = root
        self.root.title("Email Reply Generator")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Get API key from environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("No OpenAI API key found. Please set OPENAI_API_KEY in your .env file.")
        
        # Initialize OpenAI client
        self.openai = OpenAI(api_key=api_key)
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create UI elements
        self.create_input_section(main_frame)
        self.create_output_section(main_frame)
        self.create_controls(main_frame)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_input_section(self, parent):
        """Create the input section of the UI."""
        # Input section
        input_frame = ttk.LabelFrame(parent, text="Original Email", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Email content input
        self.email_input = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=10)
        self.email_input.pack(fill=tk.BOTH, expand=True)
        
        # Add some placeholder text
        placeholder = "Enter the email you want to reply to here..."
        self.email_input.insert(tk.END, placeholder)
        
        # Tone selection
        tone_frame = ttk.Frame(input_frame)
        tone_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(tone_frame, text="Reply Tone:").pack(side=tk.LEFT, padx=5)
        
        self.tone_var = tk.StringVar(value="formal")
        tones = ["formal", "casual", "friendly", "professional", "enthusiastic"]
        tone_combo = ttk.Combobox(tone_frame, textvariable=self.tone_var, values=tones, state="readonly", width=15)
        tone_combo.pack(side=tk.LEFT, padx=5)
    
    def create_output_section(self, parent):
        """Create the output section of the UI."""
        # Output section
        output_frame = ttk.LabelFrame(parent, text="Generated Reply", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Reply output
        self.reply_output = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=10)
        self.reply_output.pack(fill=tk.BOTH, expand=True)
        self.reply_output.config(state=tk.DISABLED)
    
    def create_controls(self, parent):
        """Create the control buttons."""
        # Control buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.generate_button = ttk.Button(button_frame, text="Generate Reply", command=self.generate_reply)
        self.generate_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        self.copy_button = ttk.Button(button_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack(side=tk.RIGHT, padx=5)
    
    def generate_reply(self):
        """Handle the generate reply button click."""
        email_content = self.email_input.get("1.0", tk.END).strip()
        tone = self.tone_var.get()
        
        if not email_content:
            self.status_var.set("Error: Please enter email content")
            return
        
        # Disable the generate button during processing
        self.generate_button.config(state=tk.DISABLED)
        self.status_var.set("Generating reply...")
        
        # Run the API call in a separate thread to avoid freezing the UI
        threading.Thread(target=self._process_reply, args=(email_content, tone)).start()
    
    def _process_reply(self, email_content, tone):
        """Process the reply generation in a separate thread."""
        try:
            reply = self.generate_email_reply(email_content, tone)
            
            # Update UI in the main thread
            self.root.after(0, self._update_reply, reply)
        except Exception as e:
            self.root.after(0, self._show_error, str(e))
    
    def _update_reply(self, reply):
        """Update the UI with the generated reply."""
        self.reply_output.config(state=tk.NORMAL)
        self.reply_output.delete("1.0", tk.END)
        self.reply_output.insert(tk.END, reply)
        self.reply_output.config(state=tk.DISABLED)
        self.generate_button.config(state=tk.NORMAL)
        self.status_var.set("Reply generated successfully")
    
    def _show_error(self, error_message):
        """Display an error message in the status bar."""
        self.status_var.set(f"Error: {error_message}")
        self.generate_button.config(state=tk.NORMAL)
    
    def generate_email_reply(self, email_content, tone='formal'):
        """
        Generate an email reply using OpenAI's API.
        
        Args:
            email_content (str): The original email content to respond to
            tone (str): The tone to use for the reply (default: 'formal')
            
        Returns:
            str: The generated email reply
        """
        system_prompt = f"Rephrase the following email in a {tone} tone."
        user_prompt = f"Email content: {email_content}"
        
        try:
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def clear_fields(self):
        """Clear all input and output fields."""
        self.email_input.delete("1.0", tk.END)
        self.reply_output.config(state=tk.NORMAL)
        self.reply_output.delete("1.0", tk.END)
        self.reply_output.config(state=tk.DISABLED)
        self.status_var.set("Fields cleared")
    
    def copy_to_clipboard(self):
        """Copy the generated reply to clipboard."""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.reply_output.get("1.0", tk.END))
        self.status_var.set("Copied to clipboard")


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = EmailReplyGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
