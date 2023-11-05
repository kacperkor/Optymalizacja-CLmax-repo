from functions import initialization, runtime, define_settings, read_results

threads = 4             # Ile wątków xfoila wykorzystać, minimum 3

#process, check = initialization(0.7, 0.9, 5, 13, threads)

read_results(threads, 0.7, 0.9)

#while True:
    #compute_time = runtime(threads, process, check)
    #print(compute_time)
    #read_results()
    #define_settings(cieciwa1, cieciwa2, alfa1, alfa2, threads)
