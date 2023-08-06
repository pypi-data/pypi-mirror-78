from dicemaths.infinity import contested_roll_hit_avg
import pytest

def test_contested_basic():
    (hits, crits) = contested_roll_hit_avg(1, 10, 1, 0)
    assert (round(hits, 5), round(crits, 5)) == (0.4275, 0.0475)
