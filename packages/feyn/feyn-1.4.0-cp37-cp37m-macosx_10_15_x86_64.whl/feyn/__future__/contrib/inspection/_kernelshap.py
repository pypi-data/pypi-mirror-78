import pandas as pd
import numpy as np
import math

from itertools import permutations
import matplotlib.pyplot as plt
from IPython.display import display

class KernelShap:
    """
    This class approximates SHAP values of a feyn.Graph object.
    SHAP values are based on conditional expectations which means that it requires data in order to calculate SHAP values.

    Typically this data will be the training set.

    The computation time scales exponentially with the amount of features, and scales linearly by datapoints.
    """
    def __init__(self, graph, background_data):
        """
        Constructs a new 'KernelShap' object

        Arguments:
            graph {feyn.Graph} -- A feyn Graph object
            background_data {pandas.DataFrame} -- Usually the train DataFrame, that the model was fitted to.
        """
        self.graph = graph
        self.data = background_data.copy()
        self.features = self._get_features()
        self.base_value = np.average(self._get_prediction(self.data))

    def _get_features(self):
        not_features = ['', self.graph[-1].name]  # The final node is the output node
        return [interaction.name for interaction in self.graph
                    if interaction.name not in not_features]

    def _get_prediction(self, data):
        return self.graph.predict(data)

    def SHAP(self, instances, n_samples='auto', format='numpy'):
        """
        Approximates the SHAP values of instances.

        Keyword arguments:
            instances -- A collection of datapoints that one wants to find their SHAP values. This is a pandas.DataFrame object
            n_samples -- This is either 'auto' or an integer. When n_samples in an integer it is amount of sampling for each combination of subsets of the features in the model. The higher the number the more accurate the approximation but the slower the calculation.
            The keyword 'auto' varies the amount of sampling for each combination. More samples are taking with the smallest and largest subsets. Less for the subsets that are about half the size of the full subset of features.
            format -- Either 'numpy' or 'pandas'. Determines what format the return values should be

        Returns:
            numpy.array --- Size #instances x #features where each entry represets the SHAP values of that feature for that particular instance.
            pandas.DataFrame --- Each row is an instance and the columns are the SHAP values of the feature.,
        """
        data = instances.copy()
        solutions = self._lo_solver(data, n_samples=n_samples)

        reshaped_solutions = solutions.sum(axis=1).reshape((len(data),))
        final_feat_SHAP = self._get_prediction(data) - reshaped_solutions - self.base_value

        reshaped_final_feat = final_feat_SHAP.reshape((len(data), 1, 1))
        rows = np.reshape(np.hstack((solutions, reshaped_final_feat)), newshape=(len(data), len(self.features)))
        if format == 'numpy':
            return rows
        if format == 'pandas':
            cols = [col for col in self.features]
            return pd.DataFrame(data=rows, index=data.index, columns=cols)

    def feature_plot(self, shap_values, figsize=(8, 4), show_graph=True):
        """
        Finds feature importance from calculated SHAP values. This calculates the mean of the absolute value of each feature.

        Keyword arguments:
            shap_values --- A numpy array of shap values of chosen instances.
            figsize --- A tuple that determines the size of the figure.
            show_graph --- Boolean that displays the graph along with the figure.

        Returns:
            matplotlib horizontal bar chart. On the y-axis is each feature and the x-axis the mean absolute value of each feature.
        """

        abs_shap_values = np.absolute(shap_values)
        abs_ave = np.average(abs_shap_values, axis=0)

        z_features_avers = list(zip(self.features, abs_ave))
        z_features_avers.sort(key=lambda x: x[1], reverse=False)
        z_features_avers = pd.DataFrame(z_features_avers)

        fig, ax = plt.subplots(figsize=figsize)

        ax.barh(z_features_avers[0], width=z_features_avers[1], color='teal', edgecolor='fuchsia', lw=1.5)
        ax.set_xlabel('mean absolute SHAP value', fontsize=12)
        ax.set_title('Feature importance', fontsize=13)

        if show_graph:
            display(self.graph)

        return fig

    def _lo_solver(self, instances, n_samples='auto'):
        coalition_matrix = self._coalition_matrix()
        CM_shape = np.shape(coalition_matrix)

        TrCM_x_model = KernelShap._trim_matrix(coalition_matrix, column_index=[0])
        x_model_output = self._explainer_model(TrCM_x_model, instances, n_samples)
        _hat_x_model = self._y_hat(x_model_output)

        TrCM_solv_lo = KernelShap._trim_matrix(coalition_matrix, row_index=[0, CM_shape[0] - 1], column_index=[0, CM_shape[1] - 1])

        TrCM_final_col = KernelShap._trim_matrix(coalition_matrix, row_index=[0, CM_shape[0] - 1], column_index=[i for i in range(CM_shape[1] - 1)])
        TrCM_fin_col_mat = KernelShap._col_into_matrix(TrCM_final_col, number_of_cols=np.shape(TrCM_solv_lo)[1])

        LO_matrix = np.array([TrCM_solv_lo - TrCM_fin_col_mat for i in range(len(instances))])

        kernel = self._kernel_matrix()
        kernels = np.array([kernel for i in range(len(instances))])
        LO_sol = KernelShap._linearoptimizer(LO_matrix, kernels, _hat_x_model)

        return LO_sol

    def _kernel_matrix(self):
        coal_mat = self._coalition_matrix()
        CM_shape = np.shape(coal_mat)
        tr_mat = KernelShap._trim_matrix(coal_mat, row_index=[0, CM_shape[0] - 1], column_index=[0])

        no_features = len(self.features)
        nonzero_feat = np.sum(tr_mat, axis=1)
        denom = np.multiply(np.multiply(KernelShap._binom(no_features, nonzero_feat), nonzero_feat), (no_features - nonzero_feat))
        nom = no_features - 1
        return np.diag(np.divide(nom, denom))

    def _y_hat(self, y):
        coal_mat_shape = np.shape(self._coalition_matrix())
        zp = KernelShap._trim_matrix(self._coalition_matrix(),
                                     row_index=[0, coal_mat_shape[0] - 1],
                                     column_index=[i for i in range(coal_mat_shape[1] - 1)])

        trim_y = np.array([KernelShap._trim_matrix(x, row_index=[0, np.shape(x)[0] - 1]) for x in y])
        instance_eval = [y[i][-1][0] for i in range(np.shape(y)[0])]
        return trim_y - np.array([np.multiply(zp, x) for x in instance_eval]) - np.multiply(1 - zp, self.base_value)

    def _coalition_matrix(self):
        amount_of_subsets = 2 ** len(self.features)
        ls = []
        for subset in range(amount_of_subsets):
            ls.append([int(i) for i in "1"+("{:0"+str(len(self.features)) + "b}").format(subset)])
        return np.array(ls)

    def _replace_sample_with_instance(self, dataframe, binary, instance):
        copy_dataframe = dataframe.copy()
        features_from_instance = [self.features[k] for k in range(len(self.features)) if binary[k] == 1]
        copy_dataframe[features_from_instance] = instance[features_from_instance].values[0]
        return copy_dataframe

    def _array_to_dict(self, array):
        return {self.features[j]: array[:, j] for j in range(len(self.features))}

    def _explainer_model(self, matrix, instances, n_samples='auto'):
        output = np.zeros(shape=(len(instances), matrix.shape[0], 1))
        if n_samples == 'auto':
            if len(self.data) < 10000:
                sample_size = [len(self.data)] * matrix.shape[1]
            else:
                len_of_feat = len(self.features)
                ls = [i for i in range(1, int(len_of_feat / 2)+1)] + \
                     [i for i in range(int((len_of_feat + 1) / 2), 0, -1)]
                sample_size = list(map(lambda x: int(10000 / x), ls))
        else:
            sample_size = [n_samples] * matrix.shape[1]

        output[:, 0, 0] = self.base_value
        output[:, -1, 0] = self._get_prediction(instances)
        samples = np.array([self.data[self.features].sample(sample_size[sum(matrix[k])-1]).values
                            for k in range(1, matrix.shape[0] - 1)])

        for i in range(len(instances)):
            instance = instances[i:i+1]
            instance_values = instance[self.features].values

            repeat_mat_rows = np.array([np.repeat([matrix[j]], sample_size[sum(matrix[j]) - 1], axis=0) for j in range(1, matrix.shape[0] - 1)])
            repeat_inst = np.array([np.repeat(instance_values, sample_size[sum(matrix[j]) - 1], axis=0) for j in range(1, matrix.shape[0] - 1)])
            replaced_samples = np.array([np.where(repeat_mat_rows[i], repeat_inst[i], samples[i]) for i in range(matrix.shape[0]-2)])

            # This is where it is slow :D!
            predicts = list(map(lambda x: self._get_prediction(self._array_to_dict(x)), replaced_samples))

            averages = list(map(lambda x: np.average(x), predicts))

            output[i][1:-1, 0] = averages

        return output

    @staticmethod
    def _trim_matrix(matrix, row_index=[], column_index=[]):
        matrix_shape = np.shape(matrix)
        rows = [i for i in range(matrix_shape[0]) if i not in row_index]
        columns = [i for i in range(matrix_shape[1]) if i not in column_index]
        return np.reshape(np.array([matrix[i][j] for i in rows for j in columns]), newshape=(len(rows), len(columns)))

    @staticmethod
    def _linearoptimizer(matrices, kernel, y):
        transpose = np.transpose(matrices, axes=[0, 2, 1])
        A = np.linalg.inv(np.matmul(np.matmul(transpose, kernel), matrices))
        B = np.matmul(np.matmul(transpose, kernel), y)
        return np.matmul(A, B)

    @staticmethod
    def _row_into_matrix(row, number_of_rows):
        return np.array([row for i in range(number_of_rows)])

    @staticmethod
    def _col_into_matrix(col, number_of_cols):
        row = np.transpose(col)[0]
        matrix = KernelShap._row_into_matrix(row, number_of_rows=number_of_cols)
        return np.transpose(matrix)

    @staticmethod
    def _binom(n, k):
        return float(math.factorial(n) // math.factorial(k) // math.factorial(n - k))
