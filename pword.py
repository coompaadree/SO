### Grupo: SO-TI-XX
### Aluno 1: Nome Apelido (fcXXXX)
### Aluno 2: Nome Apelido (fcXXXX)
### Aluno 3: Nome Apelido (fcXXXX)

# import sys

# #TO-DO: Implementar o pword

# def main(args):
#     print('Programa: pword.py')
#     print('Argumentos: ',args)

# if __name__ == "__main__":
#     main(sys.argv[1:])





import argparse
import sys
import os
from multiprocessing import Process, current_process

def parse_arguments(arg):
    parser = argparse.ArgumentParser(description="Parallel word search and count")
    parser.add_argument("-m", choices=["c", "l", "i"], default="c", help="Modo de contagem: c (total), l (linhas), i (isolado)")
    parser.add_argument("-p", type=int, default=1, help="Número de processos paralelos")
    parser.add_argument("-w", required=True, help="Palavra a ser pesquisada")
    parser.add_argument("files", nargs="+", help="Lista de ficheiros")
    return parser.parse_args(arg)






def count_words(lines, word, mode):
    total_count = 0
    for line in lines:
        if mode == "c":
            # Modo "c": Contar todas as ocorrências da palavra
            total_count += line.count(word)
        elif mode == "l":
            # Modo "l": Contar linhas que contêm a palavra
            if word in line:
                total_count += 1
        elif mode == "i":
            # Modo "i": Contar ocorrências isoladas da palavra
            words_in_line = line.split()
            total_count += words_in_line.count(word)
    return total_count




def prcs(filename, lines, word, mode):
    count = count_words(lines, word, mode)
    sys.stdout.write(f"Processo {current_process().name} - Ficheiro {filename} - Contagem: {count} \n")


def split_file(filename, num_parts):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    size = len(lines) // num_parts
    return [lines[i*size:(i+1)*size] for i in range(num_parts)]






def distribute_tasks(files, word, mode, num_processes):
    processes = []
    
    if len(files) == 1:
        # Caso apenas um ficheiro seja passado, divida-o em partes para os processos
        filename = files[0]
        file_parts = split_file(filename, num_processes)
        for i, lines in enumerate(file_parts):
            process = Process(target=prcs, args=(filename, lines, word, mode,), name=i+1)
            processes.append(process)
            process.start()
    else:
        # Caso múltiplos ficheiros sejam passados, distribua os ficheiros entre os processos
        for i, filename in enumerate(files):
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            process = Process(target=prcs, args=(filename, lines, word, mode), name=i+1)
            processes.append(process)
            process.start()
            if len(processes) >= num_processes:
                for p in processes:
                    p.join()
                processes = []
    
    # Espera que todos os processos terminem
    for p in processes:
        p.join()




def main(args):
    args = parse_arguments(args)
    files = args.files
    word = args.w
    mode = args.m
    num_processes = args.p

    print('Programa: pword.py')
    print('Argumentos: ', args, "\n")
    
    # Verifica se há ficheiros para processar
    # if not files:
    #     print("Erro: Nenhum ficheiro especificado.")
    #     return
    
    # Ajusta o número de processos se necessário
    if len(files) < num_processes:
        num_processes = len(files)

    distribute_tasks(files, word, mode, num_processes)



if __name__ == "__main__":
    main(sys.argv[1:])
