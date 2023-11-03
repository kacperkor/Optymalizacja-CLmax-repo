import subprocess
import os


def write_settings(ck, alfa0, alfa1, step):
    with open('ustawienia.conf', 'w') as conf:
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
        output.dat\n
        aseq {alfa0} {alfa1} {step}\n''')


write_settings(0.8, 2, 10, 0.5)

os.remove('output.dat')

subprocess.call('xfoil.exe < ustawienia.conf', shell=True)
