"""
Multithreading Class base on threading.Thread
"""

import logging
import sys
import threading
import traceback

MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class GenericThreadWorker(threading.Thread):
    """
    Generic Thread worker

    Args:
        function (function): function to submit to Process
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """

    log = False

    def __init__(self, function, *args, **kwargs):
        super(GenericThreadWorker, self).__init__()

        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """
        Override run initialise and starts the worker function
        with passed args, kwargs.
        """

        try:
            self.function(*self.args, **self.kwargs)
        except:  # pylint: disable=bare-except
            traceback.print_exc()

        return


class QueueThreadWorker(threading.Thread):
    """
    Generic Queue process Thread worker

    Args:
        queue (Queue): Queue to process
        function (function): function to submit to Process
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """

    log = False

    def __init__(self, queue, function, *args, **kwargs):
        super(QueueThreadWorker, self).__init__()

        self.queue = queue
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """
        Override run gets next job from queue. The initialise and
        starts the worker function with passed args, kwargs and
        nextJob.
        """

        while True:
            # Get the work from the queue and expand the tuple
            nextJob = self.queue.get()
            try:
                self.function(nextJob, *self.args, **self.kwargs)
            finally:
                self.queue.task_done()


class ThreadWorker(threading.Thread):
    """
    Worker thread

    Inherits from threading.Tread to handle worker thread setup, signals and wrap-up.

    Args:
        function (function): Function to submit to Thread.
        funcFinished (function): Call back function when thread finishes.
        funcError (function): Call back function when an error occurs.
        funcResult (function): Call back function with the result of the execution.
        funcStart (function): Call back function when an Thread is about to start.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """

    log = False

    def __init__(self,
                 function,
                 *args,
                 **kwargs):
        super(ThreadWorker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.function = function
        self.args = args

        # remove optional known named parameters
        self.funcStart = kwargs.pop('funcStart', None)
        self.funcFinished = kwargs.pop('funcFinished', None)
        self.funcError = kwargs.pop('funcError', None)
        self.funcResult = kwargs.pop('funcResult', None)

        self.kwargs = kwargs # pass rest of named parameters to self.function

    def run(self):
        """
        Override run initialise and starts the worker function
        with passed args, kwargs.
        """

        if callable(self.funcStart):
            self.funcStart()  # Done

        # Retrieve args/kwargs here; and fire processing using them
        # pylint: disable-msg=W0702
        # have to capture all exceptions using sys.exc_info()
        # to sort out what is happening
        try:
            result = self.function(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            excepttype, value = sys.exc_info()[:2]
            if callable(self.funcError):
                self.funcError((excepttype, value, traceback.format_exc()))
        else:
            if callable(self.funcResult):
                self.funcResult(result)  # Return the result of the processing
        finally:
            if callable(self.funcFinished):
                self.funcFinished()  # Done
