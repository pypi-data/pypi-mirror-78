# pytype: skip-file
# flake8: noqa
import abc
import warnings
from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar

import gym
import numpy as np

from imitation.contrib import dataset_wrappers
from imitation.data import buffer, datasets, types

S = TypeVar("S")
T = TypeVar("T")


class DatasetWrapper(Generic[S, T], datasets.Dataset[T]):
    """Abstract base class for classes that wrap other Dataset instances.

    Concrete subclasses should implement `.sample(n_samples) -> T`.
    """

    def __init__(self, dataset: datasets.Dataset[S], name: Optional[str] = None):
        self.dataset = dataset
        self.name = name

    def size(self):
        return self.dataset.size()

    def __str__(self):
        name = self.name or type(self).__name__
        return f"<{name}{self.dataset}>"

    def __repr__(self):
        return str(self)


class ReplayBufferDatasetWrapper(DatasetWrapper):
    def __init__(
        self,
        dataset: datasets.Dataset[Dict[str, np.ndarray]],
        capacity: int,
    ):
        """Wrapper that modifies .sample() to sample indirectly using a replay buffer.

        With every call to `.sample(n_samples)`, `n_samples` samples from the wrapped
        Dataset are stored in a FIFO buffer, and `n_samples` samples are randomly
        selected and returned from the buffer.

        Args:
            dataset: A Dataset returning `TransitionsWithRew` samples.
            capacity: The number of samples that can be stored in the `ReplayBuffer`.
                Upon initialization of this wrapper, the `ReplayBuffer` is immediately
                populated with `capacity` samples from `dataset.sample(capacity).
        """

        super().__init__(dataset, f"ReplayBuffer[cap={capacity}]")
        self.capacity = capacity
        samples = self.dataset.sample(self.capacity)
        self.buffer = buffer.ReplayBuffer.from_data(samples)

    def sample(self, n_samples: int):
        assert n_samples >= 0
        self.buffer.store(n_samples, truncate_ok=True)
        return self.buffer.sample(n_samples)


class BidirectionalTransform(abc.ABC):
    def __init__(self, observation_space: gym.Space, action_space: gym.Space):
        self.observation_space = observation_space
        self.action_space = action_space  # Processed action space.

    @abc.abstractmethod
    def forwards(
        self,
        transitions: types.TransitionsWithRew,
    ) -> types.TransitionsWithRew:
        """Defines a transformation from raw (Dataset or Env) to transformed values.

        `forwards` should be a pure function. In other words, any instance of
        BidirectionalTransform returns the same outputs given the same inputs.

        Args:
            ob: Raw observation (as passed to `Env.step(act)` or `Dataset.sample()`).
            act: Raw action (as returned from `Dataset.sample()` or passed to
                `Env.step(act)`.
            next_ob: Raw observation for the next timestep. Can be None, in which
                case the corresponding return value should also be None.
            rew: Raw reward (as returned from `Env.step()` or from `Dataset.sample()`.
            info: Raw info (as returned from `Env.step()` or from `Dataset.sample()`.

        Returns:
            Transformed versions of the arguments.
        """

    @abc.abstractmethod
    def backwards_act(self, transformed_act):
        """Defines a (pseudo-)inverse transformation from transformed act to raw act.

        `backwards_act` should be a pure function. In other words, any instance of
        BidirectionalTransform returns the same outputs given the same inputs.


        Args:
            transformed_act: Actions transformed from raw actions by `forwards()`.

        Returns:
            A raw action. Not required to be the same raw action as that passed into
            `forwards()` because `forwards()` might not be one-to-one / injective.
        """


class DefinesDatasetWrapperMixin(abc.ABC, Generic[S, T]):
    """A class implementing this mixin defines an `DatasetWrapper`."""

    @abc.abstractmethod
    def apply_dataset_wrapper(
        self, dataset: datasets.Dataset[S]
    ) -> DatasetWrapper[S, T]:
        """Wraps a dataset using the dataset.

        Args:
            dataset: A Dataset to wrap.

        Returns:
            A wrapped dataset.
        """


class BidirectionalGymWrapper(
    gym.Wrapper,
    DefinesDatasetWrapperMixin[types.TransitionsWithRew, types.TransitionsWithRew],
):
    def __init__(self, env: gym.Env, transform: BidirectionalTransform):
        self.transform = transform
        super().__init__(env)

    @property
    def observation_space(self) -> gym.Space:
        return self.transform.observation_space

    @property
    def action_space(self) -> gym.Space:
        return self.transform.action_space

    def step(self, action: Any) -> Tuple[Any, float, dict]:
        act = self.transform.backwards_act(action)
        return self.env.step(act)

    def apply_dataset_wrapper(
        self, dataset: datasets.Dataset[types.TransitionsWithRew]
    ) -> DatasetWrapper[types.TransitionsWithRew, types.TransitionsWithRew]:
        """Wraps a dataset using the dataset."""
        return BidirectionalDatasetWrapper(dataset, self.transform)


class BidirectionalDatasetWrapper(
    DatasetWrapper[types.TransitionsWithRew, types.TransitionsWithRew],
):
    def __init__(
        self,
        dataset: datasets.Dataset[types.TransitionsWithRew],
        transform: BidirectionalTransform,
    ):
        self.dataset = dataset
        self.transform = transform
        super().__init__(dataset)

    def sample(self, n_samples: int) -> types.TransitionsWithRew:
        samples = self.dataset.sample(n_samples)
        iterator = zip(
            samples.obs,
            samples.acts,
            samples.rews,
            samples.dones,
            samples.infos,
            samples.next_obs,
        )
        transformed_iterator = map(self.transform.forwards, iterator)
        transformed_data_needs_stack = list(zip(*transformed_iterator))
        transformed_data = tuple(map(np.stack, transformed_data_needs_stack))
        obs, acts, rews, dones, infos, next_obs = transformed_data
        transformed_samples = types.TransitionsWithRew(
            obs=obs,
            acts=acts,
            infos=infos,
            next_obs=next_obs,
            dones=dones,
            rews=rews,
        )
        return transformed_samples


def wrap_dataset_with_env_wrappers(
    dataset: datasets.Dataset[types.TransitionsWithRew],
    env: gym.Env,
    warn_on_ignore_wrapper: bool = True,
) -> datasets.Dataset[types.TransitionsWithRew]:
    """Apply GymDatasetWrappers on top of a Dataset[TransitionsWithRew].

    Args:
        dataset: ...
        env: An Env possibly with wrappers. For every gym.Wrapper wrapping `env` which
            also subclasses `GymWrapperDatasetMixin`, `minerl_dataset` is wrapped with
            MineRLDatasetWrapper which applies that the gym.Wrapper's transform
            to the dataset, as defined in `GymWrapperDatasetMixin.process_batch()`.

            Any `gym.Wrapper` that doesn't subclass `GymWrapperDatasetMixin` is skipped.
        warn_on_ignore_wrapper: If True, then warn with RuntimeWarning for every
            `gym.Wrapper` that doesn't subclass `GymWrapperDatasetMixin`.

    Returns:
        `dataset` wrapped by a `DatasetWrapper` for every gym.Wrapper around `env`
        also subclasses `GymWrapperDatasetMixin`. If `env` has no wrappers, then the
        return is simply `dataset`.
    """
    # Traverse all the gym.Wrapper starting from the outermost wrapper. When re-apply
    # them to the Dataset as MineRLDatasetWrapper, we need to apply in reverse order
    # (starting with innermost wrapper), so we save gym.Wrappers in a list first.
    compatible_wrappers: List[DefinesDatasetWrapperMixin] = []
    curr = env
    while isinstance(curr, gym.Wrapper):
        if isinstance(curr, DefinesDatasetWrapperMixin):
            compatible_wrappers.append(curr)
        elif warn_on_ignore_wrapper:
            warnings.warn(
                f"{curr} doesn't subclass DefinesDatasetWrapperMixin. Skipping "
                "this Wrapper when creating Dataset processing wrappers.",
                RuntimeWarning,
            )
        curr = curr.env

    for wrapper in reversed(dataset_wrappers):
        dataset = DatasetWrapper(dataset, wrapper)
    return dataset
