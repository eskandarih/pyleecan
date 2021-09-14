from numpy import pi, array, linspace, mean, floor, flip, concatenate, arange

from ....Methods.Machine.Skew import TYPE_SKEW_LIST


def comp_angle(self):
    """Compute skew angles and positions

    Parameters
    ----------
    self : Skew
        a Skew object

    """

    logger = self.get_logger()

    if self.parent is None:
        raise Exception("ERROR: The Skew object must be in a Lamination object to run")

    L = self.parent.comp_length()
    rate = self.rate
    is_step = self.is_step
    type_skew = self.type_skew
    Nstep = self.Nstep
    z_list = self.z_list
    angle_list = self.angle_list

    if "PMSM" in self.parent.parent.get_machine_type():
        Z = self.parent.parent.stator.get_Zs()
    else:
        Z = self.parent.parent.rotor.get_Zs()

    sp = 2 * pi / Z

    if rate is None:
        # Set rate value by default
        logger.info("Skew rate is " + str(rate) + ", setting it to 1 by default")
        rate = 1

    # Continuous skew
    if is_step:

        if type_skew in TYPE_SKEW_LIST and type_skew != "user-defined":

            if Nstep in [None, 0, 1]:
                raise Exception(
                    "Number of steps= "
                    + str(Nstep)
                    + " must be defined and > 1 for stepped skew of type: "
                    + str(type_skew)
                )

            z_list = linspace(-0.5, 0.5, Nstep + 1)

            if type_skew == "linear":

                angle_list = linspace(-rate * sp / 2, rate * sp / 2, Nstep)

            elif type_skew == "vshape":

                if Nstep in [None, 2]:
                    raise Exception(
                        "Number of steps= "
                        + str(Nstep)
                        + " must be defined and > 2 for vshape stepped skew"
                    )

                Nhalf = int(floor((Nstep + 1) / 2))

                angles_half = linspace(-rate * sp, 0, Nhalf)

                if Nstep % 2 == 0:
                    angle_list = concatenate((angles_half, flip(angles_half)))
                else:
                    angle_list = concatenate((angles_half[:-1], flip(angles_half)))

            elif type_skew == "zig-zag":

                if Nstep in [None, 2]:
                    raise Exception(
                        "Number of steps= "
                        + str(Nstep)
                        + " must be defined and > 2 for alternate stepped skew"
                    )

                angle_list = 0.5 * rate * sp * (-1) ** arange(Nstep)

            elif type_skew == "function":
                if self.function is None:
                    raise Exception("Function must be defined if type_skew == function")
                try:
                    angle_list = self.function(array(z_list))
                except Exception:
                    raise Exception("Error in skew function definition")

            # Put average skew angle to zero
            angle_list = list(array(angle_list) - mean(angle_list))

        elif type_skew == "user-defined":

            if angle_list is None:
                raise Exception("angle_list not provided for user-defined stepped skew")

            Nstep = len(angle_list)

            if z_list is None:
                z_list = linspace(-0.5, 0.5, Nstep + 1)

            else:

                if len(angle_list) != len(z_list) - 1:
                    raise Exception(
                        "angle_list must have one element less than z_list for user-defined stepped skew"
                    )

                if z_list[0] != -0.5:
                    raise Exception(
                        "First coordinate in z_list must be -0.5 (x L) for user-defined stepped skew"
                    )

                if 0.5 in z_list:
                    raise Exception(
                        "0.5 (x L) must not be in z_list for user-defined stepped skew"
                    )

        else:
            raise Exception("Unknown stepped-skew type: " + self.type_skew)

    else:

        if type_skew == "linear":
            Nstep = 2
            z_list = linspace(-0.5, 0.5, Nstep)
            angle_list = [z * rate * sp for z in z_list]

        else:
            raise Exception("Only linear skew is available for continuous skew")

    # Store z_list in absolute value
    z_list = [z * L for z in z_list]

    self.rate = rate
    self.Nstep = Nstep
    self.angle_list = angle_list
    self.z_list = z_list
