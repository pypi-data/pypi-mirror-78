# import unittest
# from feyn.__future__.contrib.inspection import pdheatmap
# import feyn
# import pandas as pd
# import numpy as np


# class TestPdHeatmap(unittest.TestCase):
#     def test_that_it_runs(self):
#         graph = feyn.Graph.load('test/__future__/simple.graph')
#         df = pd.DataFrame(np.array([[0.095, 0.2255, 0.6770, 0.5160, 0.2050], [0.2245, 0.0995, 0.2565, 0.2155, 0.0985]]).T, columns=['Height', 'Shucked weight'])

#         heatmap = pdheatmap.paint_df_importance_heatmap(graph, df)
#         assert heatmap is not None, "Heatmap should be computed"
