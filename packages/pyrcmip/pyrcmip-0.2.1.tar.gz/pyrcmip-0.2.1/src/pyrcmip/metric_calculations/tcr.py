"""
Calculation of the transient climate response (TCR)
"""
from ..database import time_mean


def calculate_transient_climate_response(
    assessed_ranges, res_calc, norm_period, evaluation_period, unit
):
    """
    Calculate the transient climate response (TCR)

    Parameters
    ----------
    assessed_ranges : :obj:`pyrcmip.assessed_ranges.AssessedRanges`
        Assessed ranges instance

    res_calc : :obj:`scmdata.ScmRun`
        Results from which the TCR is to be derived

    norm_period : list
        Years to use for normalising the data before calculating the TCR

    evaluation_period : list
        Years to use when evaluating the TCR

    unit : str
        Unit in which the TCR should be returned

    Returns
    -------
    :obj:`pd.DataFrame`
        TCR with other relevant model metadata

    Raises
    ------
    NotImplementedError
        The evaluation period is not the year 1920 i.e. the experiment does
        not match the CMIP6 specifications
    """
    res_calc_normed = assessed_ranges._get_normed_res_calc(res_calc, norm_period)

    if evaluation_period is not None and (
        len(evaluation_period) != 1 or evaluation_period[0] != 1920
    ):
        raise NotImplementedError(
            "Evaluation period other than [1920], input: {}".format(evaluation_period)
        )

    return time_mean(
        res_calc_normed.filter(
            scenario="1pctCO2",
            variable="Surface Air Temperature Change",
            unit=unit,
            region="World",
            year=range(1920, 1921),
        )
    )
