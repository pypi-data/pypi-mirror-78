import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from ._kernelshap import KernelShap


def _plot_colorbar(absmax, cmap='RdYlGn'):
    fig, ax = plt.subplots(figsize=(5, 0.5))
    ax.get_yaxis().set_visible(False)
    ax.set_title('Contribution (SHAP)')
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))

    ax.imshow(gradient, extent=[-absmax, absmax, 0, 1], aspect='auto',
              cmap=plt.get_cmap(cmap))


def _calculating_col_gradient(series, importance_values, absmax, cmap='RdYlGn'):
    """ Parameters:
            series: The series to get the styles for
            importance_values: the values to compute the colors for
            absmax: Highest absolute value
        Returns: styles for a pandas dataframe as a background color gradient"""
    if series.name in importance_values.columns:
        importance_series = importance_values[series.name]
        normalizer = colors.Normalize(-absmax, absmax)
        normed_df = normalizer(importance_series.values)

        colorlist = [colors.rgb2hex(x) for x in plt.cm.get_cmap(cmap)(normed_df)]
        return ['background-color: %s' % color for color in colorlist]
    return ['' for i in range(len(importance_values))]


def _get_percent_color(value, absmax):
    """ Related to a bar chart, returns the percent coloring in either
        direction assuming 50% is the middle
    """
    return 50 + value/absmax*50


def _get_gradient_string(value):
    if value > 50:
        # Try to make sure you can always see the sliver of contribution, even if it's small.
        value = max(53, value)
        return f"background: linear-gradient(90deg, transparent 50.0%, #5fba7d 50.0%, #5fba7d {value}%, transparent {value}%)"
    elif value < 50:
        value = min(47, value)
        return f"background: linear-gradient(90deg, transparent {value}%, #d65f5f {value}%, #d65f5f 50.0%, transparent 50.0%)"
    else:
        return 'background-color: #feffbe'


def _calculating_col_gradient_bar(series, importance_values, absmax):
    """ Parameters:
            series: The series to get the styles for
            importance_values: the values to compute the colors for
            absmax: Highest absolute value
        Returns: styles for a pandas dataframe as a bar chart """
    if series.name in importance_values.columns:
        importance_series = importance_values[series.name]
        percentages = [_get_percent_color(v, absmax) for v in importance_series.values]
        return [_get_gradient_string(pct) for pct in percentages]
    return ['' for i in range(len(importance_values))]


def _handle_ensemble(ensembler, dataframe, bg_data):
    importances = pd.DataFrame([], columns=dataframe.columns)
    bg_importances = pd.DataFrame([], columns=bg_data.columns)

    # pd.concat will add multiple entries for the same index value
    for graph in ensembler.graphs:
        explainer = KernelShap(graph, bg_data)

        # Reset indices to avoid duplicate indices in case they exist as it will contaminate aggregation. Restore index after aggregation.
        bg_imp = explainer.SHAP(bg_data.reset_index(), format='pandas')
        bg_imp['index'] = bg_data.index
        imp = explainer.SHAP(dataframe.reset_index(), format='pandas')
        imp['index'] = dataframe.index
        bg_importances = pd.concat([bg_importances, bg_imp], sort=True)
        importances = pd.concat([importances, imp], sort=True)

    # fill NA's with 0, group by the index, and aggregate with the mean to average over each graphs shap value per sample, then restore previous index.
    avg_importances = importances.fillna(0).groupby(by=importances.index).agg('mean').set_index('index', drop=True)
    avg_bg_importances = bg_importances.fillna(0).groupby(by=bg_importances.index).agg('mean').set_index('index', drop=True)

    return avg_importances, avg_bg_importances


def _get_absmax(x):
    return max(x.values.max(), np.abs(x.values.min()))


def plot_importance_dataframe(graph, dataframe, bg_data=None, kind='bar', legend=True, cmap='RdYlGn'):
    """ Paints a Pandas DataFrame according to feature importance in the provided model.
        Parameters:
            graph: The feyn graph to predict on
            dataframe: The dataframe to paint
            [bg_data]: The dataframe to use for background data to get more accurate importance scores
            [kind]: The kind of coloring. Options: 'fill' or 'bar'
            [cmap]: The colormap to use (if kind='fill')
        Returns:
            A Styled Pandas DataFrame with a color gradient heatmap or the cells as bar charts according to feature importances. """

    # Special handle if you're using an ensemble method.
    if 'FeynEnsemble' in str(type(graph)):
        if bg_data is None:
            bg_data = dataframe
        importance_values, bg_importance = _handle_ensemble(graph, dataframe, bg_data)
    elif bg_data is not None:
        shap_explainer = KernelShap(graph, bg_data)
        bg_importance = shap_explainer.SHAP(bg_data, format='pandas')
        importance_values = shap_explainer.SHAP(dataframe, format='pandas')
    else:
        shap_explainer = KernelShap(graph, dataframe)
        importance_values = shap_explainer.SHAP(dataframe, format='pandas')

    # TODO: Clean up the if/else statements a bit to reduce duplication.
    # Maybe always set bg_data to dataframe if none and accept double work?

    if bg_data is not None:
        absmax = _get_absmax(bg_importance)
    else:
        absmax = _get_absmax(importance_values)

    if kind not in ['bar', 'fill']:
        raise Exception(f"Kind {kind} not recognized. Must be either 'bar' or 'fill'")
    if kind == 'bar':
        painted_df = dataframe.style.apply(_calculating_col_gradient_bar,
                                           importance_values=importance_values,
                                           absmax=absmax)
    elif kind == 'fill':
        painted_df = dataframe.style.apply(_calculating_col_gradient,
                                           importance_values=importance_values,
                                           absmax=absmax,
                                           cmap=cmap)
        if legend:
            _plot_colorbar(absmax, cmap=cmap)

    return painted_df
