# Author: Piotr Cieślak

import matplotlib.pyplot as plt
import numpy as np

#fixme add dates in x axis
class GraphUtils():
    """This class provides methods for generating and modifying plots and graphs which are presented to the user"""

    @staticmethod
    def get_graph(prices):
        """Generate a graph from given values"""
        y_points = prices[0:3]
        x_points = np.array([1, 2, 3])
        y_points_predicted = prices[2:]
        x_points_calculated = np.array([3, 4])
        plt.clf()
        plt.plot(x_points, y_points, color='black', linewidth=2)
        plt.plot(x_points_calculated, y_points_predicted, color='blue', linewidth=2, linestyle='dashed')
        plt.savefig('app/static/home_page/plots/plot.png')