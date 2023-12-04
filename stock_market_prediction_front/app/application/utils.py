# Author: Piotr Cieślak

import matplotlib.pyplot as plt
import numpy as np
import datetime

#fixme add dates in x axis
class GraphUtils():
    """This class provides methods for generating and modifying plots and graphs which are presented to the user"""

    @staticmethod
    def get_graph(prices):
        """Generate a graph from given values"""
        y_points = prices[0:3, 0]
        x_points = np.chararray((1,4), itemsize=10)
        for i in range(0, len(prices)):
            date = datetime.datetime(int(prices[i, 1]), int(prices[i, 2]), int(prices[i, 3]))
            x_points[0, i] = date.date().strftime("%d/%m/%Y")
        # x_points = np.array([1, 2, 3])
        y_points_predicted = prices[2:, 0]
        # x_points = [f'{x:%Y-%m-%d}' for x in x_points]
        x_points_calculated = np.array([3, 4])
        plt.clf()
        plt.plot(x_points[0, 0:3], y_points, color='black', linewidth=2)
        plt.plot(x_points[0, 2:], y_points_predicted, color='blue', linewidth=2, linestyle='dashed')
        plt.savefig('app/static/home_page/plots/plot.png')