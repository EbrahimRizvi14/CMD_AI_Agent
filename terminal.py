import sys
import os
import subprocess
import shlex

from ai.tools import processRunError, processRunOutput, readFiles, chatAnswer, summarizeProject


def main():

    builtin = {'exit': 'Exits the shell', 
               'type': 'Display information about command types',
               'echo': 'Display a line of text',
               'pwd': 'Print working directory',
               'cd': 'Change directory',
               'ai': 'Interact with the AI assistant',
               'ls': 'List directory contents',
               'help': 'Show all builtins',
               }

    while True:

        sys.stdout.write('$ ')

        command = input()
        cmd_lst = shlex.split(command)

        if not cmd_lst:
            continue

        if cmd_lst[0] == "exit":
            print("Buh bye!")
            sys.exit()

        elif cmd_lst[0] == 'cd':
            target_dir = cmd_lst[1]

            try:
                os.chdir(target_dir)

            except FileNotFoundError:
                print(f'cd: no such file or dir: {target_dir}')
            
            except NotADirectoryError:
                 print(f'cd: not a directory: {target_dir}')

            except PermissionError:
                 print(f"cd: permission denied: {target_dir}")

        elif cmd_lst[0] == 'pwd':
             print(os.getcwd())
        
        elif cmd_lst[0] == 'ls':
            try:
                items = os.listdir(os.getcwd())
                for item in items:
                    path = os.getcwd() + f"\{item}"

                    if os.path.isdir(path) and not item.startswith('.'):
                        print(f'[DIR] {item}')
                    elif not item.startswith('.'):
                        print(item)


            except FileNotFoundError:
                 print(f'ls: cannot access {os.getcwd()}: no such file or directory')

        elif cmd_lst[0] == 'help':
             print('Builtins:')
             for i, j in builtin.items():
                  print(f'{i}: {j}')

        elif cmd_lst[0] == 'type':
                
                if cmd_lst[1] in builtin:
                     print(f'{cmd_lst[1]} is a shell builtin')

                else:
                                
                    path = os.environ.get('PATH', "")
                    directories = path.split(os.pathsep)

                    found_file = False
                    
                    for directory in directories:
                         if os.path.isdir(directory):
                              file_path = os.path.join(directory, cmd_lst[1])
                              if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                                   print(f'{cmd_lst[1]} is {file_path}')
                                   found_file = True
                                   break
                              
                    if not found_file:
                        print(f'{' '.join(cmd_lst[1:])}: not found')

        elif cmd_lst[0] == 'echo':
            print(str(' '.join(cmd_lst[1:])))


        elif cmd_lst[0] == 'ai':

            if cmd_lst[1] == 'read':
                print(readFiles(cmd_lst))
            
            elif cmd_lst[1] == 'run':
                try:
                    print(processRunOutput(cmd_lst))          
                                    
                except subprocess.CalledProcessError as e:
                    print(processRunError(cmd_lst, e))

            elif cmd_lst[1] == 'project':
                print(summarizeProject())
                                        
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
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()
