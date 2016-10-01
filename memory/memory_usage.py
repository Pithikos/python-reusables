from multiprocessing import Process, Manager
import psutil


def memory_now(pid):
    return psutil.Process(pid).memory_info()[0] / (1024 ** 2)


def memory_sampler(pid, samples_freq, samples_order):
    """Get memory usage samples for given pid

    Takes:
        samples_freq(dict): Counting the sample occurance in every interval
        samples_order(list): Keeps track of the samples' order
    """
    if not pid:
        print('No PID given.')
        exit(1)
    proc = psutil.Process(pid)
    while True:
        sample = proc.memory_info()[0] / (1024 ** 2)
        if not sample in samples_freq:
            samples_freq[sample] = 1
            samples_order.append(sample)
        else:
            samples_freq[sample] += 1


def memory_profile(fn, arg):
    """Measure memory consumption for given function

    The memory usage given back is the best possible we can that reflects
    the actual memory consumption. A small error is always there (for example due
    to the boilerplate of Python) but as long as you compare outputs relative to
    each other (function1 vs function2) there should be no problem.

    The way we accomplish the profiling is by (1) starting the function on its
    own process (in order the profiler not to interfere) and (2) starting a memory
    sampler before the function process even starts. That way we can get a realistic
    measurement of the actual memory consumption.

    Returns:
        total memory of the boilerplate (just before starting profiling)
        first memory peak for the function
        average memory usage for the function
        highest memory peak for the function
    """
    def sleep_and_start(fn, *args):
        time.sleep(0.05) # Give some time for to-be-sampled proc to start.
        return fn(*args)
    manager = Manager()
    samples_freq = manager.dict()
    samples_order = manager.list()
    sampled_proc = Process(target=sleep_and_start, args=(fn, arg))

    sampled_proc.start()
    memsampler = Process(target=memory_sampler, args=(sampled_proc.pid, samples_freq, samples_order))
    memsampler.start()
    sampled_proc.join()
    memsampler.terminate()

    samples_freq  = dict(samples_freq)
    samples_order = list(samples_order)
    mem_init      = samples_order[0]

    # Since we start profiling before we actually run the function, we can find
    # roughly the memory size of the boilerplate and remove it from our samples.
    # We also want to remove any 'invalid' samples that occured before proper
    # initializations.
    if 0 in samples_freq and 0 in samples_order:
        del samples_freq[0]
        samples_order.remove(0)
    if len(samples_order) > 1:
        del samples_freq[samples_order[0]]
        samples_order = samples_order[1:]
    samples_order = list(map(lambda s: s-mem_init, samples_order))
    samples_freq  = { (s-mem_init):v for s,v in samples_freq.items()}

    num_values = sum(samples_freq.values())
    sum_values = sum([k*v for k,v in samples_freq.items()])
    return (mem_init, min(samples_order), sum_values/num_values, max(samples_order))



