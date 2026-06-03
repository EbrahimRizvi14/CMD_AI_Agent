import sys
import os
import subprocess
import shlex

from ai.tools import processRunError, processRunOutput, readFiles, chatAnswer


def main():

    builtin = ['exit', 'type', 'echo']

    while True:

        sys.stdout.write('$ ')

        command = input()
        cmd_lst = shlex.split(command)

        if not cmd_lst:
            continue

        if cmd_lst[0] == "exit":
            print("Buh bye! Toodles!")
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
                print(readFiles(cmd_lst))
            
            elif cmd_lst[1] == 'run':
                try:
                    print(processRunOutput(cmd_lst))          
                                    
                except subprocess.CalledProcessError as e:
                    print(processRunError(cmd_lst, e))
                                        
            else:
                print(chatAnswer(cmd_lst))

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
