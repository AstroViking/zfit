import abc

import tensorflow as tf
from typing import Optional, Union

from zfit import ztf
from .baseobject import BaseObject, BaseDependentsMixin
from .interfaces import ZfitLoss
from ..models.functions import SimpleFunc
from ..util.container import convert_to_container, is_container

from .limits import convert_to_space, Space


def _unbinned_nll_tf(model, data, fit_range, constraints: Optional[dict] = None) -> tf.Tensor:
    """Return unbinned negative log likelihood graph for a PDF

    Args:
        fit_range ():
        model (Tensor): The probabilities
        constraints (dict): A dictionary containing the constraints for certain parameters. The key
            is the parameter while the value is a pdf with at least a `pdf(x)` method.

    Returns:
        graph: the unbinned nll

    Raises:
        ValueError: if both `probs` and `log_probs` are specified.
    """

    if is_container(model):
        nlls = [_unbinned_nll_tf(model=p, data=d, fit_range=r)
                for p, d, r in zip(model, data, fit_range)]
        nll_finished = tf.reduce_sum(nlls)
    else:  # TODO: complicated limits?
        fit_range = model.convert_sort_space(fit_range)
        limits = fit_range.limits
        assert len(limits[0]) == 1, "multiple limits not (yet) supported in nll."
        (lower,), (upper,) = limits

        # TODO(Mayou36): implement properly data cutting
        # in_limits = tf.logical_and(lower <= data, data <= upper)
        # data = tf.boolean_mask(tensor=data, mask=in_limits)
        log_probs = tf.log(model.pdf(data, norm_range=fit_range))
        nll = -tf.reduce_sum(log_probs)
        nll_finished = nll
    return nll_finished


def _nll_constraints_tf(constraints):
    if not constraints:
        return ztf.constant(0.)  # adding 0 to nll
    probs = []
    for param, dist in constraints.items():
        probs.append(dist.pdf(param))
    # probs = [dist.pdf(param) for param, dist in constraints.items()]
    constraints_neg_log_prob = -tf.reduce_sum(tf.log(probs))
    return constraints_neg_log_prob


#
# def extended_unbinned_NLL(pdfs, integrals, n_obs, nsignals,
#                           param_gauss=None, param_gauss_mean=None, param_gauss_sigma=None,
#                           log_multi_gauss=None):
#     """
#     Return unbinned negative log likelihood graph for a PDF
#     pdfs       : concatenated array of several PDFs (different regions/channels)
#     integrals  : array of precalculated integrals of the corresponding pdfs
#     n_obs       : array of observed num. of events, used in the extended fit and in the
#     normalization of the pdf
#                  (needed since when I concatenate the pdfs I loose the information on how many
#                  data points are fitted with the pdf)
#     nsignals   : array of fitted number of events resulted from the extended fit (function of the
#     fit parameters, prop to BR)
#     param_gauss : list of parameter to be gaussian constrained (CKM pars, etc.)
#     param_gauss_mean : mean of parameter to be gaussian constrained
#     param_gauss_sigma : sigma parameter to be gaussian constrained
#     log_multi_gauss : log of the multi-gaussian to be included in the Likelihood (FF & alphas)
#     """
#     # tf.add_n(log(pdf(x))) - tf.add_n(Nev*Norm)
#     nll = - (tf.reduce_sum(tf.log(pdfs)) - tf.reduce_sum(
#         tf.cast(n_obs, tf.float64) * tf.log(integrals)))
#
#     # Extended fit to number of events
#     nll += - tf.reduce_sum(-nsignals + tf.cast(n_obs, tf.float64) * tf.log(nsignals))
#
#     # gaussian constraints on parameters (CKM) # tf.add_n( (par-mean)^2/(2*sigma^2) )
#     if param_gauss is not None:
#         nll += tf.reduce_sum(
#             tf.square(param_gauss - param_gauss_mean) / (2. * tf.square(param_gauss_sigma)))
#
#     # multivariate gaussian constraints on param that have correlations (alphas, FF)
#     if log_multi_gauss is not None:
#         nll += - log_multi_gauss
#
#     return nll


class BaseLoss(BaseObject, BaseDependentsMixin, ZfitLoss):

    def __init__(self, model, data, fit_range, constraints=None):
        super().__init__(name=type(self).__name__)
        if constraints is None:
            constraints = {}
        model, data, fit_range = self._input_check(pdf=model, data=data, fit_range=fit_range)
        self._model = model
        self._data = data
        self._fit_range = fit_range
        self._constraints = constraints.copy()

    def __init_subclass__(cls, **kwargs):
        cls._name = "UnnamedSubBaseLoss"

    def _input_check(self, pdf, data, fit_range):
        if is_container(pdf) ^ is_container(data):
            raise ValueError("`pdf` and `data` either both have to be a list or not.")

        # simultaneous fit
        if is_container(pdf):
            if not is_container(fit_range) or not isinstance(fit_range[0], Space):
                raise ValueError(
                    "If several pdfs are specified, the `fit_range` has to be given as a list of `Space` "
                    "objects and not as pure tuples.")
            if not len(pdf) == len(data) == len(fit_range):
                raise ValueError("pdf, data and fit_range don't have the same number of components:"
                                 "\npdfs: {}"
                                 "\ndata: {}"
                                 "\nfit_range: {}".format(pdf, data, fit_range))

        else:
            fit_range = pdf.convert_sort_space(limits=fit_range)  # fit_range may be a tuple and
            # therefore is a container already!
        # convert everything to containers
        pdf, data, fit_range = (convert_to_container(obj) for obj in (pdf, data, fit_range))
        # sanitize fit_range
        fit_range = [p.convert_sort_space(limits=range_) for p, range_ in zip(pdf, fit_range)]
        # TODO: sanitize pdf, data?

        return pdf, data, fit_range

    def add_constraints(self, constraints):
        if not isinstance(constraints, dict):
            raise TypeError("`constraint` has to be a dict, is currently {}".format(type(constraints)))
        overwritting_keys = set(constraints).intersection(self._constraints)
        if overwritting_keys:
            raise ValueError("Cannot change existing constraints but only add (currently). Constrain for "
                             "parameter(s) {} already there.".format(overwritting_keys))
        self._constraints.update(constraints)

    @property
    def name(self):
        return self._name

    @property
    def model(self):
        return self._model

    @property
    def data(self):
        return self._data

    @property
    def fit_range(self):
        fit_range = self._fit_range
        return fit_range

    @property
    def constraints(self):
        return self._constraints

    def _get_dependents(self):
        pdf_dependents = self._extract_dependents(self.model)
        return pdf_dependents

    @abc.abstractmethod
    def _loss_func(self, model, data, fit_range, constraints):
        raise NotImplementedError

    def value(self):
        try:
            return self._loss_func(model=self.model, data=self.data, fit_range=self.fit_range,
                                   constraints=self.constraints)
        except NotImplementedError:
            raise NotImplementedError("_loss_func not properly defined!")

    def __add__(self, other):
        if not isinstance(other, BaseLoss):
            raise TypeError("Has to be a subclass of `BaseLoss` or overwrite `__add__`.")
        if not type(other) == type(self):
            raise ValueError("cannot safely add two different kind of loss.")
        model = self.model + other.model
        data = self.data + other.data
        fit_range = self.fit_range + other.fit_range
        loss = type(self)(model=model, data=data, fit_range=fit_range, constraints=self.constraints)
        loss.add_constraints(constraints=other.constraints)
        return loss


class UnbinnedNLL(BaseLoss):
    _name = "UnbinnedNLL"

    def _loss_func(self, model, data, fit_range, constraints):
        nll = _unbinned_nll_tf(model=model, data=data, fit_range=fit_range)
        constraints = _nll_constraints_tf(constraints=constraints)
        nll_constr = nll + constraints
        return nll_constr

    def errordef(self, sigma: Union[float, int]) -> Union[float, int]:
        return sigma


class SimpleLoss(BaseLoss):
    _name = "SimpleLoss"

    def __init__(self, func):
        self._simple_func = func
        model= SimpleFunc(func=func, obs='obs1')
        super().__init__(model=model, data=None, fit_range=False)

    def errordef(self, func):
        raise NotImplementedError("For this simple loss function, no error calculation is possible.")

    def _loss_func(self, model, data, fit_range, constraints=None):
        loss = self._simple_func
        return loss()