"""Retry policy BDD."""
from __future__ import annotations


def test_delays_geometric_and_capped():
    from estorides_core.config import RETRY, retry_delay

    assert retry_delay(1) == RETRY.base_s
    assert abs(retry_delay(2) - RETRY.base_s * RETRY.factor) < 1e-9
    assert retry_delay(0) == retry_delay(1)
    assert retry_delay(100) <= RETRY.cap_s


def test_client_defaults_to_central_policy():
    from estorides_core import async_client as ac
    from estorides_core.config import RETRY

    c = ac.AsyncClient()
    assert c.max_retries == RETRY.attempts
    c2 = ac.AsyncClient(max_retries=7)
    assert c2.max_retries == 7
