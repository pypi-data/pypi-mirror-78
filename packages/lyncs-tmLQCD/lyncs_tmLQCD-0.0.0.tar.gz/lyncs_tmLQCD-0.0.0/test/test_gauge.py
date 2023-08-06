import tempfile
from pytest import raises
import numpy as np
from lyncs_tmLQCD import Gauge
from lyncs_tmLQCD.gauge import get_g_iup, get_g_gauge_field


def test_init():
    gauge = Gauge(np.zeros((4, 4, 4, 4, 4, 3, 3), dtype="complex"))
    assert gauge == Gauge(gauge)
    with raises(ValueError):
        Gauge(np.zeros((4, 4, 4, 4), dtype="complex"))
    with raises(TypeError):
        Gauge(np.zeros((4, 4, 4, 4, 4, 3, 3), dtype="float"))


def test_unity():
    gauge = Gauge(np.zeros((4, 4, 4, 4, 4, 3, 3), dtype="complex"))
    gauge.unity()
    assert gauge.plaquette() == 1
    assert gauge.temporal_plaquette() == 1
    assert gauge.spatial_plaquette() == 1
    assert gauge.rectangles() == 1
    assert gauge.gauge_action() == 6 * 4 ** 4
    assert np.isclose(
        gauge.symanzik_gauge_action(), 6 * 4 ** 4 * (1 + 8 / 12 - 2 * 1 / 12)
    )
    assert np.isclose(
        gauge.iwasaki_gauge_action(), 6 * 4 ** 4 * (1 + 8 * 0.331 - 2 * 0.331)
    )


def test_random():
    gauge = Gauge(np.zeros((4, 4, 4, 4, 4, 3, 3), dtype="complex"))
    gauge.random()
    assert -1 <= gauge.plaquette() <= 1
    assert np.isclose(
        gauge.plaquette(), (gauge.temporal_plaquette() + gauge.spatial_plaquette()) / 2
    )


def test_global():
    gauge = Gauge(np.zeros((4, 4, 4, 4, 4, 3, 3), dtype="complex"))
    gauge.random()
    gauge.copy_to_global()
    assert gauge == get_g_gauge_field()

    gauge_copy = Gauge(np.zeros((4, 4, 4, 4, 4, 3, 3), dtype="complex"))
    gauge_copy.copy_from_global()
    assert gauge == gauge_copy


def test_io():
    tmp = tempfile.mkdtemp()
    gauge = Gauge(np.zeros((4, 4, 4, 4, 4, 3, 3), dtype="complex"))
    gauge.random()
    gauge.write(tmp + "/conf")
    gauge_read = Gauge(np.zeros((4, 4, 4, 4, 4, 3, 3), dtype="complex"))
    gauge_read.read(tmp + "/conf")
    assert gauge == gauge_read


def test_repr():
    gauge = Gauge(np.zeros((4, 4, 4, 4, 4, 3, 3), dtype="complex"))
    gauge.random()
    assert repr(gauge) == repr(gauge.field)
    assert str(gauge) == str(gauge.field)


def test_g_iup():
    g_iup = get_g_iup()
    g_iup[0, 0, 0, 0, 0] == 1
