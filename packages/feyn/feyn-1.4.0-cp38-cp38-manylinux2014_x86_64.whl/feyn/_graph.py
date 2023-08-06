"""A graph is a path from some input registers to an output register.

The graph is a result of running a simulation. It is one of the many possible paths from the inputs to the output. It can be compared to a model in various other machine learning frameworks.
"""
import json
from pathlib import Path
from typing import AnyStr, TextIO, Union, Iterable, Optional

import numpy as np

import _feyn
import feyn

# Update this number whenever there are breaking changes to save/load
# (or to_dict/from_dict). Then use it intelligently in Graph.load.
SCHEMA_VERSION = "2020-02-07"

PathLike = Union[AnyStr, Path]


class Graph(_feyn.Graph):
    """
    A Graph represents a single mathematical model which can be used used for predicting.

    The constructor is for internal use. You will typically use `QGraph[ix]` to pick graphs from QGraphs, or load them from a file with Graph.load().

    Arguments:
        size -- The number of nodes this graph contains. The actual nodes must be added to the graph after construction.
    """

    def __init__(self, size: int):
        """Construct a new 'Graph' object."""
        super().__init__(size)

        self.loss_value = np.nan
        self.age = 0

    def predict(self, X) -> np.ndarray:
        """
        Calculate predictions based on input values.

        >>> graph.predict({ "age": [34, 78], "sex": ["male", "female"] })
        [True, False]

        Arguments:
            X -- The input values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            np.ndarray -- The calculated predictions.
        """
        if type(X).__name__ == 'dict':
            for k in X:
                if type(X[k]).__name__ == 'list':
                    X[k] = np.array(X[k])

        # Magic support for pandas DataFrame
        if type(X).__name__ == "DataFrame":
            X = {col: X[col].values for col in X.columns}

        return super()._query(X, None)

    @property
    def edges(self) -> int:
        """Get the total number of edges in this graph."""
        return super().edge_count

    @property
    def depth(self) -> int:
        """Get the depth of the graph"""
        return self[-1].depth

    @property
    def features(self):
        return [i.name for i in self if i.spec.startswith("in:")]

    def save(self, file: Union[PathLike, TextIO]) -> None:
        """
        Save the `Graph` to a file-like object.

        The file can later be used to recreate the `Graph` with `Graph.load`.

        Arguments:
            file -- A file-like object or path to save the graph to.
        """
        as_dict = self._to_dict()
        as_dict["version"] = SCHEMA_VERSION

        if isinstance(file, (str, bytes, Path)):
            with open(file, mode="w") as f:
                json.dump(as_dict, f)
        else:
            json.dump(as_dict, file)

    @staticmethod
    def load(file: Union[PathLike, TextIO]) -> "Graph":
        """
        Load a `Graph` from a file.

        Usually used together with `Graph.save`.

        Arguments:
            file -- A file-like object or a path to load the `Graph` from.

        Returns:
            Graph -- The loaded `Graph`-object.
        """
        if isinstance(file, (str, bytes, Path)):
            with open(file, mode="r") as f:
                as_dict = json.load(f)
        else:
            as_dict = json.load(file)

        return Graph._from_dict(as_dict)

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        return other.__hash__() == self.__hash__()

    def __contains__(self, item:str):
        return item in [interaction.name for interaction in self]

    def _fit(self, data, loss_function, sample_weights=None):
        out_reg = self[-1]
        Y = data[out_reg.name]

        out_reg._loss = loss_function.c_derivative

        predictions = super()._query(data, Y, sample_weights)
        losses = loss_function(Y.astype(float), predictions)
        if sample_weights is not None:
            losses *= sample_weights
        self.loss_value = np.mean(losses)

        return self.loss_value

    def _to_dict(self):
        nodes = []
        links = []
        for ix in range(len(self)):
            interaction = self[ix]
            nodes.append({
                "id": interaction._index,
                "spec": interaction.spec,
                "location": interaction._latticeloc,
                "peerlocation": interaction._peerlocation,
                "legs": len(interaction.sources),
                "strength": interaction._strength,
                "name": interaction.name,
                "state": interaction.state._to_dict()
            })
            for ordinal, src in enumerate(interaction.sources):
                if src != -1:
                    links.append({
                        'source': src,
                        'target': interaction._index,
                        'ord': ordinal
                    })

        return {
            'directed': True,
            'multigraph': True,
            'nodes': nodes,
            'links': links
        }

    def _repr_svg_(self):
        return feyn._current_renderer.rendergraph(self)

    @staticmethod
    def _get_interaction(data: dict) -> _feyn.Interaction:
        interaction = feyn.Interaction(data["spec"], tuple(data["location"]), peerlocation=data["peerlocation"], strength=data["strength"], name=data["name"])
        interaction.state._from_dict(data["state"])

        return interaction

    @staticmethod
    def _from_dict(gdict):
        sz = len(gdict["nodes"])
        graph = Graph(sz)
        for ix, node in enumerate(gdict["nodes"]):
            interaction = Graph._get_interaction(node)
            graph[ix] = interaction

        for edge in gdict["links"]:
            interaction = graph[edge["target"]]
            ord = edge["ord"]
            interaction._set_source(ord, edge["source"])
        return graph




    def squared_error(self, data:Iterable):
        """
        Compute the graph's squared error loss on the provided data.

        This function is a shorthand that is equivalent to the following code:
        > y_true = data[<output col>]
        > y_pred = graph.predict(data)
        > se = feyn.losses.squared_error(y_true, y_pred)

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            nd.array -- The losses as an array of floats.

        """
        output = self[-1].name

        pred = self.predict(data)
        return feyn.losses.squared_error(data[output], pred)

    def absolute_error(self, data:Iterable):
        """
        Compute the graph's absolute error on the provided data.

        This function is a shorthand that is equivalent to the following code:
        > y_true = data[<output col>]
        > y_pred = graph.predict(data)
        > se = feyn.losses.absolute_error(y_true, y_pred)

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            nd.array -- The losses as an array of floats.

        """
        output = self[-1].name

        pred = self.predict(data)
        return feyn.losses.absolute_error(data[output], pred)

    def binary_cross_entropy(self, data:Iterable):
        """
        Compute the graph's binary cross entropy on the provided data.

        This function is a shorthand that is equivalent to the following code:
        > y_true = data[<output col>]
        > y_pred = graph.predict(data)
        > se = feyn.losses.binary_cross_entropy(y_true, y_pred)

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            nd.array -- The losses as an array of floats.

        """
        output = self[-1].name

        pred = self.predict(data)
        return feyn.losses.binary_cross_entropy(data[output], pred)

    def accuracy_score(self, data: Iterable):
        """
        Compute the graph's accuracy score on a data set

        The accuracy score is useful to evaluate classification graphs. It is the fraction of the preditions that are correct. Formally it is defned as

        (number of correct predictions) / (total number of preditions)

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            accuracy score for the predictions
        """

        output = self[-1].name

        pred = self.predict(data)
        return feyn.metrics.accuracy_score(data[output], pred)

    def r2_score(self, data: Iterable):
        """
        Compute the graph's r2 score on a data set

        The r2 score for a regression model is defined as 
        1 - rss/tss

        Where rss is the residual sum of squares for the predictions, and tss is the total sum of squares.
        Intutively, the tss is the resuduals of a so-called "worst" model that always predicts the mean. Therefore, the r2 score expresses how much better the predictions are than such a model.

        A result of 0 means that the model is no better than a model that always predicts the mean value
        A result of 1 means that the model perfectly predicts the true value

        It is possible to get r2 scores below 0 if the predictions are even worse than the mean model.

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            r2 score for the predictions
        """

        output = self[-1].name

        pred = self.predict(data)
        return feyn.metrics.r2_score(data[output], pred)


    def rmse(self, data):
        """
        Compute the graph's root mean squared error on a data set

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            RMSE for the predictions
        """ 
        return np.sqrt(self.squared_error(data).mean())        


    def plot_confusion_matrix(self,
                            data: Iterable,
                            labels: Iterable=None,
                            title:str='Confusion matrix',
                            color_map="abzu-partial",
                            ax=None) -> None:

        """
        Compute and plot a Confusion Matrix.

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.
            labels -- List of labels to index the matrix
            title -- Title of the plot.
            color_map -- Color map from matplotlib to use for the matrix
            ax -- matplotlib axes object to draw to, default None
        Returns:
            [plot] -- matplotlib confusion matrix
        """

        output = self[-1].name

        pred = self.predict(data).round()
        feyn.plots.plot_confusion_matrix(data[output], pred, labels, title, color_map, ax)


    def plot_regression_metrics(self, data: Iterable, title:str="Regression metrics", ax=None ) -> None:
        """
        Plot the graph's metrics for a regression.

        This is a shorthand for calling feyn.plots.plot_regression_metrics.

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.
            title -- Title of the plot.
            ax -- matplotlib axes object to draw to, default None

        """

        output = self[-1].name

        pred = self.predict(data)
        feyn.plots.plot_regression_metrics(data[output], pred, title, ax)


    def plot_segmented_loss(self, data:Iterable, by:Optional[str] = None, loss_function="squared_error", title="Segmented Loss", ax=None) -> None:
        """
        Plot the loss by segment of a dataset.

        This plot is useful to evaluate how a model performs on different subsets of the data.

        Example:
        > qg = qlattice.get_regressor(["age","smoker","heartrate"], output="heartrate")
        > qg.fit(data)
        > best = qg[0]
        > feyn.plots.plot_segmented_loss(best, data, by="smoker")

        This will plot a histogram of the model loss for smokers and non-smokers separately, which can help evaluate wheter the model has better performance for euther of the smoker sub-populations.

        You can use any column in the dataset as the `by` parameter. If you use a numerical column, the data will be binned automatically.

        Arguments:
            data -- The dataset to measure the loss on.
            by -- The column in the dataset to segment by.
            loss_function -- The loss function to compute for each segmnent,
            title -- Title of the plot.
            ax -- matplotlib axes object to draw to
        """

        feyn.plots.plot_segmented_loss(self, data, by=by, loss_function=loss_function, title=title, ax=ax)

    def plot_roc_curve(self, data: Iterable, title:str="ROC curve", ax=None, **kwargs) -> None:
        """
        Plot the graph's ROC curve.

        This is a shorthand for calling feyn.plots.plot_roc_curve.

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.
            title -- Title of the plot.
            ax -- matplotlib axes object to draw to, default None
            **kwargs -- additional options to pass on to matplotlib    
        """
        output = self[-1].name

        pred = self.predict(data)
        feyn.plots.plot_roc_curve(data[output], pred, title, ax, **kwargs)


    def plot_summary(self, data:Iterable):
        """
        Plot the graph's summary metrics and show the signal path.

        This is a shorthand for calling feyn.plots.plot_graph_summary.

        Arguments:
            data -- Data set including both input and expected values. Must be a pandas.DataFrame.
        """
        return feyn.plots._graph_summary.plot_graph_summary(self, data)
