from threading import Thread
import copy


class MyThread(Thread):
    def __init__(self, thread_id, name, func, args, logger, data_index):
        """
        Constructor
        :param int thread_id: ID number
        :param str name: thread name
        :param function func: function to run on the thread
        :param list args: list of args to be passed to the function
        :param logging.Logger logger: project logger
        :param int data_index: list index of data within the args list
        """
        Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.__result = MyThreadResult(self.thread_id)
        self.__func = func
        self.__args = args
        self.__logger = logger
        self.__data_index = data_index

    def run(self):
        """
        Run the supplied function
        :return: value returned by function
        """
        self.__logger.info(f"Thread-{self.thread_id} running")
        try:
            # Check if the data must be run individually or passed as is.
            func_args = self.__args
            temp_args = copy.deepcopy(func_args)
            for i in range(len(func_args[self.__data_index])):
                temp_args[self.__data_index] = copy.deepcopy(func_args[self.__data_index][i])
                self.__result.set_return_value(self.__func(*temp_args))

        except Exception as e:
            self.__result.set_error(e)

    def join(self, timeout=None):
        """
        returns the result of the run
        :return: result
        :rtype: MyThreadResult
        """
        Thread.join(self)
        self.__logger.info(f"Thread-{self.thread_id} finishing")
        return self.__result, self.__args[self.__data_index]


class MyBasicThread(Thread):
    def __init__(self, thread_id, name, func, logger):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.__result = MyThreadResult(self.thread_id)
        self.__func = func
        self.__logger = logger

    def run(self):
        """
        Run the supplied function
        :return: value returned by function
        """
        self.__logger.info(f"Thread-{self.thread_id} running")
        try:
            self.__result.set_return_value(self.__func())
        except Exception as e:
            self.__result.set_error(e)

    def join(self, timeout=None):
        """
        returns the result of the run
        :return: result
        :rtype: MyThreadResult
        """
        Thread.join(self)
        self.__logger.info(f"Thread-{self.thread_id} finishing")
        return self.__result


class MyThreadResult:
    def __init__(self, thread_id):
        """
        Stores results of MyThread objects
        :param int thread_id: thread ID
        """
        self.thread_id = thread_id
        self.__return_value = []
        self.__error = []

    def set_return_value(self, val):
        self.__return_value.append(val)

    def get_return_value(self):
        return self.__return_value

    def set_error(self, error):
        self.__error.append(error)

    def get_error(self):
        return self.__error



