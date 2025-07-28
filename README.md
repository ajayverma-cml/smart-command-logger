# 🧠 Smart Command Logger

A smart terminal tool that:

* 📜 Monitors **successfully executed shell commands**
* 🧠 Uses **Google Gemini** to generate natural-language explanations
* 📁 Saves unique commands to a JSONL log file with timestamps
* 🚫 Skips failed or duplicate commands automatically

---

## 📌 Purpose

This tool helps developers track and document useful terminal commands in real-time. It's like `bash history`, but with AI explanations and cleaner, deduplicated logs.

---

## 🔧 Setup

### 1. Clone the Script

Place the `command_logger.py` script anywhere, for example:

```bash
/home/ajayverma/Documents/test/tools/command_logger.py
```

Make sure it’s executable:

```bash
chmod +x /home/ajayverma/Documents/test/tools/command_logger.py
```

---

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv myenv
source myenv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Get Gemini API Key

* Go to: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
* Copy your API key
* Export it in your shell:

```bash
export GEMINI_API_KEY="your-key-here"
```

You can also add it to your `~/.bashrc` to persist:

```bash
echo 'export GEMINI_API_KEY="your-key-here"' >> ~/.bashrc
```

---

### 5. Add Shell Hooks

Edit your `~/.bashrc` and append the following:

```bash
# Hook to capture last successful command
function preexec() {
    export LAST_COMMAND=$(history 1 | sed 's/^[ ]*[0-9]\+[ ]*//')
}

function precmd() {
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        export LAST_SUCCESS_CMD="$LAST_COMMAND"
        PY_SCRIPT="/home/ajayverma/Documents/test/tools/command_logger.py"
        PY_BIN="/home/ajayverma/Documents/test/tools/myenv/bin/python"

        # Only run logger if the script exists
        if [ -f "$PY_SCRIPT" ]; then
            "$PY_BIN" "$PY_SCRIPT" > /dev/null 2>&1 &
            disown  # Prevent shell from tracking the job
        fi
    fi
}

# Set PROMPT_COMMAND to call precmd after every command
PROMPT_COMMAND='precmd;'
trap 'preexec' DEBUG
```

Then reload your shell:

```bash
source ~/.bashrc
```

---

## 📂 Output

* All logged commands are saved in:

  ```
  /home/ajayverma/Documents/test/tools/command_history_log.jsonl
  ```

* Each line is a JSON object like:

```json
{
  "timestamp": "2025-07-28T14:33:00",
  "command": "ls -la",
  "description": "Lists all files in the current directory, including hidden ones, in long format."
}
```

---

## 🚫 Duplicate Protection

* Commands are logged only once, using **exact string matching**.
* Repeated identical commands are skipped.

---

## 🔍 Example Use Case

1. Run some commands:

   ```bash
   ls -la
   cd /var/log
   cat syslog
   ```

2. View logged history:

   ```bash
   cat /home/ajayverma/Documents/test/tools/command_history_log.jsonl
   ```

3. Result:

   * Each successful and unique command is saved with a timestamp and AI-generated explanation.

---

## 🙋‍♂️ Author

Ajay Verma
[ajay.verma@crossml.com](mailto:ajay.verma@crossml.com)

---
