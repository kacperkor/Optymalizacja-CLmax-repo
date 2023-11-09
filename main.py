import matplotlib.colors
import numpy as np
import pandas as pd
import time
import subprocess
import os
from datetime import timedelta
from matplotlib import pyplot as plt
from functions import points, initialization, write_settings, read_output

threads = 12             # Ile wątków xfoila wykorzystać
cieciwa1 = 0.7
cieciwa2 = 0.78
alfa1 = 8.4
alfa2 = 9.6
cieciwa_step = 0.01
alfa_step = 0.5

limits = [cieciwa1, cieciwa2, alfa1, alfa2]

cieciwa_points = points(cieciwa1, cieciwa2, cieciwa_step)
alfa_points = points(alfa1, alfa2, alfa_step)

zakres_cieciw = np.linspace(cieciwa1, cieciwa2, cieciwa_points)
zakres_alfa = np.linspace(alfa1, alfa2, alfa_points)

output = pd.DataFrame(index=zakres_alfa)

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

end_time = time.monotonic()
print(timedelta(seconds=end_time - start_time))


start_time = time.monotonic()

for i, cieciwa in enumerate(zakres_cieciw):
    output.insert(i, cieciwa, read_output(cieciwa, zakres_alfa))

end_time = time.monotonic()
print(timedelta(seconds=end_time - start_time))


print(f"Wartosc maksymalna: CL={output.max(None)} "
      f"dla cieciwy={output.max(0).idxmax()} i alfa={output.max(1).idxmax()}")

print(output.loc[output.max(1).idxmax(), output.max(0).idxmax()])


X, Y = np.meshgrid(output.columns, output.index)
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.plot_surface(X, Y, output, antialiased=True)
plt.show()

