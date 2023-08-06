"""
Handling of assessed ranges
"""
from collections import defaultdict

import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tqdm.autonotebook as tqdman
from matplotlib.gridspec import GridSpec
from scmdata import run_append

from .database import time_mean
from .plotting import CLIMATE_MODEL_PALETTE, CMIP6_NAME
from .stats import get_skewed_normal


def _get_evaluation_axes():
    fig = plt.figure(figsize=(12, 7))
    gs = GridSpec(2, 1, width_ratios=[1], height_ratios=[3, 2])
    ax0 = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1], sharex=ax0)
    axes = [ax0, ax1]

    return axes


def _drop_unwanted_metadata(inp):
    out = inp.copy()
    out_meta = out.meta.columns.tolist()
    out_meta_to_drop = [
        v
        for v in out_meta
        if v
        not in [
            "model",
            "scenario",
            "region",
            "variable",
            "unit",
            "ensemble_member",
            "climate_model",
        ]
    ]
    out.drop_meta(out_meta_to_drop)

    return out


def _convert_unit(res_calc, unit):
    # TODO: check if this is still needed...
    # some scmdata bug requires this workaround...
    units_to_convert = [u for u in res_calc.get_unique_meta("unit") if u != unit]
    if units_to_convert:
        print("Converting {} to {}".format(units_to_convert, unit))
        res_calc_leave = _drop_unwanted_metadata(
            res_calc.filter(unit=unit, log_if_empty=False)
        )
        res_calc_converted = _drop_unwanted_metadata(
            res_calc.filter(unit=unit, keep=False, log_if_empty=False).convert_unit(
                unit
            )
        )

        res_calc = run_append([res_calc_leave, res_calc_converted])

    res_calc = _drop_unwanted_metadata(res_calc)

    return res_calc


class AssessedRanges:
    """
    Class for handling assessed ranges and performing operations with them.

    For example, getting values for specific metrics and plotting results against
    assessed ranges.
    """

    def __init__(self, db):
        """
        Initialise

        Parameters
        ----------
        db : :obj:`pd.DataFrame`
            Assessed ranges data
        """
        self.db = db.copy()

    def head(self, n=5):
        """
        Show head of ``self.db``

        Parameters
        ----------
        n : int
            Number of rows to show

        Returns
        -------
        :obj:`pd.DataFrame`
            Head of ``self.db``
        """
        return self.db.head(n)

    def tail(self, n=5):
        """
        Show tail of ``self.db``

        Parameters
        ----------
        n : int
            Number of rows to show

        Returns
        -------
        :obj:`pd.DataFrame`
            Tail of ``self.db``
        """
        return self.db.tail(n)

    def get_col_for_metric(self, metric, col, single_value=True):
        """
        TODO: docstring
        """
        out = self.db.loc[self.db["RCMIP name"] == metric, col].tolist()

        assert len(out) == 1, "{} {}: {}".format(metric, col, out)

        if not single_value:
            return [v.strip() for v in out[0].split(",")]

        return out[0]

    def get_variables_regions_scenarios_for_metric(self, metric, single_value=True):
        """
        TODO: docstring
        """
        return [
            self.get_col_for_metric(metric, "RCMIP {}".format(ids), single_value=False)
            for ids in ("variable", "region", "scenario")
        ]

    def get_norm_period_evaluation_period(self, metric):
        """
        TODO: docstring
        """
        norm_period_start = self.get_col_for_metric(metric, "norm_period_start")

        norm_period_end = self.get_col_for_metric(metric, "norm_period_end")

        if not np.isnan(norm_period_start) and not np.isnan(norm_period_end):
            norm_period = range(int(norm_period_start), int(norm_period_end) + 1)
        else:
            norm_period = None

        evaluation_period_start = self.get_col_for_metric(
            metric, "evaluation_period_start"
        )

        evaluation_period_end = self.get_col_for_metric(metric, "evaluation_period_end")

        if not np.isnan(evaluation_period_start) and not np.isnan(
            evaluation_period_end
        ):
            evaluation_period = range(
                int(evaluation_period_start), int(evaluation_period_end) + 1
            )
        else:
            evaluation_period = None

        return norm_period, evaluation_period

    def check_norm_period_evaluation_period_against_data(
        self, norm_period, evaluation_period, res_calc
    ):
        """
        TODO: docstring
        """
        res_min_year = res_calc["year"].min()
        res_max_year = res_calc["year"].max()

        if norm_period is not None:
            if res_min_year > min(norm_period):
                raise ValueError(
                    "Res min. year: {}, greater than ref. period min.: {}".format(
                        res_min_year, min(norm_period)
                    )
                )

            if res_max_year < max(norm_period):
                raise ValueError(
                    "Res max. year: {}, less than ref. period max.: {}".format(
                        res_max_year, max(norm_period)
                    )
                )

        if evaluation_period is not None:
            if res_min_year > min(evaluation_period):
                raise ValueError(
                    "Res min. year: {}, greater than evalution period min.: {}".format(
                        res_min_year, min(evaluation_period)
                    )
                )

            if res_max_year < max(evaluation_period):
                raise ValueError(
                    "Res max. year: {}, less than evalution period max.: {}".format(
                        res_max_year, max(evaluation_period)
                    )
                )

    def get_assessed_range_for_boxplot(self, metric):
        """
        TODO: docstring
        """
        value_cols = [
            "very_likely__lower",
            "likely__lower",
            "central",
            "likely__upper",
            "very_likely__upper",
        ]
        values = {
            k: float(self.db.loc[self.db["RCMIP name"] == metric, k].values.squeeze())
            for k in value_cols
        }

        if np.isnan(values["very_likely__lower"]):
            lower = values["likely__lower"]
            upper = values["likely__upper"]
            conf = 0.66
        else:
            lower = values["very_likely__lower"]
            upper = values["very_likely__upper"]
            conf = 0.9

        if np.isnan(values["central"]):
            out = np.zeros(100) * np.nan
        else:
            # generate array which will plot as desired
            out = get_skewed_normal(
                values["central"], lower, upper, conf, np.random.random(2 * 10 ** 4)
            )

        ar_for_boxplot = pd.DataFrame(out, columns=[metric])
        ar_for_boxplot["Source"] = "assessed range"
        ar_for_boxplot["unit"] = self.get_col_for_metric(
            metric, "unit", single_value=True
        )

        return ar_for_boxplot

    def plot_metric_and_results(self, metric, model_results, axes=None):
        """
        TODO: docstring
        """
        if axes is None:
            axes = _get_evaluation_axes()
        else:
            assert len(axes) == 2

        return self._plot(metric, model_results, axs=axes, box_only=False)

    def plot_metric_and_results_box_only(self, metric, model_results, ax=None):
        """
        TODO: docstring
        """
        if ax is None:
            ax = plt.figure().add_subplot(111)

        return self._plot(metric, model_results, axs=ax, box_only=True)

    def _plot(self, metric, model_results, axs, box_only):
        res = model_results.pivot_table(
            values="value",
            columns="RCMIP name",
            index=list(set(model_results.columns) - {"value", "RCMIP name"}),
        ).reset_index()
        res["Source"] = res["climate_model"]
        res["Source"] = res["Source"].apply(
            lambda x: CMIP6_NAME if x.startswith("CMIP6") else x
        )

        ar = self.get_assessed_range_for_boxplot(metric)

        box_plot_df = pd.concat([ar, res])[[metric, "Source", "unit"]]

        unit = box_plot_df["unit"].unique().tolist()
        assert len(unit) == 1, unit

        if box_only:
            box_ax = axs
        else:
            box_ax = axs[1]

        stats = {}
        for source, df in box_plot_df.groupby("Source"):
            data = df[metric].values.squeeze()
            stats[source] = cbook.boxplot_stats(data, labels=[source])[0]
            if source == "SOD assessed range":
                values = self.get_assessed_range_values_for_metric(metric)

                if not np.isnan(values["central"]):
                    stats[source]["med"] = values["central"]
                else:
                    stats[source]["med"] = np.percentile(data, 50)

                if not np.isnan(values["likely__lower"]):
                    stats[source]["q1"], stats[source]["q3"] = (
                        values["likely__lower"],
                        values["likely__upper"],
                    )
                else:
                    stats[source]["q1"], stats[source]["q3"] = np.percentile(
                        data, [17, 83]
                    )

                if not np.isnan(values["very_likely__lower"]):
                    stats[source]["whislo"], stats[source]["whishi"] = (
                        values["very_likely__lower"],
                        values["very_likely__upper"],
                    )
                else:
                    stats[source]["whislo"], stats[source]["whishi"] = np.percentile(
                        data, [5, 95]
                    )

            else:
                stats[source]["q1"], stats[source]["q3"] = np.percentile(data, [17, 83])
                stats[source]["whislo"], stats[source]["whishi"] = np.percentile(
                    data, [5, 95]
                )

        box_ax.bxp(
            list(stats.values()),
            showfliers=False,
            vert=box_only,
            #             rot=90 if box_only else 0,
            #             positions
        )
        box_ax.set_xlabel(unit[0])

        xlim = box_ax.get_xlim()

        if box_only:
            box_ax.set_title(metric)
            box_ax.grid(axis="y")
        else:
            box_ax.set_title("")
            box_ax.grid(axis="x")

        if not box_only:
            pdf_ax = axs[0]
            for label, df in box_plot_df.groupby("Source"):
                sns.distplot(
                    df[metric],
                    bins=50,
                    norm_hist=True,
                    label=label,
                    ax=pdf_ax,
                    color=CLIMATE_MODEL_PALETTE[label],
                )

            pdf_ax.legend()
            pdf_ax.set_title(metric)
            pdf_ax.set_xlim(xlim)
            pdf_ax.set_xlabel("")

        plt.suptitle("")

        return axs

    def get_results_summary_table_for_metric(self, metric, model_results):
        """
        TODO: docstring
        """
        summary_table = defaultdict(list)
        assessed_range_quantiles = {
            "very_likely__lower": 0.05,
            "likely__lower": 0.17,
            "central": 0.5,
            "likely__upper": 0.83,
            "very_likely__upper": 0.95,
        }
        for label, quantile in tqdman.tqdm(
            assessed_range_quantiles.items(), leave=False
        ):
            assessed_value = self.get_col_for_metric(metric, label)
            if np.isnan(assessed_value):
                continue

            for climate_model, df in model_results.groupby("climate_model"):
                model_quantile = df["value"].quantile(quantile)

                summary_table["climate_model"].append(climate_model)
                summary_table["assessed_range_label"].append(label)
                summary_table["assessed_range_value"].append(assessed_value)
                summary_table["climate_model_value"].append(model_quantile)
                summary_table["percentage_difference"].append(
                    (model_quantile - assessed_value) / assessed_value * 100
                )

        summary_table = pd.DataFrame(summary_table)
        summary_table["metric"] = metric
        summary_table["unit"] = self.get_col_for_metric(metric, "unit")

        return summary_table

    def plot_against_results(
        self, results_database, custom_calculations={}, exclude_models=None
    ):
        """
        TODO: docstring
        """
        summary_table = []
        for metric in tqdman.tqdm(self.db["RCMIP name"].tolist()):
            eval_method = self.get_col_for_metric(metric, "RCMIP evaluation method")
            if isinstance(eval_method, float) and np.isnan(eval_method):
                print("No evaluation method for {}".format(metric))
                continue

            (
                variables,
                regions,
                scenarios,
            ) = self.get_variables_regions_scenarios_for_metric(
                metric, single_value=False
            )

            try:
                res_calc = run_append(
                    [
                        results_database.load_data(variable=v, region=r, scenario=s)
                        for v in variables
                        for r in regions
                        for s in scenarios
                    ]
                ).time_mean("AC")
            except IndexError:
                print("No data for: {}".format(metric))
                continue

            res_calc = _drop_unwanted_metadata(res_calc)
            if exclude_models is not None:
                res_calc = res_calc.filter(climate_model=exclude_models, keep=False)

            derived = self.calculate_metric_from_results(
                metric, res_calc, custom_calculations=custom_calculations
            )

            summary_table_metric = self._plot_pdf_and_box_and_get_summary_table(
                metric, derived
            )

            summary_table.append(summary_table_metric)

        summary_table = pd.concat(summary_table).reset_index(drop=True)

        return summary_table

    def plot_model_reported_against_results(self, model_reported):
        """
        TODO: docstring
        """
        summary_table = []

        for label, df in model_reported.groupby("RCMIP name"):
            summary_table_metric = self._plot_pdf_and_box_and_get_summary_table(
                label, df
            )

            summary_table.append(summary_table_metric)

        summary_table = pd.concat(summary_table).reset_index(drop=True)

        return summary_table

    def _plot_pdf_and_box_and_get_summary_table(self, metric, derived):
        axes = _get_evaluation_axes()

        axes = self.plot_metric_and_results(metric, derived, axes=axes)
        plt.tight_layout()

        ax = plt.figure(figsize=(6, 4)).add_subplot(111)
        self.plot_metric_and_results_box_only(metric, derived, ax=ax)

        plt.tight_layout()
        plt.show()

        summary_table_metric = self.get_results_summary_table_for_metric(
            metric, derived
        )

        return summary_table_metric

    def _get_normed_res_calc(self, res_calc, norm_period):
        if norm_period is not None:
            res_calc_normed = res_calc.relative_to_ref_period_mean(year=norm_period)
        else:
            res_calc_normed = res_calc

        return res_calc_normed

    def calculate_metric_from_results(self, metric, res_calc, custom_calculations={}):
        """
        TODO: docstring
        """
        eval_method = self.get_col_for_metric(metric, "RCMIP evaluation method")

        (norm_period, evaluation_period) = self.get_norm_period_evaluation_period(
            metric
        )
        self.check_norm_period_evaluation_period_against_data(
            norm_period, evaluation_period, res_calc
        )

        unit = self.get_col_for_metric(metric, "unit")

        if eval_method == "mean":
            print(norm_period)
            res_calc_normed = self._get_normed_res_calc(res_calc, norm_period)
            res_calc_normed = _convert_unit(res_calc_normed, unit)

            derived = time_mean(res_calc_normed.filter(year=evaluation_period))

            if metric.startswith("Minus"):
                derived *= -1

        elif eval_method == "integral":
            derived = self._calculate_integral(
                res_calc, norm_period, evaluation_period, unit
            )

        elif eval_method == "custom":
            try:
                calc = [c for f, c in custom_calculations.items() if f(metric)][0]

                derived = calc(self, res_calc, norm_period, evaluation_period, unit)

            except IndexError:
                raise IndexError(
                    "No custom method implementation for {}".format(metric)
                )

        else:
            raise NotImplementedError(eval_method)

        derived = derived.to_frame().reset_index()
        derived["RCMIP name"] = metric

        return derived
