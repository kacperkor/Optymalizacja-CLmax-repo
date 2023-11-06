import subprocess
import os
import numpy as np
import pandas as pd
import time
from datetime import timedelta


def write_settings(i, ck, alfa0, alfa1, step):
    with open(f'ustawienia{i}.conf', 'w') as conf:
        conf.write(f'''
        load mh32.txt
        gdes
        flap {ck} 0 10
        tgap 0.0002 0.4
        exec\n
        ppar
        N 500
        P 1.5\n\n
        oper
        re 1e6
        m 0.15
        visc
        iter 1000
        pacc
        output{i}.dat\n
        aseq {alfa0} {alfa1} {step}\n''')


def initialization(ck1, ck2, alfa1, alfa2, instance_quantity):
    if type(instance_quantity) is not int:
        raise TypeError("Ilość wątków musi być liczbą całkowitą")
    if instance_quantity < 3:
        raise ValueError("Za mało wątków do przeprowadzenia optymalizacji")
    try:
        ck1+ck2+alfa1+alfa2
    except TypeError:
        TypeError("Wartości graniczne cięciwy i kątów natarcia muszą być liczbami")

    instancelist, checklist = [], []
    for _ in range(0, instance_quantity):
        instancelist.append(None)
        checklist.append(None)

    define_settings(ck1, ck2, alfa1, alfa2, instance_quantity)
    return instancelist, checklist


def define_settings(ck1, ck2, alfa1, alfa2, instance_quantity):
    zakres = np.linspace(ck1, ck2, instance_quantity)
    step = (alfa2 - alfa1) / 10
    for i in range(0, instance_quantity):
        write_settings(i, zakres[i], alfa1, alfa2, step)


def runtime(instance_quantity, instance, check):
    start_time = time.monotonic()

    for i in range(0, instance_quantity):
        try:
            os.remove(f'output{i}.dat')
        except FileNotFoundError:
            pass
        # uruchamiam instancję (proces) xfoil z zadanymi ustawieniami
        instance[i] = subprocess.Popen(f'xfoil.exe < ustawienia{i}.conf', shell=True, stdout=False)

    while True:
        for i in range(0, instance_quantity):
            check[i] = instance[i].poll()  # zwraca None jeśli proces dalej działa
        try:
            sum(check)              # sumuje listę, jeśli lista zawiera jakieś None (proces działa) to zwraca TypeError
            break                   # udało się zsumować, czyli nie ma żadnych None (procesy zakończone) -> koniec pętli
        except TypeError:
            pass                    # nie udało się zsumować, idziemy do kolejnej iteracji

    end_time = time.monotonic()

    return timedelta(seconds=end_time - start_time)


def read_output(instance_quantity):
    cl_data = []
    clmax_in_ck = []
    for i in range(0, instance_quantity):
        data = np.loadtxt(f'output{i}.dat', skiprows=12)[:, [0, 1]]

        clmax_in_ck.append(data[:, 1].max())

        clmax_index_in_alfa = (data[:, 1].argmax())
        if clmax_index_in_alfa == 0 or clmax_index_in_alfa == len(data[:, 0]) - 1:
            print(data)
            raise RuntimeWarning('Coś nie tak, max nie powinien być na 1 miejscu')

        cl_data.append(data[clmax_index_in_alfa - 1:clmax_index_in_alfa + 2])

    return cl_data, clmax_in_ck


def read_results(instance_quantity, ck1, ck2):
    cl_data, clmax_in_ck = read_output(instance_quantity)
    zakres = np.linspace(ck1, ck2, instance_quantity)

    clmax_max_index_in_ck = clmax_in_ck.index(max(clmax_in_ck))

    print(cl_data)
    if clmax_max_index_in_ck == 0:
        new_ck1 = zakres[0]
        new_ck2 = zakres[1]
        cl_data = [cl_data[0], cl_data[1]]
    elif clmax_max_index_in_ck == len(clmax_in_ck) - 1:
        new_ck1 = zakres[-2]
        new_ck2 = zakres[-1]
        cl_data = [cl_data[-2], cl_data[-1]]
    else:
        new_ck1 = zakres[clmax_max_index_in_ck - 1]
        new_ck2 = zakres[clmax_max_index_in_ck + 1]
        cl_data = cl_data[clmax_max_index_in_ck - 1:clmax_max_index_in_ck + 2]

    new_alfa1 = cl_data[0][0][0]
    new_alfa2 = cl_data[-1][-1][0]

    return max(clmax_in_ck), new_ck1, new_ck2, new_alfa1, new_alfa2
