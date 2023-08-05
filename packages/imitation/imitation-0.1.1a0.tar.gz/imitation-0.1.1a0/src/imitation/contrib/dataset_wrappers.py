# pytype: skip-file
# flake8: noqa

import warnings
from typing import Dict, Generic, List, Optional, TypeVar

import gym
import numpy as np

from imitation.data import buffer, datasets, types

S = TypeVar("S")
T = TypeVar("T")


"""Test: Add scaling wrapper that just multiplies obs and acts by K, M."""


class TransitionsDatasetWrapper(datasets.Dataset[types.TransitionsWithRew]):
    """Wrapper that converts dictionary samples to TransitionsWithRew.

    The dictionary samples must have the same keys as TransitionsWithRew's fields.
    Namely, 'obs', 'acts', 'next_obs', 'rews', and 'dones'.

    Useful for GAIL and AIRL, which require `Dataset[imitation.data.types.Transitions]`
    instead of `Dataset[BatchDict]`.
    """

    def __init__(self, minerl_dataset: datasets.Dataset[Dict[str, np.ndarray]]):
        f"""Constructs DictToTransitionsWrapper."""
        self.dataset = minerl_dataset

    def sample(self, n_samples: int) -> types.TransitionsWithRew:
        return types.TransitionsWithRew(**self.dataset.sample(n_samples))

    def size(self) -> Optional[int]:
        return self.dataset.size()
