from rtgo._mythreads import *
import multiprocessing
from logging import Logger


LOGGER = Logger("JobHandler Logger")


def set_logger(logger):
    """
    set the logger (otherwise, default is used)
    :param logging.Logger logger:
    :return:
    """
    global LOGGER
    LOGGER = logger


def __get_results_from_threads(running_threads):
    """
    for each running thread, get the results and return as a flat list
    :param running_threads:
    :return: list of results or Error
    """
    thread_results = []

    if running_threads:
        for thread in running_threads:
            try:
                result, input_data = thread.join()
                return_data = result.get_return_value()
                error = result.get_error()

                if return_data:
                    thread_results.append(return_data)

                if error:
                    LOGGER.error(f"{error[0].__class__}: Results error from {thread.name} using {input_data}: {error[0]}\n")

            except Exception as e:
                LOGGER.error(f"{e.__class__}: Unable to collect results from {thread.name} ({thread.__func.__name__})")

        try:
            # Re-combine the results to return as if a single thread was used (flatten list)
            return_val = [item for sublist in thread_results for item in sublist]
            LOGGER.info(f"Successfully merged results from multiple threads")
            return return_val

        except Exception as e:
            LOGGER.error(f"{e.__class__}: could not merge thread results.")
            return e


def go_cluster(funcs):
    """
    runs the given functions concurrently
    :param funcs: list of functions to run
    :return: list containing results from each function executed
    """
    running_threads = []

    # create a thread for each supplied function
    for i in range(len(funcs)):
        thread_id = i + 1
        thread = MyBasicThread(thread_id, f"Thread-{thread_id}", funcs[i], LOGGER)
        thread.daemon = True
        running_threads.append(thread)
        thread.start()

    return __get_results_from_threads(running_threads)


def go(func, args, arg_data_index, n_threads=0):
    """
    runs the function across n CPU threads
    :param function func: function to run
    :param list args: args to be passed to the function
    :param int arg_data_index: list index of the arg
    :param int n_threads: number of threads
    :return: list of results from running the function
    """
    # initialise lists of running thread objects and results, data count, and an args copy
    running_threads = []
    data_count = len(args[arg_data_index])

    if not data_count:
        LOGGER.info(f"ReadyThready.go received no input at at the specified position ({arg_data_index}) in the "
                    f"supplied arguments '{args}'. The function '{func.__name__}' will not be run")
        return None

    # set number of threads to use: specified, CPU core count, or data count (to prevent use of excess resources)
    if n_threads == 0:
        n_threads = multiprocessing.cpu_count()
    if data_count / n_threads <= 1:
        n_threads = data_count

    LOGGER.info(f"Using {n_threads} threads to run '{func.__name__}' for {data_count} input items")

    # split data by number of threads (works with DataFrames)
    data = __split_list(args[arg_data_index], n_threads, data_count)

    # spool up new threads
    for i in range(n_threads):
        # initialise thread ID, thread arg and thread object
        thread_id = i + 1  # Thread 0 handles the additional threads, so start at index 1
        thread_args = copy.deepcopy(args)
        thread_args[arg_data_index] = copy.deepcopy(data[i])
        thread = MyThread(thread_id, f"Thread-{thread_id}", func, thread_args, LOGGER, arg_data_index)

        # terminate daemon threads if the host process terminates
        thread.daemon = True

        # keep track of running threads for future joining and start
        running_threads.append(thread)
        thread.start()

    return __get_results_from_threads(running_threads)


def __split_list(input_list, n_threads, data_count):
    """
    Splits a list into n lists based on n_threads value.
    :param list input_list: List to be split.
    :param int n_threads: Number of threads to split the data into.
    :param int data_count: Total number of items in input_list
    :return: List containing a list for each thread
    """
    # print(n_threads, data_count)
    if isinstance(input_list, list):
        chunk_size = data_count // n_threads
        remainder = data_count % n_threads
        max_slice_index = data_count - remainder
        new_list = []

        # split data records into one list per thread
        for i in range(n_threads):
            lower_slice = i * chunk_size
            upper_slice = min((i + 1) * chunk_size, max_slice_index)
            new_list.append(input_list[lower_slice:upper_slice])

        # spread remainder records across sub lists
        while remainder > 0:
            for i in range(n_threads):
                if remainder:
                    current_record = input_list[-remainder]
                    new_list[i].append(current_record)
                    remainder -= 1
                else:
                    break
        return new_list
