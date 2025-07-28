import os
import json
import google.generativeai as genai
from datetime import datetime


# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# File to store command history
LOG_FILE = "/home/ajayverma/Documents/test/tools/command_history_log.jsonl"

def explain_command(command):
    """
    Uses Gemini API to generate a brief natural-language explanation of a shell command.
    
    Args:
        command (str): The shell command string.

    Returns:
        str: A plain English explanation of what the command does.
    """
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(
            f"Explain this Linux shell command in one or two sentences: {command}"
        )
        return response.text.strip()
    except Exception as e:
        return f"Explanation failed: {str(e)}"

def command_exists(cmd):
    """
    Checks whether the given command already exists in the history log.

    Args:
        cmd (str): The command to check.

    Returns:
        bool: True if the command exists, False otherwise.
    """
    if not os.path.exists(LOG_FILE):
        return False
    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("command") == cmd:
                    return True
            except Exception:
                continue
    return False

def save_command(cmd):
    """
    Saves a command to the log file if it hasn't already been logged.

    Args:
        cmd (str): The shell command to save.
    """
    if command_exists(cmd):
        return  # Skip duplicate
    explanation = explain_command(cmd)
    with open(LOG_FILE, "a") as f:
        f.write(
            json.dumps({
                "timestamp": datetime.now().isoformat(),
                "command": cmd,
                "description": explanation
            }) + "\n"
        )

if __name__ == "__main__":
    # Entry point when script is called via shell hook
    command = os.environ.get("LAST_SUCCESS_CMD")
    if command:
        save_command(command)
