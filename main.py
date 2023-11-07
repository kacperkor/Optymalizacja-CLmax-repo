import numpy as np
import pandas as pd
import time
import subprocess
import os
from datetime import timedelta

from functions import initialization, write_settings, read_output

threads = 12             # Ile wątków xfoila wykorzystać
cieciwa1 = 0.7
cieciwa2 = 0.8
alfa1 = 8
alfa2 = 10
alfa_step = 0.01

limits = [cieciwa1, cieciwa2, alfa1, alfa2]
zakres_cieciw = np.linspace(cieciwa1, cieciwa2, 101)
zakres_alfa = np.linspace(alfa1, alfa2, 201)
output = pd.DataFrame(index=zakres_alfa)
print(output)

process_list, free_slot_list = initialization(limits, threads)

start_time = time.monotonic()

for cieciwa in zakres_cieciw:
    cieciwa_not_assigned = True
    try:
        os.remove(f'output{cieciwa}.dat')
    except FileNotFoundError:
        pass

    while cieciwa_not_assigned:
        for i, free_slot in enumerate(free_slot_list):
            if free_slot:
                write_settings(cieciwa, alfa1, alfa2, alfa_step)
                process_list[i] = subprocess.Popen(f'xfoil.exe < ustawienia{cieciwa}.conf', shell=True, stdout=False)
                free_slot_list[i] = False
                # print(cieciwa, i, True)
                cieciwa_not_assigned = False
                print(time.asctime(time.localtime()), cieciwa)
                break
            else:
                # print(cieciwa, i, False)
                pass

        for i, process in enumerate(process_list):
            try:
                check = process.poll()
            except AttributeError:
                continue

            if check is None:                   # proces dalej działa
                pass
            else:                               # proces się zakończył
                free_slot_list[i] = True
        time.sleep(0.1)


for i, process in enumerate(process_list):
    while True:
        check = process.poll()
        if check is None:                   # proces dalej działa
            pass
        else:                               # proces się zakończył
            print('proces', i, 'zakonczony')
            break
        time.sleep(0.1)


for i, cieciwa in enumerate(zakres_cieciw):
    output.insert(i, cieciwa, read_output(cieciwa))
    print(output)


end_time = time.monotonic()

print(timedelta(seconds=end_time - start_time))
