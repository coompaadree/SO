### Grupo: SO-TI-02
### Aluno 1: André Alexandre (fc62224)
### Aluno 2: Sofian Fathallah (fc62814)
### Aluno 3: Tair Injai (fc62848)



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



def prcs(lines, filename, word, mode):
    count = count_words(lines, word, mode)
    sys.stdout.write(f"Processo {current_process().name} - Ficheiro {filename} - Contagem: {count} \n")



def split_file(filename, num_parts):
    with open(filename[0], 'r', encoding='utf-8') as file:
        lines = file.readlines()
    size = len(lines) // num_parts
    return [lines[i*size:(i+1)*size] for i in range(num_parts - 1)] + [lines[(num_parts-1)*size:]]



def distribute(files, word, mode, num_processes):
    processes = []
    
    if len(files) == 1:  # Caso de apenas um arquivo
        filename = files
        file_parts = split_file(filename, num_processes)
        for i, lines in enumerate(file_parts):
            process = Process(target=prcs, args=(lines, filename, word, mode), name=i+1)
            processes.append(process)
            process.start()

    else:  # Caso de múltiplos arquivos
        file_groups = [files[i::num_processes] for i in range(num_processes)]
        for i, file_group in enumerate(file_groups):
            lines = []
            for filename in file_group:
                with open(filename, 'r', encoding='utf-8') as file:
                    lines.extend(file.readlines())
            process = Process(target=prcs, args=(lines, ', '.join(file_group), word, mode), name=i+1)
            processes.append(process)
            process.start()

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
    
    # Ajusta o número de processos se necessário
    if len(files) < num_processes and len(files)!=1:
        num_processes = len(files)

    distribute(files, word, mode, num_processes)



if __name__ == "__main__":
    main(sys.argv[1:])
