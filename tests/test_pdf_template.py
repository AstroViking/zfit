#  Copyright (c) 2020 zfit
import boost_histogram as bh
import numpy as np
import pytest

import zfit
from zfit.core.binneddata import BinnedData
from zfit.core.binning import RectBinning
from zfit.models.binned_functor import BinnedSumPDF
from zfit.models.template import BinnedTemplatePDF


def test_binned_template_pdf():
    counts = np.random.uniform(high=1, size=(10, 20))  # generate counts
    counts2 = np.random.normal(loc=5, size=(10, 20))
    counts3 = np.linspace(0, 10, num=10)[:, None] * np.linspace(0, 5, num=20)[None, :]

    binnings = [bh.axis.Regular(10, 0, 10), bh.axis.Regular(20, -10, 30)]
    binning = RectBinning(binnings=binnings)
    obs = zfit.Space(obs=['obs1', 'obs2'], binning=binning)

    data = BinnedData.from_numpy(obs=obs, counts=counts, w2error=10)
    data2 = BinnedData.from_numpy(obs=obs, counts=counts2, w2error=10)
    data3 = BinnedData.from_numpy(obs=obs, counts=counts3, w2error=10)

    pdf = BinnedTemplatePDF(data=data)
    pdf2 = BinnedTemplatePDF(data=data2)
    pdf3 = BinnedTemplatePDF(data=data3)
    pdf.set_yield(np.sum(counts))
    pdf2.set_yield(np.sum(counts2))
    pdf3.set_yield(np.sum(counts3))
    assert len(pdf.ext_pdf(None)) > 0
    pdf_sum = BinnedSumPDF(pdfs=[pdf, pdf2, pdf3], obs=obs)

    probs = pdf_sum.ext_pdf(None)
    np.testing.assert_allclose(counts + counts2 + counts3, probs)

    # import matplotlib.pyplot as plt
    # plt.imshow(probs)
    # plt.figure()
    # plt.imshow(counts + counts2 + counts3)
    # plt.show()
