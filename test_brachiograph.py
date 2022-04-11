import pytest
from pytest import approx
import numpy

from brachiograph import BrachioGraph
import linedraw

bg = BrachioGraph(virtual=True)

# ----------------- set-up tests -----------------

bg2 = BrachioGraph(
    virtual = True,
    servo_1_angle_pws_bidi = {
        -135: {'cw': 2374, 'acw': 2386},
        -120: {'cw': 2204, 'acw': 2214},
        -105: {'cw': 2042, 'acw': 2054},
        -90:  {'cw': 1898, 'acw': 1900},
        -75:  {'cw': 1730, 'acw': 1750},
        -60:  {'cw': 1604, 'acw': 1612},
        -45:  {'cw': 1466, 'acw': 1476},
        -30:  {'cw': 1330, 'acw': 1340},
        -15:  {'cw': 1188, 'acw': 1200},
        0:    {'cw': 1048, 'acw': 1060},
        15:   {'cw':  904, 'acw':  910},
        30:   {'cw':  750, 'acw':  766},
    },
    servo_2_angle_pws_bidi = {
        15:   {'cw':  783, 'acw':  761},
        30:   {'cw':  917, 'acw':  901},
        45:   {'cw': 1053, 'acw': 1035},
        60:   {'cw': 1183, 'acw': 1167},
        75:   {'cw': 1303, 'acw': 1287},
        90:   {'cw': 1427, 'acw': 1417},
        105:  {'cw': 1557, 'acw': 1537},
        120:  {'cw': 1697, 'acw': 1681},
        135:  {'cw': 1843, 'acw': 1827},
        150:  {'cw': 2003, 'acw': 1987},
    },

    pw_up=1400,                     # pulse-widths for pen up/down
    pw_down=1650,
)


def test_defaults_of_default_bg():
    assert bg.angles_to_pw_1 == bg.naive_angles_to_pulse_widths_1
    assert bg.get_pulse_widths() == (1500, 1500)
    assert (bg.angle_1, bg.angle_2) == (-90, 90)


def test_defaults_of_bg_with_bidi_pws():
    assert bg2.angles_to_pw_1 != bg2.naive_angles_to_pulse_widths_1

    assert bg2.angles_to_pw_1(-90) == approx(1894, abs=1e-0)
    assert bg2.angles_to_pw_2(90) == approx(1422, abs=1e-0)

    assert bg2.hysteresis_correction_1 == approx(5.416666)
    assert bg2.hysteresis_correction_2 == approx(-8.3)

    assert bg2.get_pulse_widths() == (
        approx(1894 + bg2.hysteresis_correction_1, abs=1e-0),
        approx(1422 + bg2.hysteresis_correction_2, abs=1e-0)
    )
    assert (bg2.angle_1, bg2.angle_2) == (-90, 90)


# ----------------- drawing methods -----------------


def test_plot_from_file():
    bg.plot_file("test-patterns/accuracy.json")


# ----------------- test pattern methods -----------------


def test_test_pattern():
    bg.test_pattern()


def test_vertical_lines():
    bg.vertical_lines()


def test_horizontal_lines():
    bg.horizontal_lines()


def test_box():
    bg.box()


# ----------------- pen-moving methods -----------------


def test_centre():
    bg.park()


def test_can_land_at_0_degrees():
    bg.set_angles(0, 0)
    assert (bg.angle_1, bg.angle_2) == (0, 0)


# ----------------- reporting methods -----------------


def test_report():
    bg.report()


def test_maths_errors():
    plotter = BrachioGraph(inner_arm=8.2, outer_arm=8.85, virtual=True)
    with pytest.raises(Exception):
        plotter.xy_to_angles(-10.2, 13.85)
