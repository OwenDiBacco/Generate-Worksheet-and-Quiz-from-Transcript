# Worksheet and Quiz Generator from Transcript

The objective of this program is to generate a Google Form project and a worksheet in a Word document based off an AI response generated from a selected text file.

## Table of Contents

- [Installation](#Installation)
- [How-To-Run-The-Application](#How-To-Run-The-Application)
- [How-The-Application-Works](#How-The-Application-Works)

## Installation

1. Clone The Repository:
   
  a). Go to your indended directory in your Command Prompt (ex. cd Downloads/Transcript Code)<br>
  b). Paste this command: 
```bash
cd Downloads/[Your Directory]
```

2. Make The Required Installations<br>

```bash
pip install -r requirements.txt
```

3. Get a Gemini API Key

   a). click on this link: https://aistudio.google.com/<br>
   b). click on 'get api key' button, then the 'create api key' button<br>
   c). select the Google Cloud Console project you would like this key associated with<br>
   d). then 'create api key in existing project'<br>
   e). copy this key becuase it is the only time you'll be able to access it<br>
   d). create a file called '.env,' declare a function named 'API_KEY' and store your API key value in it. This creates an environemnt variable named 'API KEY'<br>

4. Create a client_secret.json file

5. Create a token.json file

## How-To-Run-The-Application 

1. Run the Generate_Worksheet_and_Quiz_from_Transcript.py file
2. Select the text file icon on the GUI and select the text file you would like to reference
3. When the run has completed, you will see output worksheet in your 'output-worksheet' folder in your root directory and the Google Form will appear automatically on your screen


## How-The-Application-Works

1. The generate_questions() function is called with the path to the text file passed as an argument. The purpose of this function is to call the pompt_genai() function and pass in a prompt to generate a number of questions regarding the material
2. The questions are then passed into the generate_worksheet() function which creates a Word document with all the conent
3. The original text file is passed into the generate_json_data function which prompts the AI service through the prompt_genai() function to respond with a number of questions and corresponding answer in JSON format
4. The JSON data is then passed into the generate_forms() function which creates a google form project based on the JSON data
