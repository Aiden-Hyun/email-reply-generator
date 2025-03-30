# Email Reply Generator

A simple GUI application that uses OpenAI's GPT models to generate email replies in different tones.

## Features

- Input any email text
- Choose from multiple tones (formal, casual, friendly, professional, enthusiastic)
- Generate AI-powered email replies
- Copy replies to clipboard with one click

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/email-reply-generator.git
   cd email-reply-generator
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the application:
```
python email_reply_generator.py
```

1. Enter the email text you want to reply to in the "Original Email" section
2. Select the desired tone from the dropdown menu
3. Click "Generate Reply"
4. The AI-generated response will appear in the "Generated Reply" section
5. Click "Copy to Clipboard" to copy the reply

## Requirements

- Python 3.6 or higher
- OpenAI API key
- Packages listed in requirements.txt

## License

MIT

## Acknowledgements

This project uses the OpenAI API to generate email replies.
