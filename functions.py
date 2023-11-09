import os
import numpy as np


def points(p1, p2, step, tolerance=1e-7):
    wartosc = (p2-p1)/step

    if abs((wartosc+1e-8) % 1) > tolerance:
        raise ValueError("Wartość kroku nieodpowiednia dla zakresu, ilość punktów niecałkowita:",
                         f"({p2}-{p1})/{step} = {wartosc}")

    return round(wartosc) + 1


def write_settings(ck, alfa0, alfa1, step):
    with open(f'ustawienia{ck}.conf', 'w') as conf:
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
        iter 500
        pacc
        output{ck}.dat\n
        aseq {alfa0} {alfa1} {step}\n''')


def initialization(limits, instance_quantity):
    ck1, ck2, alfa1, alfa2 = limits
    if type(instance_quantity) is not int:
        raise TypeError("Ilość wątków musi być liczbą całkowitą")
    if instance_quantity < 3:
        raise ValueError("Za mało wątków do przeprowadzenia optymalizacji")
    try:
        ck1+ck2+alfa1+alfa2
    except TypeError:
        TypeError("Wartości graniczne cięciwy i kątów natarcia muszą być liczbami")

    instancelist, checklist = [], []
    for i in range(0, instance_quantity):
        instancelist.append(None)
        checklist.append(True)

    for i in range(0, instance_quantity):
        try:
            os.remove(f'output{i}.dat')
        except FileNotFoundError:
            pass

    return instancelist, checklist


def read_output(cieciwa, zakres_alfa):
    data = np.loadtxt(f'output{cieciwa}.dat', skiprows=12)[:, [0, 1]]

    brakujace_alfa = []
    if len(zakres_alfa) != len(data):
        for alfa in zakres_alfa:
            if all(np.abs(data[:, 0] - alfa) > 1e-10):
                brakujace_alfa.append(alfa)

        print(len(data), cieciwa, brakujace_alfa)

        for alfa in brakujace_alfa:
            data = np.insert(data, np.searchsorted(data[:, 0], alfa), [alfa, None], axis=0)

    return data[:, 1]

