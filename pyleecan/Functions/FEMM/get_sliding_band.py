# -*- coding: utf-8 -*-
from numpy import exp, pi

from ...Classes.Arc1 import Arc1
from ...Classes.Circle import Circle
from ...Classes.Segment import Segment
from ...Classes.SurfLine import SurfLine
from ...Functions.labels import (
    SLID_LAB,
    NO_MESH_LAB,
    NO_LAM_LAB,
    BOUNDARY_PROP_LAB,
    SLID_LINE1_LAB,
    SLID_LINE2_LAB,
    SLID_LINE_LAB,
)


def get_sliding_band(sym, lam_int, lam_ext):
    """Returns  a list of surface in the airgap including the sliding band surface

    Parameters
    ----------
    sym: int
        Symmetry factor (1= full machine, 2= half of the machine...)
    Rgap_mec_int: float
        Internal lamination mechanic radius
    Rgap_mec_ext: float
        External lamination mechanic radius

    Returns
    -------
    surf_list: list
        List of surface in the airgap including the sliding band surface
    """

    Rgap_mec_int = lam_int.comp_radius_mec()
    Rgap_mec_ext = lam_ext.comp_radius_mec()
    Rgap_mag_int = lam_int.Rext
    Rgap_mag_ext = lam_ext.Rint
    Wgap_mec = Rgap_mec_ext - Rgap_mec_int
    W_sb = Wgap_mec / 3  # Width sliding band
    surf_list = list()
    label_int = lam_int.get_label()
    label_ext = lam_ext.get_label()

    if sym == 1:  # Complete machine
        # Bottom sliding band
        surf_list.append(
            Circle(
                center=0,
                radius=Rgap_mec_int + W_sb,
                label=label_int + "_" + SLID_LAB,
                point_ref=(Rgap_mec_int + W_sb / 2) * exp(1j * pi / 2),
                line_label=label_int + "_" + SLID_LAB,
            )
        )
        # Top sliding band
        surf_list.append(
            Circle(
                center=0,
                radius=Rgap_mec_int + 2 * W_sb,
                label=label_ext + "_" + SLID_LAB,
                point_ref=(Rgap_mec_ext - W_sb / 2) * exp(1j * pi / 2),
                line_label=label_ext + "_" + SLID_LAB,
            )
        )
        # Middle
        surf_list.append(
            SurfLine(
                line_list=[],
                point_ref=(Rgap_mec_int + W_sb * 3 / 2) * exp(1j * pi / 2),
                label=NO_LAM_LAB + "_" + NO_MESH_LAB,
            )
        )
    else:  # Symmetry
        # Bottom line
        Z1 = Rgap_mag_int
        Z2 = Rgap_mec_int + W_sb
        Z3 = Z2 * exp(1j * 2 * pi / sym)
        Z4 = Z1 * exp(1j * 2 * pi / sym)
        airgap_lines = list()
        airgap_lines.append(
            Segment(begin=Z1, end=Z2, prop_dict={BOUNDARY_PROP_LAB: SLID_LINE1_LAB})
        )
        airgap_lines.append(
            Arc1(
                begin=Z2,
                end=Z3,
                radius=Rgap_mec_int + W_sb,
                prop_dict={BOUNDARY_PROP_LAB: SLID_LINE_LAB},
            )
        )
        airgap_lines.append(
            Segment(begin=Z3, end=Z4, prop_dict={BOUNDARY_PROP_LAB: SLID_LINE1_LAB})
        )
        surf_list.append(
            SurfLine(
                line_list=airgap_lines,
                point_ref=(Z2 - W_sb / 2) * exp(1j * pi / sym),
                label=label_int + "_" + SLID_LAB,
            )
        )
        # Top line
        Z5 = Rgap_mag_ext
        Z6 = Rgap_mec_ext - W_sb
        Z7 = Z6 * exp(1j * 2 * pi / sym)
        Z8 = Z5 * exp(1j * 2 * pi / sym)
        airgap_lines = list()
        airgap_lines.append(
            Segment(begin=Z5, end=Z6, prop_dict={BOUNDARY_PROP_LAB: SLID_LINE2_LAB})
        )
        airgap_lines.append(
            Arc1(
                begin=Z6,
                end=Z7,
                radius=Rgap_mec_ext - W_sb,
                prop_dict={BOUNDARY_PROP_LAB: SLID_LINE_LAB},
            )
        )
        airgap_lines.append(
            Segment(begin=Z7, end=Z8, prop_dict={BOUNDARY_PROP_LAB: SLID_LINE2_LAB})
        )
        surf_list.append(
            SurfLine(
                line_list=airgap_lines,
                point_ref=(Z6 + W_sb / 2) * exp(1j * pi / sym),
                label=label_ext + "_" + SLID_LAB,
            )
        )

    return surf_list
