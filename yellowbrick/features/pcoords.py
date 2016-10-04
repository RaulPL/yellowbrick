# yellowbrick.features.pcoords
# Implementations of parallel coordinates for feature analysis.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Mon Oct 03 21:46:06 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: pcoords.py [] benjamin@bengfort.com $

"""
Implementations of parallel coordinates for multi-dimensional feature
analysis. There are a variety of parallel coordinates from Andrews Curves to
coordinates that optimize column order.
"""

##########################################################################
## Imports
##########################################################################

import numpy as np
import matplotlib.pyplot as plt

from yellowbrick.base import FeatureVisualizer
from yellowbrick.exceptions import YellowbrickTypeError
from yellowbrick.color_utils import resolve_colors


##########################################################################
## Static Parallel Coordinates Visualizer
##########################################################################

class ParallelCoordinates(FeatureVisualizer):
    """
    Parallel coordinates displays each feature as a vertical axis spaced
    evenly along the horizontal, and each instance as a line drawn between
    each individual axis.
    """

    def __init__(self, ax=None, features=None, classes=None, color=None,
                 colormap=None, vlines=True, vlines_kwds=None, **kwargs):
        """
        Initialize the base parallel coordinates with many of the options
        required in order to make the visualization work.

        Parameters
        ----------

        :param ax: the axis to plot the figure on.

        :param features: a list of feature names to use
            If a DataFrame is passed to fit and features is None, feature
            names are selected as the columns of the DataFrame.

        :param classes: a list of class names for the legend
            If classes is None and a y value is passed to fit then the classes
            are selected from the target vector.

        :param color: optional list or tuple of colors to colorize lines
            Use either color to colorize the lines on a per class basis or
            colormap to color them on a continuous scale.

        :param colormap: optional string or matplotlib cmap to colorize lines
            Use either color to colorize the lines on a per class basis or
            colormap to color them on a continuous scale.

        :param vlines: flag to determine vertical line display, default True

        :param vlines_kwds: options to style or display the vertical lines

        :param kwargs: keyword arguments passed to the super class.

        These parameters can be influenced later on in the visualization
        process, but can and should be set as early as possible.
        """
        super(ParallelCoordinates, self).__init__(**kwargs)

        # The figure params
        # TODO: hoist to a higher level base class
        self.ax = ax

        # Data Parameters
        self.features_ = features
        self.classes_  = classes

        # Visual Parameters
        self.color = color
        self.colormap = colormap
        self.show_vlines = vlines
        self.vlines_kwds = vlines_kwds or {
            'linewidth': 1, 'color': 'black'
        }

    def fit(self, X, y=None, **kwargs):
        """
        The fit method is the primary drawing method for the parallel coords
        visualization since it has both the X and y data required for the
        viz and the transform method does not.
        """

        # Get the shape of the data
        nrows, ncols = X.shape

        # Compute the classes for the legend if they're None.
        if self.classes_ is None:
            # TODO: Is this the most efficient method?
            self.classes_ = [str(label) for label in set(y)]

        # Handle the feature names if they're None.
        if self.features_ is None:

            # If X is a data frame, get the columns off it.
            if hasattr(X, 'columns'):
                self.features_ = X.columns

            # Otherwise create numeric labels for each column.
            else:
                self.features_ = [
                    str(cdx) for cdx in range(ncols)
                ]

        # Create the xticks for each column
        # TODO: Allow the user to specify this feature
        x = list(range(ncols))

        # Create the axis if it doesn't exist
        if self.ax is None: self.ax = plt.gca()

        # Create the colors
        color_values = resolve_colors(
            num_colors=len(self.classes_), colormap=self.colormap, color=self.color
        )
        colors = dict(zip(self.classes_, color_values))

        print colors

        # Add the instances
        for idx, row in enumerate(X):
            # TODO: How to map classmap to labels?
            label = y[idx] # Get the label for the row
            label = self.classes_[label]
            self.ax.plot(x, row, color=colors[label], label=label)

        # Add the vertical lines
        if self.show_vlines:
            for idx in x:
                self.ax.axvline(idx, **self.vlines_kwds)

        # Finalize the plot
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(self.features_)
        self.ax.set_xlim(x[0], x[-1])

        # Fit always returns self.
        return self

    def poof(self):
        """
        Display the parallel coordinates.
        """
        self.ax.legend(loc='best')
        self.ax.grid()

        plt.show()
