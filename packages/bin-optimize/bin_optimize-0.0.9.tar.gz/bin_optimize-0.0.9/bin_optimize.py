"""
The utility provides the ability to optimize the bins already arranged
using any bin packing algorithm into n-1 bins.

The utility works on the principle of pick up an item with largest volume from
the bin to be reduced and add it to the bin with least total volume.
"""

import copy
import typing

Bins = typing.Dict[typing.Any, typing.List[typing.Tuple[str, int]]]
"""Type annotation for Bins"""

Key = typing.Any
"""Type annotation for Key"""


def optimize(to_optimize: Bins,
             to_reduce: Key) -> Bins:
    """
    :param to_optimize: The bins to be optimized as n-1 bins
    :type to_optimize: :data:`~bin_optimize.Bins`
    :param to_reduce: The bin to be adjusted in existing n-1 bins
    :type to_reduce: :data:`~bin_optimize.Key`

    :rtype: :data:`~bin_optimize.Bins`
    :raises: KeyError
    """
    bins = copy.deepcopy(to_optimize)

    try:
        items_to_adj = bins.pop(to_reduce)
    except KeyError:
        raise KeyError('bin %s not found', to_reduce)

    volumes = {k: sum(y for x, y in v) for k, v in bins.items()}
    for item in sorted(items_to_adj):
        k = min(volumes, key=lambda key: volumes[key])
        bins.get(k).append(item)
        if len(item) > 1:
            volumes[k] += int(item[1])
    return bins
