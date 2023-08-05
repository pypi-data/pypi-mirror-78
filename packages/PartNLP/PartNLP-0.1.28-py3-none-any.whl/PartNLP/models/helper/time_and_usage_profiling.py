"""
        SEMANTIC SEARCH ENGINE
            AUTHORS:
                MOSTAFA & po_oya
"""
from time import perf_counter
import psutil as p
import os
from terminaltables import AsciiTable
from PartNLP.models.helper.color import Color


def profile(func):
    """
          Wrapper Profiler
    """
    def wrap(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        func_time = perf_counter() - start_time
        usage = [[f'{Color.green}MEMORY USAGE{Color.endc}',
                  f'{Color.blue}SWAP USAGE{Color.endc}',
                  f'{Color.header}TIME{Color.endc}'],
                 [f'{Color.green}{p.virtual_memory().percent}{Color.endc}',
                  f'{Color.blue}{p.swap_memory().percent}{Color.endc}',
                  f'{Color.header}{float(func_time)}{Color.endc}']]
        usage_table = AsciiTable(usage)
        usage_table.title = f'{Color.fail}{func.__name__} profiling{Color.endc}'
        print('\n')
        print(usage_table.table)
        return result
    return wrap


def profile_file(data):
    for key, value in data.items():
        batch_size, package = value['batch_size'], value['package']
        usage = [['OPERATION', 'BATCH_SIZE', 'TIME', 'MEMORY USAGE', 'SWAP USAGE', 'TOTAL_MEMORY', 'TOTAL_SWAP'],
                 [key, value['batch_size'], value['time'], value['memory']/value['num_of_calls'],
                  value['swap']/value['num_of_calls'], value['total_memory'], value['total_swap']]]
        usage_table = AsciiTable(usage)
        usage_table.title = f'{package} profiling'
        with open(os.getcwd() + '/preprocessed/' + f'{batch_size}_{package}' + '_profile.txt', 'a') as outfile:
            outfile.write(usage_table.table)
            outfile.write('\n' + '\n')
