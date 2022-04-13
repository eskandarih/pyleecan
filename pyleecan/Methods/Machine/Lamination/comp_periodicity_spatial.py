from numpy import gcd


def comp_periodicity_spatial(self):
    """Compute the periodicity factor of the lamination

    Parameters
    ----------
    self : lamination
        A lamination object

    Returns
    -------
    per_a : int
        Number of spatial periodicities of the lamination
    is_antiper_a : bool
        True if an spatial anti-periodicity is possible after the periodicities
    """

    if hasattr(self, "get_Zs") and hasattr(self, "get_pole_pair_number"):
        Zs = self.get_Zs()
        p = self.get_pole_pair_number()

        nb_list = [p, Zs]
        # account for notches and bore
        for notch in self.notch:
            nb_list.append(notch.notch_shape.Zs)

        if self.bore:
            if hasattr(self.bore, "N"):
                nb_list.append(self.bore.N)

        # compute the gcd of the list
        per_a = gcd(nb_list[0], nb_list[1])
        for ii in range(2, len(nb_list)):
            per_a = gcd(per_a, nb_list[ii])

        nb_list.pop(0)
        is_antiper_a = all(nb_list / per_a % 2 == 0)

        # Account for duct periodicity
        per_a, is_antiper_a = self.comp_periodicity_duct_spatial(per_a, is_antiper_a)

    else:
        per_a = None
        is_antiper_a = False

    return per_a, is_antiper_a
