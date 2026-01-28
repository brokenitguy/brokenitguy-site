import os
import json
import datetime
import subprocess
from google import genai

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_FILE = os.path.join(BASE_DIR, "logs.json")
INPUT_FILE = os.path.join(BASE_DIR, "what i am doing.txt")
MARKER_FILE = os.path.join(BASE_DIR, ".log_marker")
SECRETS_FILE = os.path.join(BASE_DIR, "secrets.json")
FEED_FILE = os.path.join(BASE_DIR, "feed.xml")

# --- LOAD SECRETS ---
try:
    with open(SECRETS_FILE, "r") as f:
        secrets = json.load(f)
        API_KEY = secrets["GEMINI_API_KEY"]
except FileNotFoundError:
    print("CRITICAL ERROR: secrets.json not found!")
    exit()

# Initialize Gemini Client
client = genai.Client(api_key=API_KEY)

# --- HELPER: GENERATE RSS FEED ---
def generate_rss(all_logs):
    """Generates an RSS feed from the logs.json data."""
    rss_content = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
 <title>BrokenITGuy Updates</title>
 <description>Live log entries from the headless pipeline.</description>
 <link>https://brokenitguy.com</link>
 <language>en-us</language>
"""
    for entry in all_logs[:10]:
        rss_content += f""" <item>
  <title>{entry.get('title', 'Update')}</title>
  <description>{entry.get('content', 'No Content')}</description>
  <link>https://brokenitguy.com</link>
  <guid>{entry.get('date', '')}</guid>
 </item>
"""
    rss_content += "</channel>\n</rss>"
    
    with open(FEED_FILE, "w") as f:
        f.write(rss_content)

# --- MAIN UPDATE SCRIPT ---
def update_logs():
    # 1. CHECK FOR NEW CONTENT
    last_pos = 0
    if os.path.exists(MARKER_FILE):
        try:
            with open(MARKER_FILE, "r") as f:
                last_pos = int(f.read().strip())
        except:
            last_pos = 0

    try:
        with open(INPUT_FILE, "r") as f:
            f.seek(last_pos)
            new_content = f.read().strip()
            current_pos = f.tell()
    except FileNotFoundError:
        print("Waiting for input file...")
        return

    # GATEKEEPER: Stop if there is no new text to process
    if not new_content:
        print("⏸️ No new content since last run. Skipping build to save tokens.")
        return

    print(f"🔹 New content detected: {len(new_content)} chars. Processing batch...")

    # 2. READ EXISTING LOGS
    existing_data = []
    if os.path.exists(LOGS_FILE):
        try:
            with open(LOGS_FILE, "r") as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []

    # 3. GENERATE ENTRIES WITH GEMINI
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=f"""
            I have a list of raw terminal notes with timestamps. 
            Format EACH separate timestamped note into its own JSON object.
            Return a JSON LIST of objects only. No markdown formatting.
            
            Use the 'BrokenITGuy' persona: gritty, technical, and honest.
            
            Format for each object:
            {{
                "date": "YYYY-MM-DD HH:MM:SS",
                "status": "SUCCESS",
                "title": "TECH_TITLE",
                "content": "SUMMARIZED_CONTENT (use <br> for new lines)",
                "tags": ["#automated", "#brokenitguy"]
            }}
            
            Raw Text:
            {new_content}
            """
        )
        
        # Clean response and parse JSON
        cleaned_response = response.text.replace("```json", "").replace("```", "").strip()
        new_entries = json.loads(cleaned_response)
        
        # Ensure it's a list even if only one note was processed
        if isinstance(new_entries, dict):
            new_entries = [new_entries]

        if not new_entries:
            print("⚠️ AI produced no valid entries. Stopping.")
            return

        # Merge with old logs and sort by date descending
        updated_data = new_entries + existing_data
        updated_data.sort(key=lambda x: x['date'], reverse=True)

    except Exception as e:
        print(f"⚠️ AI Generation or Parsing failed: {e}")
        return

    # 4. SAVE EVERYTHING LOCALLY
    with open(LOGS_FILE, "w") as f:
        json.dump(updated_data, f, indent=4)

    generate_rss(updated_data)

    # Save the marker so we don't re-process these notes
    with open(MARKER_FILE, "w") as f:
        f.write(str(current_pos))

    # 5. PUSH TO GITHUB
    print(">> Syncing batch to GitHub...")
    try:
        subprocess.run(["git", "add", "logs.json", "feed.xml", ".log_marker"], check=True)
        subprocess.run(["git", "commit", "-m", "Batch update logs via scheduled task"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("✅ SUCCESS: Website updated and tokens saved!")
    except subprocess.CalledProcessError as e:
        print(f"!! Git Error: {e}")

if __name__ == "__main__":
    update_logs()