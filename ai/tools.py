import os

import traceback
from groq import Groq
from dotenv import load_dotenv
import subprocess

from ai.utils import readFile
from ai.config import CHAT_PROMPT, READ_PROMPT, RUN_PROMPT 

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))


def processRunOutput(cmd_lst):

    result = subprocess.run(f'python {cmd_lst[2]}', check=True, capture_output=True, text=True)
    # print(result.stdout)
    response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                            {
                                "role":'system',
                                'content': RUN_PROMPT,
                            },
                            {
                                'role':'user',
                                'content': f'''Program Output:
                                            {result.stdout}
                                            Return Code:
                                            {result.returncode}''',
                            }
                                    ],
                            )
                
    return response.choices[0].message.content         

def processRunError(cmd_lst, e):
    
    file_contents = readFile(cmd_lst[2])

    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                                {
                                  "role":'system',
                                  'content': RUN_PROMPT,
                                },
                                {
                                  'role':'user',
                                  'content': f'''File Contents: {file_contents}
                                                 STDERR: {e.stderr}
                                                 Return Code: {e.returncode}''',
                                }
                                ],
                                )
                    
    return response.choices[0].message.content

def readFiles(cmd_lst):
        file_content = readFile(cmd_lst[2])

        response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                {
                    "role":'system',
                    'content': READ_PROMPT,
                },
                {
                    "role": "user",
                    "content": f"Explain this code:\n\n{file_content}"
                }
            ]
        )

        return response.choices[0].message.content


def chatAnswer(cmd_lst):
    prompt = ' '.join(cmd_lst[1:])

    response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role":'system',
                    'content': CHAT_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ]
                )

    return response.choices[0].message.content
