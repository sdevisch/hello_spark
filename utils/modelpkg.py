"""
Model scoring package: Numba/NumPy kernels for complex feature transforms
and multi-step forecasts per entity.

In a real cluster, distribute this module as a wheel/zip and register via
SparkContext.addPyFile(). For local testing we import it directly.
"""

from __future__ import annotations

import numpy as np

try:
    from numba import njit, prange
    NUMBA_AVAILABLE = True
except Exception:  # pragma: no cover - environment dependent
    NUMBA_AVAILABLE = False


def has_numba() -> bool:
    return NUMBA_AVAILABLE


if NUMBA_AVAILABLE:

    @njit(fastmath=True)
    def transform_features(values: np.ndarray, prices: np.ndarray,
                           exog: np.ndarray) -> np.ndarray:
        """Complex but vectorizable transforms.

        Returns a composite feature vector per row.
        """
        # exog is shape (n, 2): [flag, cat_code]
        flag = exog[:, 0]
        cat = exog[:, 1]
        out = (
            0.15 * (values * prices)
            + 0.07 * (values ** 0.5)
            + 0.03 * (prices ** 1.5)
            + 0.10 * (flag * values)
            + 0.02 * (cat * prices)
        )
        return out

    @njit(fastmath=True)
    def _sigmoid(x: float) -> float:
        return 1.0 / (1.0 + np.exp(-x))

    @njit(parallel=True, fastmath=True)
    def iterative_forecast(entity_ids: np.ndarray,
                           base: np.ndarray,
                           horizon: int,
                           alpha: float,
                           beta: float) -> np.ndarray:
        """Compute iterative forecasts per entity for given horizon.

        For each entity's time series base[t], produce y[t+h] by recurrence:
          y_{t+1} = sigmoid(alpha * base_t + beta * y_t)
        We return final y after `horizon` steps for each t (rolling one-step
        iteration). This is an intensive, stateful per-entity loop.
        """
        n = base.shape[0]
        out = np.empty(n, dtype=np.float64)
        # Walk through rows; reset state at entity boundary
        last_entity = -1
        y = 0.0
        for i in prange(n):
            e = int(entity_ids[i])
            if e != last_entity:
                last_entity = e
                y = 0.0
            # advance horizon steps from this point using base[i]
            y_local = y
            b = base[i]
            for _ in range(horizon):
                y_local = _sigmoid(alpha * b + beta * y_local)
            out[i] = y_local
            # update state one step as if we step forward by 1 period
            y = _sigmoid(alpha * b + beta * y)
        return out

else:

    def transform_features(values: np.ndarray, prices: np.ndarray,
                           exog: np.ndarray) -> np.ndarray:  # type: ignore[misc]
        flag = exog[:, 0]
        cat = exog[:, 1]
        return (
            0.15 * (values * prices)
            + 0.07 * (values ** 0.5)
            + 0.03 * (prices ** 1.5)
            + 0.10 * (flag * values)
            + 0.02 * (cat * prices)
        )

    def iterative_forecast(entity_ids: np.ndarray, base: np.ndarray, horizon: int,
                           alpha: float, beta: float) -> np.ndarray:  # type: ignore[misc]
        def sigmoid(x: float) -> float:
            return 1.0 / (1.0 + np.exp(-x))

        n = base.shape[0]
        out = np.empty(n, dtype=np.float64)
        last_entity = -1
        y = 0.0
        for i in range(n):
            e = int(entity_ids[i])
            if e != last_entity:
                last_entity = e
                y = 0.0
            y_local = y
            b = base[i]
            for _ in range(horizon):
                y_local = sigmoid(alpha * b + beta * y_local)
            out[i] = y_local
            y = sigmoid(alpha * b + beta * y)
        return out


