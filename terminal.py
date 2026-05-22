import sys
import os
import subprocess
import shlex
import traceback

from groq import Groq
from dotenv import load_dotenv


load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))


def read_file(path):

    try:
        with open(path, 'r') as f:
            return f.read()
        
    except Exception as e:
        return str(e)


def main():

    builtin = ['exit', 'type', 'echo']

    while True:

        sys.stdout.write('$ ')

        command = input()
        cmd_lst = shlex.split(command)

        if not cmd_lst:
            continue

        if cmd_lst[0] == "exit":
            sys.exit()

        elif cmd_lst[0] == 'type':
                
                if cmd_lst[1] in builtin:
                     sys.stdout.write(f'{cmd_lst[1]} is a shell builtin\n')

                else:
                                
                    path = os.environ.get('PATH', "")
                    directories = path.split(os.pathsep)

                    found_file = False
                    
                    for directory in directories:
                         if os.path.isdir(directory):
                              file_path = os.path.join(directory, cmd_lst[1])
                              if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                                   sys.stdout.write(f'{cmd_lst[1]} is {file_path}\n')
                                   found_file = True
                                   break
                              
                    if not found_file:
                        sys.stdout.write(f'{' '.join(cmd_lst[1:])}: not found\n')

        elif cmd_lst[0] == 'echo':
            sys.stdout.write(str(' '.join(cmd_lst[1:])) + '\n')


        elif cmd_lst[0] == 'ai':

            if cmd_lst[1] == 'read':
                file_content = read_file(cmd_lst[2])
                response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                {
                    "role": "user",
                    "content": f"Explain this code:\n\n{file_content}"
                }
            ]
        )
                print(response.choices[0].message.content)
            
            if cmd_lst[1] == 'run':
                
                path = os.environ.get('PATH', "")
                directories = path.split(os.pathsep)

                for directory in directories:
                            if os.path.isdir(directory):
                                file_path = os.path.join(directory, cmd_lst[0])
                                if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                                    subprocess.run([cmd_lst[0]] + cmd_lst[1:])
                                    try:
                                        error_output = subprocess.check_output([cmd_lst[0]] + cmd_lst[1:], stderr=subprocess.STDOUT, text=True)
                                    except subprocess.CalledProcessError as e:
                                        print(f"Error occurred while running {cmd_lst[0]}: {e}")
                                        print(f"Error output: {e.output}")
                                        
            prompt = ' '.join(cmd_lst[1:])

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            print(response.choices[0].message.content)
        else:

            path = os.environ.get('PATH', "")
            directories = path.split(os.pathsep)

            found_file = False

            for directory in directories:
                         if os.path.isdir(directory):
                              file_path = os.path.join(directory, cmd_lst[0])
                              if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                                   subprocess.run([cmd_lst[0]] + cmd_lst[1:])
                                   found_file = True
                                   break  
            if not found_file:
                sys.stdout.write(f"{command}: command not found\n")


if __name__ == "__main__":
    main()
