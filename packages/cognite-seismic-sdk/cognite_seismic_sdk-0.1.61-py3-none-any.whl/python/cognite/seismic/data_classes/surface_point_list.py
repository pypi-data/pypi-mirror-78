# Copyright 2019 Cognite AS

import itertools

import numpy as np
from cognite.seismic.data_classes.custom_list import CustomList


def _get_max_inline_group_len(groups):
    trace_len = 0
    for group in groups:
        trace_len = max(trace_len, len(group))
    return trace_len


class SurfacePointList(CustomList):
    def to_array(self):
        sorted_traces = sorted(self.to_list(), key=lambda x: (x.iline, x.xline))
        inline_groups = [list(g) for k, g in itertools.groupby(sorted_traces, lambda x: x.iline)]
        max_group_len = _get_max_inline_group_len(inline_groups)
        result = []
        for inline_group in inline_groups:
            prefix_zeros = np.zeros(max_group_len - len(inline_group))
            values = np.array([i.value for i in inline_group])
            result.append(np.append(prefix_zeros, values))

        return np.array(result, dtype=object)
