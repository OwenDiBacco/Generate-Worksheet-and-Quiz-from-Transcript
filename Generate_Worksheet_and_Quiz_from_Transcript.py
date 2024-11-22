import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

import io
import google.generativeai as genai
import json
import webbrowser
from apiclient import discovery
from oauth2client.file import Storage
from httplib2 import Http
from oauth2client import tools, client

import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

from tkinter import Tk, filedialog


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('200x250')
        self.root.title("Txt File Selector")


        original_image = Image.open('images/txt_image.png')
        resized_image = original_image.resize((50, 50), Image.LANCZOS)
        zip_icon = ImageTk.PhotoImage(resized_image)

        zip_button = tk.Button(self.root, image=zip_icon, command=self.select_txt_file, borderwidth=0)
        zip_button.pack(pady=10)


        description_label = tk.Label(self.root, text="Open Zip File")
        description_label.pack()

        close_button = tk.Button(self.root, text="Run", command=self.close_app)
        close_button.pack(side=tk.BOTTOM, pady=10)

        self.root.mainloop()
        print('heer')

    def select_txt_file(self):
        # Create a Tkinter window to open the file dialog
        root = Tk()
        root.withdraw()  # Hide the main Tkinter window
        
        # Open the file dialog to select a .txt file
        selected_file = filedialog.askopenfilename(
            title="Select a .txt file",
            filetypes=[("Text Files", "*.txt")]  # Filter to only show .txt files
        )
        
        # Return the selected file path
        if selected_file:
            self.txt_file = selected_file
            print(self.txt_file)
        else:
            print("No file selected.")
            self.txt_file = None
            print(self.txt_file)
    

    def close_app(self):
        self.root.destroy()


    # create the main window
    

def prompt_genai(prompt):
    text = ''
    load_dotenv() # Load variables from .env
    api_key = os.getenv("API_KEY")  # Access the API key
    genai.configure(api_key=api_key) # Replace with your own Gemini API Key
    model = genai.GenerativeModel("gemini-1.5-flash")
    responses = model.generate_content([prompt])
    for response in responses:
        text += ' ' + response.text
    
    return text


'''
Code in function taken from Tanmay
'''
def generate_form(forms_questions_json):
    generated_files = {}

    forms_questions_json_str = json.dumps(forms_questions_json)
    forms_questions = json.loads(forms_questions_json_str)
    print("Parsed JSON successfully")
    # Setup Google Forms API
    SCOPES = [
        "https://www.googleapis.com/auth/forms.body",
        "https://www.googleapis.com/auth/forms.responses.readonly"
    ]
    DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
    store = Storage("token.json") # token is Tanmay's
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets("client_secrets.json", SCOPES) # client secret is Tanmay's
        creds = tools.run_flow(flow, store)
    form_service = discovery.build(
        "forms", "v1", http=creds.authorize(Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False
    )
    form = {
        "info": {
            "title": "Generated Quiz",
        }
    }
    result = form_service.forms().create(body=form).execute()
    update_requests = [
        {
            "updateSettings": {
                "settings": {"quizSettings": {"isQuiz": True}},
                "updateMask": "quizSettings.isQuiz",
            }
        }
    ]
    question_index = 0
    for question_data in forms_questions:
        question_text = question_data.get("question", "")
        options = [{"value": option} for option in question_data.get("options", [])]
        correct_answer = question_data.get("correctAnswer", "A")
        parsed_correct_answer = ord(correct_answer.lower()) - ord('a')
        question_request = {
            "createItem": {
                "item": {
                    "title": question_text,
                    "questionItem": {
                        "question": {
                            "required": True,
                            "grading": {
                                "pointValue": 1,
                                "correctAnswers": {
                                    "answers": [{"value": options[parsed_correct_answer]["value"]}]
                                },
                                "whenRight": {"text": "You got it!"},
                                "whenWrong": {"text": "Sorry, that's wrong"}
                            },
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": options,
                                "shuffle": True
                            }
                        }
                    }
                },
                "location": {
                    "index": question_index 
                }
            }
        }
        update_requests.append(question_request)
        question_index += 1
    form_service.forms().batchUpdate(formId=result["formId"], body={"requests": update_requests}).execute()
    form_url = f"https://docs.google.com/forms/d/{result['formId']}/edit"
    webbrowser.open(form_url)
    form_txt = io.BytesIO()
    form_txt.write(form_url.encode('utf-8'))
    form_txt.seek(0)
    generated_files['form'] = form_txt


if __name__ == "__main__":
    form_prompt = f"""
                    Based on the following notes and transcript, generate a list of multiple-choice questions. 
                    Format each question as JSON objects with the following structure:

                    {{
                        "question": "Question text",
                        "options": [
                            "Option A",
                            "Option B",
                            "Option C",
                            "Option D"
                        ],
                        "correctAnswer": "A"
                    }}
                    """
    app = App()
    content = app.txt_file
    print(content)
    response = prompt_genai(form_prompt)
    print(response)
    generate_form(response)
    
    


