import re
import io
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from flask import Flask, request, send_file, render_template
from docx import Document
import json
import webbrowser
from apiclient import discovery
from oauth2client.file import Storage
from httplib2 import Http
from oauth2client import tools, client
import uuid
from pytubefix import YouTube
from pytubefix.cli import on_progress
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pathlib import Path
import os

generated_files = {}

forms_questions_json = [
    {
        "question": "What is the primary reason for Python's widespread popularity, according to both the notes and the transcript?",
        "options": [
            "Its extensive third-party library ecosystem.",
            "Its use in artificial intelligence and machine learning.",
            "Its simple and beginner-friendly syntax.",
            "Its support for object-oriented programming."
        ],
        "correctAnswer": "C"
    },
    {
        "question": "Besides AI/ML, which application areas utilize Python extensively?",
        "options": [
            "Game development and mobile app development only.",
            "Scripting, automation, and backend development.",
            "Database management and network programming only.",
            "Web development and data visualization only."
        ],
        "correctAnswer": "B"
    },
    {
        "question": "Why might Python's simplicity be viewed negatively by some programmers?",
        "options": [
            "It lacks the performance of compiled languages.",
            "It has a limited standard library.",
            "Its dynamic typing can lead to runtime errors.",
            "All of the above."
        ],
        "correctAnswer": "C"
    },
    {
        "question": "Which library is used for numerical computing in Python?",
        "options": [
            "Pandas",
            "Scikit-learn",
            "TensorFlow",
            "NumPy"
        ],
        "correctAnswer": "D"
    },
    {
        "question": "What is the purpose of Django?",
        "options": [
            "Numerical computing",
            "Building web applications",
            "Machine learning",
            "Cross-platform app development"
        ],
        "correctAnswer": "B"
    },
    {
        "question": "How does Python's extensive third-party library ecosystem enhance its versatility?",
        "options": [
            "It limits the need for developers to write custom code.",
            "It reduces the learning curve for beginners.",
            "It provides pre-built solutions for a wide range of tasks.",
            "It makes Python compatible with various operating systems."
        ],
        "correctAnswer": "C"
    },
    {
        "question": "What is an interpreted language, and what is one disadvantage compared to compiled languages?",
        "options": [
            "A language that is translated line by line, slower execution speed.",
            "A language that requires compilation before execution, more complex syntax.",
            "A language that runs directly on the hardware, requires specialized compilers.",
            "A language that uses virtual machines, limited access to system resources."
        ],
        "correctAnswer": "A"
    },
    {
        "question": "What is dynamic typing, and what is a potential implication?",
        "options": [
            "Variable types are checked at compile time; it improves code readability.",
            "Variable types are checked at runtime; it can lead to runtime errors.",
            "Variable types are declared explicitly; it simplifies code maintenance.",
            "Variable types are inferred automatically; it improves program performance."
        ],
        "correctAnswer": "B"
    },
    {
        "question": "What does 'Batteries Included' mean in the context of Python?",
        "options": [
            "Python comes with a large standard library.",
            "Python requires external batteries to run.",
            "Python is only available on certain operating systems.",
            "Python is difficult to integrate with other tools."
        ],
        "correctAnswer": "A"
    },
    {
        "question": "What is the output of `import this`?",
        "options": [
            "A list of all Python modules.",
            "The Zen of Python.",
            "A simple graphics animation.",
            "An error message."
        ],
        "correctAnswer": "B"
    },
    {
        "question": "Which of the following is NOT a standard Python data type?",
        "options": [
            "String",
            "Boolean",
            "Integer",
            "Array"
        ],
        "correctAnswer": "D"
    },
    {
        "question": "What does negative indexing allow in Python sequences?",
        "options": [
            "Accessing elements from the end of the sequence.",
            "Modifying the length of the sequence.",
            "Creating new sequences.",
            "Sorting the elements of the sequence."
        ],
        "correctAnswer": "A"
    },
    {
        "question": "How are functions defined in Python?",
        "options": [
            "Using the `function` keyword.",
            "Using the `def` keyword.",
            "Using curly braces `{}`.",
            "Using square brackets `[]`."
        ],
        "correctAnswer": "B"
    },
    {
        "question": "What is a key characteristic of object-oriented programming (OOP) in Python?",
        "options": [
            "It does not support inheritance.",
            "It relies heavily on global variables.",
            "It supports classes and inheritance.",
            "It avoids the use of functions."
        ],
        "correctAnswer": "C"
    },
    {
        "question": "Which of these is NOT a mutable data structure in Python?",
        "options": [
            "List",
            "Tuple",
            "Set",
            "Dictionary"
        ],
        "correctAnswer": "B"
    },
    {
        "question": "Who created Python, and what is the origin of its name?",
        "options": [
            "Guido van Rossum, named after a type of snake.",
            "Guido van Rossum, named after the Monty Python comedy group.",
            "Linus Torvalds, named after a type of snake.",
            "Linus Torvalds, named after the Monty Python comedy group."
        ],
        "correctAnswer": "B"
    },
    {
        "question": "In what year was Python first created?",
        "options": [
            "1990",
            "1991",
            "Python's object-oriented features.",
            "Python's use of negative indexing."
        ],
        "correctAnswer": "B"
    },
    {
        "question": "What crucial aspect might be omitted in a two-minute summary of Python?",
        "options": [
            "Its syntax.",
            "Its core data structures.",
            "The nuances of its OOP implementation and error handling.",
            "Its popularity."
        ],
        "correctAnswer": "C"
    }
]


if forms_questions_json:
    try:
        pass 

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {str(e)}")
        print("Invalid JSON format received from the AI")