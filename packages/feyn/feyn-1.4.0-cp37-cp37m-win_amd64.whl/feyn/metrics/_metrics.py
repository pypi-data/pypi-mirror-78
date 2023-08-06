"""Functions to compute metrics and scores"""

import numpy as np
import typing
import feyn.losses

def accuracy_score(true: typing.Iterable, pred: typing.Iterable) -> float:
    """
    Compute the accuracy score of predictions

    The accuracy score is useful to evaluate classification graphs. It is the fraction of the preditions that are correct. Formally it is defned as

    (number of correct predictions) / (total number of preditions)

    Arguments:
        true -- Expected values
        pred -- Predicted values

    Returns:
        accuracy score for the predictions
    """
    correct = np.equal(true, np.round(pred))
    return np.mean(correct)


def r2_score(true: typing.Iterable, pred: typing.Iterable) -> float:
    """
    Compute the r2 score

    The r2 score for a regression model is defined as 
    1 - rss/tss

    Where rss is the residual sum of squares for the predictions, and tss is the total sum of squares.
    Intutively, the tss is the resuduals of a so-called "worst" model that always predicts the mean. Therefore, the r2 score expresses how much better the predictions are than such a model.

    A result of 0 means that the model is no better than a model that always predicts the mean value
    A result of 1 means that the model perfectly predicts the true value

    It is possible to get r2 scores below 0 if the predictions are even worse than the mean model.

    Arguments:
        true -- Expected values
        pred -- Predicted values

    Returns:
        r2 score for the predictions
    """

    mean = true.mean()
    
    rss = np.sum((true-pred)**2) # Residual sum of squares (this is the squared loss of this predition)
    tss = np.sum((true-mean)**2) # Total sum of squares (this is the squared loss of a model that predicts the mean)

    # r2 score expresses how much better the predictions are compared to a model that predicts the mean
    return 1-rss/tss

def rmse(true: typing.Iterable, pred: typing.Iterable):
    """
    Compute the root mean squared error

    Arguments:
        true -- Expected values
        pred -- Predicted values

    Returns:
        RMSE for the predictions
    """ 
    return np.sqrt(feyn.losses.squared_error(true, pred).mean())        


def confusion_matrix(true: typing.Iterable, pred: typing.Iterable) -> np.ndarray:
    """
    Compute a Confusion Matrix.

    Arguments:
        true -- Expected values (Truth)
        pred -- Predicted values

    Returns:
        [cm] -- a numpy array with the confusion matrix
    """

    classes = np.union1d(pred,true)

    sz = len(classes)
    matrix = np.zeros((sz, sz), dtype=int)
    for tc in range(sz):
        pred_tc = pred[true==classes[tc]]
        for pc in range(sz):
            matrix[(tc,pc)]=len(pred_tc[pred_tc==classes[pc]])
    return matrix


def segmented_loss(graph, data, by=None, loss_function="squared_error"):
    # Magic support for pandas DataFrame
    if type(data).__name__ == "DataFrame":
        data = {col: data[col].values for col in data.columns}

    if by is None:
        by=graph[-1].name
    
    if data[by].dtype == object or len(np.unique(data[by])) < 10:
        return discrete_segmented_loss(graph, data, by, loss_function)
    else:
        return continuous_segmented_loss(graph, data, by, loss_function)


def discrete_segmented_loss(graph, data, by, loss_function):
    loss_function = feyn.losses._get_loss_function(loss_function)
    output = graph[-1].name

    pred = graph.predict(data)

    bins = []
    cnt = []
    stats = []
    for cat in np.unique(data[by]):
        bool_index = data[by] == cat
        subset = {key: values[bool_index] for key, values in data.items()}
        pred_subset = pred[bool_index]

        loss = np.mean(loss_function(subset[output], pred_subset))

        bins.append(cat)
        cnt.append(len(pred_subset))
        stats.append(loss)

    return bins, cnt, stats

def significant_digits(x,p):
    mags = 10 ** (p - 1 - np.floor(np.log10(x)))
    return np.round(x * mags) / mags


def continuous_segmented_loss(graph, data, by, loss_function):
    bincnt = 12
    loss_function = feyn.losses._get_loss_function(loss_function)
    output = graph[-1].name

    pred = graph.predict(data)

    bins = []
    cnt = []
    stats = []

    mn = np.min(data[by])
    mx = np.max(data[by])
    stepsize = significant_digits((mx-mn)/bincnt,2)

    lower = mn
    while lower < mx:
        upper = lower + stepsize

        bool_index = (data[by] >= lower) & (data[by] < upper) 
        subset = {key: values[bool_index] for key, values in data.items()}
        pred_subset = pred[bool_index]

        if len(pred_subset)==0:
            loss = np.nan
        else:
            loss = np.mean(loss_function(subset[output], pred_subset))
        bins.append((lower,upper))
        cnt.append(len(pred_subset))
        stats.append(loss)

        lower = upper

    return bins, cnt, stats

