"""
Module for testing of the zfit components. Contains a singleton instance to register new PDFs and let
them be tested.
"""
#  Copyright (c) 2021 zfit
import sys
from collections import OrderedDict
from typing import Callable, Tuple, List, Union, Iterable

import scipy.stats

from .interfaces import ZfitPDF
from .parameter import ZfitParameterMixin
from ..util.cache import clear_graph_cache
from ..util.container import convert_to_container

__all__ = ["tester", "setup_function", "teardown_function"]

init_modules = sys.modules.keys()


def setup_function():
    # second or subsequent run: remove all but initially loaded modules
    for m in sys.modules.keys():
        if m not in init_modules:
            del (sys.modules[m])


def teardown_function():
    import tensorflow as tf
    ZfitParameterMixin._existing_params.clear()

    clear_graph_cache()
    import zfit
    zfit.run.set_graph_mode()
    for m in sys.modules.keys():
        if m not in init_modules:
            del (sys.modules[m])
    import gc
    gc.collect()


class BaseTester:
    pass


class AutoTester:

    def __init__(self):
        self.pdfs = []

    def register_pdf(self, pdf_class: ZfitPDF, params_factories: Union[Callable, Iterable[Callable]],
                     scipy_dist: scipy.stats.rv_continuous = None,
                     analytic_int_axes: Union[None, int, List[Tuple[int, ...]]] = None):
        # if not isinstance(pdf_class, ZfitPDF):
        #     raise TypeError(f"PDF {pdf_class} is not a ZfitPDF.")
        params_factories = convert_to_container(params_factories)

        if isinstance(analytic_int_axes, tuple):
            raise TypeError(f"`analytic_int_axes` is either a number or a list of tuples.")
        analytic_int_axes = convert_to_container(analytic_int_axes, non_containers=[tuple])
        if analytic_int_axes is not None:
            isinstance(analytic_int_axes)
        registration = OrderedDict((('pdf_class', pdf_class),
                                    ("params", params_factories),
                                    ("scipy_dist", scipy_dist)))
        self.pdfs.append(registration)

    def create_parameterized_pdfs(self):
        if len(self.pdfs) == 0:
            return [], []

        argnames = list(self.pdfs[0].keys())
        argvals = [[] * len(argnames)]

        for pdf in self.pdfs:
            for i, param in enumerate(pdf.values()):
                argvals[i].append(param)

        return argnames, argvals


tester = AutoTester()
