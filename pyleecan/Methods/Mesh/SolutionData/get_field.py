# -*- coding: utf-8 -*-

import numpy as np


def get_field(self, *args):
    """Get the value of variables stored in Solution.

    Parameters
    ----------
    self : SolutionData
        an SolutionData object
    *args: list of strings
        List of axes requested by the user, their units and values (optional)

    Returns
    -------
    field: array
        an array of field values

    """
    axname, axsize = self.get_axis_list()
    symbol = self.field.symbol

    if not args:
        field_dict = self.field.get_along(tuple(axname))
    else:
        field_dict = self.field.get_along(args)

    field = field_dict[symbol]

    return field
