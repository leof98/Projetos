'''
10.09
0.2
'''

import sys
import csv
from tabulate import tabulate
import os

# Global variable to keep track of the ID
#FIXME: the counter always returns to 0
# (acho que vou fazer um arquivo JSON na pasta data, para armazenar o ID. Posso usar o mesmo arquivo para salvar o email depois(?)).
id_counter = 0

# The program has three modes: write, read and done
def main():
    try:
        check_cl_arg()
        mode = check_mode(sys.argv[1])
        # Adicionar nova tarefa
        if mode == 'write':
            print('\n> WRITE MODE\n')
            new_task()
        # Visualizar tarefas (modo leitura)
        if mode == 'read':
            print('> READ MODE')
            read_task()
        if mode == 'done':
            finish_task()
    except KeyboardInterrupt:
        sys.exit('\nOperation canceled by the user.')
    
# 
def load_id_counter():
    settings_path = os.path.join('data', 'settings.txt')
    try:
        with open(settings_path, 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Function that writes a new task
# TODO: usar uma biblioteca que use uma interface grafica, para facilitar a entrada de novas tarefas
def new_task():
    global id_counter # global keyword declara o uso da variavel global
    
    try:
        # TODO: Implement data validation for tasks input (name, description, date)
        # Get a user input for the new task
        task_name = input('Set a name for the task: ')
        task_desc = input('Describe the task: ')
        task_star = int(input('Rate relevance (0-2): '))
        task_date = input('Set a deadline(DD-MM-AA): ') # TODO: mudar a data para ficar no formato de DD-MM
    except ValueError:
        sys.exit('Invalid Input')
        
    # Adiciona 1 ao countador do ID
    id_counter += 1
    
    # Abre o arquivo no 'append mode', escreve a linha com a nova tarefa no arquivo csv
    with open('task.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([id_counter, task_name, task_desc, task_star, task_date])
    
    print(f'Task {id_counter} added successfully.')

tabela = []
# Fucao para mostar a tabela formatada com as tarefas
def read_task():
    try:
        with open('task.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                tabela.append(row)        
    except FileNotFoundError:
        sys.exit('ERROR: task file not found')
    print(tabulate(tabela[1:], headers=tabela[0], tablefmt='grid'))
    
# Function to mark a task as done and remove it ()
def finish_task():
    try:
        with open('task.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if len(rows) <= 1:
                print('No tasks found.')
            else:
                print('\nTask ID and Name:')
                for i, row in enumerate(rows[1:]):  # Skip header row
                    print(f'{i}: {row[1]}')
                task_id = input(f'Enter the task ID to mark as done (0-{len(rows)-2}): ')
                try:
                    task_id = int(task_id)
                    if 0 <= task_id < len(rows)-1:
                        task_name = rows[task_id + 1][1]  # Offset for header row
                        print(f"Marking task {task_id}: '{task_name}' as done.")

                        # Remove the completed task from the list
                        del rows[task_id + 1]  # Offset for header row

                        # Save the updated list back to the CSV file
                        with open('task.csv', 'w', newline='') as updated_file:
                            writer = csv.writer(updated_file)
                            writer.writerow(rows[0])  # Write the header row
                            writer.writerows(rows[1:])  # Write tasks (excluding the deleted one)
                    else:
                        print('Invalid task ID. No task found with that ID.')
                except ValueError:
                    print('Invalid input. Please enter a valid task ID.')
                    
    except FileNotFoundError:
        sys.exit('ERROR: task file not found')

# Function to check the command line arguments
def check_cl_arg():
    if len(sys.argv) < 2:
        sys.exit('Too few command-line arguments')
    if len(sys.argv) > 2:
        sys.exit('Too many command-line arguments')

# Função para verificar modo
def check_mode(input):
    if input == 'write':
        return 'write'
    if input == 'read':
        return 'read'
    if input == 'done':
        return 'done'
    sys.exit('Invalid Input')

# TODO: Funcao para enviar um email para o usuario (tarefas 2 'estrelas')
def send_reminder():
    ...

if __name__ == '__main__':
    main()
# The - finish_task() function was generated with assistance from ChatGPT by OpenAI