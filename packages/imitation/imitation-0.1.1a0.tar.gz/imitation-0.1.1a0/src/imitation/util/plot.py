import os
from typing import Iterable, Tuple

from matplotlib import pyplot as plt


def save_fig(path: str, fig: plt.Figure, fmt: str = "pdf", dpi: int = 300, **kwargs):
    path = f"{path}.{fmt}"
    root_dir = os.path.dirname(path)
    os.makedirs(root_dir, exist_ok=True)
    kwargs.setdefault("transparent", True)
    with open(path, "wb") as f:
        fig.savefig(f, format=fmt, dpi=dpi, **kwargs)


def save_figs(
    root_dir: str, generator: Iterable[Tuple[str, plt.Figure]], **kwargs
) -> None:
    for name, fig in generator:
        name = name.replace("/", "_")
        path = os.path.join(root_dir, name)
        save_fig(path, fig, **kwargs)
