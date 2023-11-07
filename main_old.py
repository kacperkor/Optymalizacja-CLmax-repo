from functions_old import initialization, runtime, define_settings, read_results

threads = 10             # Ile wątków xfoila wykorzystać, minimum 4
cieciwa1 = 0.7
cieciwa2 = 0.9
alfa1 = 5
alfa2 = 13
limits = [cieciwa1, cieciwa2, alfa1, alfa2]


process, check = initialization(limits, threads)

for i in range(0, 5):
    compute_time = runtime(threads, process, check)
    print(compute_time)
    clmaxmax, cieciwa_clmaxmax, alfa_clmaxmax, limits = read_results(threads, cieciwa1, cieciwa2)
    print(clmaxmax, cieciwa_clmaxmax, alfa_clmaxmax, limits)
    define_settings(limits, threads)
