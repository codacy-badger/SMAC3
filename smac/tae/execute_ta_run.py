import logging
from subprocess import Popen, PIPE

import numpy as np

__author__ = "Marius Lindauer"
__copyright__ = "Copyright 2015, ML4AAD"
__license__ = "3-clause BSD"
__maintainer__ = "Marius Lindauer"
__email__ = "lindauer@cs.uni-freiburg.de"
__version__ = "0.0.1"


class StatusType(object):

    """
        class to define numbers for status types
    """
    SUCCESS = 1
    TIMEOUT = 2
    CRASHED = 3
    ABORT = 4
    MEMOUT = 5


class ExecuteTARun(object):

    """
        executes a target algorithm run with a given configuration
        on a given instance and some resource limitations

        Attributes
        ----------
        ta : string
            the command line call to the target algorithm (wrapper)
    """

    def __init__(self, ta, stats, run_obj="runtime"):
        """
        Constructor

        Parameters
        ----------
            ta : list
                target algorithm command line as list of arguments
            stats: Stats()
                 stats object to collect statistics about runtime and so on                
            run_obj: str
                run objective of SMAC
        """
        self.ta = ta
        self.stats = stats
        self.logger = logging.getLogger("ExecuteTARun")

    def start(self, config, instance,
              cutoff=99999999999999.,
              seed=12345,
              instance_specific="0"):
        """
            wrapper function for ExecuteTARun.run() to check configuration budget before the runs
            and to update stats after run

            Parameters
            ----------
                config : dictionary
                    dictionary param -> value
                instance : string
                    problem instance
                cutoff : double
                    runtime cutoff
                seed : int
                    random seed
                instance_specific: str
                    instance specific information (e.g., domain file or solution)

            Returns
            -------
                status: enum of StatusType (int)
                    {SUCCESS, TIMEOUT, CRASHED, ABORT}
                cost: float
                    cost/regret/quality (float) (None, if not returned by TA)
                runtime: float
                    runtime (None if not returned by TA)
                additional_info: dict
                    all further additional run information
        """

        if self.stats.is_budget_exhausted():
            self.logger.debug(
                "Skip target algorithm run due to exhausted configuration budget")
            return StatusType.ABORT, np.nan, 0, {"misc": "exhausted bugdet -- ABORT"}

        status, cost, runtime, additional_info = self.run(config=config,
                                                          instance=instance,
                                                          cutoff=cutoff,
                                                          seed=seed,
                                                          instance_specific=instance_specific)
        # update SMAC stats
        self.stats.ta_runs += 1
        self.stats.ta_time_used += float(runtime)

        self.logger.debug("Return: Status: %d, cost: %f, time. %f, additional: %s" % (
            status, cost, runtime, str(additional_info)))

        return status, cost, runtime, additional_info

    def run(self, config, instance,
            cutoff=99999999999999.,
            seed=12345,
            instance_specific="0"):
        """
            runs target algorithm <self.ta> with configuration <config> on
            instance <instance> with instance specifics <specifics>
            for at most <cutoff> seconds and random seed <seed>

            Parameters
            ----------
                config : dictionary
                    dictionary param -> value
                instance : string
                    problem instance
                cutoff : double
                    runtime cutoff
                seed : int
                    random seed
                instance_specific: str
                    instance specific information (e.g., domain file or solution)

            Returns
            -------
                status: enum of StatusType (int)
                    {SUCCESS, TIMEOUT, CRASHED, ABORT}
                cost: float
                    cost/regret/quality (float) (None, if not returned by TA)
                runtime: float
                    runtime (None if not returned by TA)
                additional_info: dict
                    all further additional run information
        """
        return StatusType.SUCCESS, 12345.0, 1.2345, {}
