import subprocess
import os
import numpy as np
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


def initialization(ck1, ck2, alfa1, alfa2):
    instance_quantity = 4
    instancelist, checklist = [], []
    for _ in range(0, instance_quantity):
        instancelist.append(None)
        checklist.append(None)

    define_settings(ck1, ck2, alfa1, alfa2, instance_quantity)

    return instance_quantity, instancelist, checklist


def define_settings(ck1, ck2, alfa1, alfa2, instance_quantity):
    zakres = np.linspace(ck1, ck2, instance_quantity)
    for i in range(0, instance_quantity):
        write_settings(i, zakres[i], alfa1, alfa2, 0.5)


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


