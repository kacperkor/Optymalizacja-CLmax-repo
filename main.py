from functions import initialization, runtime, define_settings, read_results

threads = 4             # Ile wątków xfoila wykorzystać, minimum 4
cieciwa1 = 0.7
cieciwa2 = 0.9
alfa1 = 5
alfa2 = 13

process, check = initialization(cieciwa1, cieciwa2, alfa1, alfa2, threads)

for i in range(0, 5):
    compute_time = runtime(threads, process, check)
    print(compute_time)
    clmaxmax, cieciwa1, cieciwa2, alfa1, alfa2 = read_results(threads, cieciwa1, cieciwa2)
    print(clmaxmax)
    define_settings(cieciwa1, cieciwa2, alfa1, alfa2, threads)
