import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from openai import OpenAI
from ics import Calendar, Event
import dateparser
from io import BytesIO
from datetime import datetime
import pytz

app = Flask(__name__)
# Initialize OpenAI client
client = OpenAI(api_key="key")

tasks = []  # Global list to store tasks and subtasks

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_text = request.form.get('task')
        
        if not task_text:
            return jsonify({'error': 'No task text provided.'})

        # Call OpenAI API to extract date and task name
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Please extract the date and task from this input: '{task_text}'. "
                        "The input may include: "
                        "1) Sentence with task, date, and time, "
                        "2) Sentence with task and date, "
                        "3) Sentence with task and time, or "
                        "4) Sentence with relative date expressions like today, tomorrow, or time words like noon/afternoon. "
                        "Return the response formatted as 'Date - Task: <date> - <task>' for easy parsing."
                        "If the date is not specified, but time is given, assume it is today's date and the time is the time given."
                        "If the date is given as a weekday, such as Monday, assume it is the next occurence of that weekday."
                        "If the date given is tomorrow, assume it is today's date plus one day. If there is a time given, add that time on the specific date"
                        "If the date given is today, assume it is today's date. If there is a time given, add that time on today's date"
                    )
                }
            ],
            max_tokens=150,
        )
        
        task_details = response.choices[0].message.content.strip()

        # Clean up response format and parse date and task
        try:
            # Remove "Date - Task:" prefix if it exists
            if task_details.startswith("Date - Task:"):
                task_details = task_details.replace("Date - Task:", "").strip()
            
            # Split based on the hyphen to separate date and task
            date_str, task_name = task_details.split("-", 1)
            date_str = date_str.strip()
            task_name = task_name.strip()

            # Use dateparser to parse natural language date formats with settings
            date = dateparser.parse(
                date_str,
                settings={
                    'PREFER_DATES_FROM': 'future',  # Prefer dates from the future if ambiguous
                    'RELATIVE_BASE': datetime.now(pytz.timezone('UTC'))  # Handle today/tomorrow cases with timezone awareness
                }
            )
            
            if not date:
                raise ValueError("Date parsing failed.")

            # Store the task details
            task = {
                'name': task_name,
                'date': date,
                'subtasks': []
            }

            # Call OpenAI API to get subtasks
            subtask_response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"Please list up to 5 short subtasks for the task: '{task_name}'. "
                            "Provide a concise list of relevant subtasks."
                        )
                    }
                ],
                max_tokens=150,
            )
            
            subtasks = subtask_response.choices[0].message.content.strip().split('\n')
            task['subtasks'] = [subtask.strip() for subtask in subtasks if subtask.strip()][:5]

            # Debugging: Print subtasks to console
            print(f"Subtasks for '{task_name}': {task['subtasks']}")

            # Add the task to the global list
            tasks.append(task)

        except (ValueError, IndexError) as e:
            print(f"Unexpected response format: {task_details}")
            return jsonify({'error': f"Failed to parse the date and task. Response received: {task_details}"})

        # Create an .ics calendar event
        calendar = Calendar()
        event = Event()
        event.name = task_name
        event.begin = date.astimezone(pytz.timezone('UTC'))  # Ensure the event time is in UTC
        event.description = "\n".join(task['subtasks'])  # Add subtasks as description
        calendar.events.add(event)

        # Prepare the .ics file for download
        ics_file = BytesIO()
        ics_file.write(calendar.serialize().encode('utf-8'))
        ics_file.seek(0)

        # Send the .ics file as a downloadable attachment
        return send_file(
            ics_file,
            as_attachment=True,
            download_name="event.ics",
            mimetype="text/calendar"
        )
    
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
