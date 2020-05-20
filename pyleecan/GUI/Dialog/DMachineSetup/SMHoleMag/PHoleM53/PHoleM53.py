# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget

from ......Classes.HoleM53 import HoleM53
from ......GUI import gui_option
from ......GUI.Dialog.DMachineSetup.SMHoleMag.PHoleM53.Gen_PHoleM53 import Gen_PHoleM53
from ......Methods.Slot.Slot.check import SlotCheckError


class PHoleM53(Gen_PHoleM53, QWidget):
    """Page to set the Hole Type 53
    """

    # Signal to DMachineSetup to know that the save popup is needed
    saveNeeded = pyqtSignal()
    # Information for WHoleMag
    hole_name = "Slot Type 53"
    hole_type = HoleM53

    def __init__(self, hole=None, w_matlib=None):
        """Initialize the widget according to hole

        Parameters
        ----------
        self : PHoleM53
            A PHoleM53 widget
        hole : HoleM53
            current hole to edit
        w_matlib : DMatLib
            Material Library Dialog to view and modify material data
        """
        # Build the interface according to the .ui file
        QWidget.__init__(self)
        self.setupUi(self)

        self.hole = hole
        self.w_matlib = w_matlib

        # Set FloatEdit unit
        self.lf_W1.unit = "m"
        self.lf_W2.unit = "m"
        self.lf_W3.unit = "m"
        self.lf_H0.unit = "m"
        self.lf_H1.unit = "m"
        self.lf_H2.unit = "m"
        self.lf_H3.unit = "m"

        # Set default materials
        self.w_mat_0.setText("magnet_0:")
        self.w_mat_0.def_mat = "Magnet1"
        self.w_mat_1.setText("magnet_1:")
        self.w_mat_1.def_mat = "Magnet1"

        # Set unit name (m ou mm)
        self.u = gui_option.unit
        wid_list = [
            self.unit_W1,
            self.unit_W2,
            self.unit_W3,
            self.unit_H0,
            self.unit_H1,
            self.unit_H2,
            self.unit_H3,
        ]
        for wid in wid_list:
            wid.setText(self.u.get_m_name())

        # Adapt GUI with/without magnet
        if hole.magnet_0 is None:  # SyRM
            self.img_slot.setPixmap(
                QPixmap(":/images/images/MachineSetup/WSlot/Slot_53_no_mag.PNG")
            )
            self.w_mat_0.hide()
            self.w_mat_1.hide()
        else:
            # Set current material
            self.w_mat_0.update(self.hole.magnet_0, "mat_type", self.w_matlib)
            self.w_mat_1.update(self.hole.magnet_1, "mat_type", self.w_matlib)

        # Fill the fields with the machine values (if they're filled)
        self.lf_W1.setValue(self.hole.W1)
        self.lf_W2.setValue(self.hole.W2)
        self.lf_W3.setValue(self.hole.W3)
        self.lf_W4.setValue(self.hole.W4)
        self.lf_H0.setValue(self.hole.H0)
        self.lf_H1.setValue(self.hole.H1)
        self.lf_H2.setValue(self.hole.H2)
        self.lf_H3.setValue(self.hole.H3)

        # Display the main output of the hole (surface, height...)
        self.comp_output()

        # Connect the signal
        self.lf_W1.editingFinished.connect(self.set_W1)
        self.lf_W2.editingFinished.connect(self.set_W2)
        self.lf_W3.editingFinished.connect(self.set_W3)
        self.lf_W4.editingFinished.connect(self.set_W4)
        self.lf_H0.editingFinished.connect(self.set_H0)
        self.lf_H1.editingFinished.connect(self.set_H1)
        self.lf_H2.editingFinished.connect(self.set_H2)
        self.lf_H3.editingFinished.connect(self.set_H3)
        self.w_mat_0.saveNeeded.connect(self.emit_save)
        self.w_mat_1.saveNeeded.connect(self.emit_save)

    def emit_save(self):
        """Send a saveNeeded signal to the DMachineSetup
        """
        self.saveNeeded.emit()

    def set_W1(self):
        """Signal to update the value of W1 according to the line edit

        Parameters
        ----------
        self : PHoleM53
            A PHoleM53 widget
        """
        self.hole.W1 = self.lf_W1.value()
        self.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_W2(self):
        """Signal to update the value of W2 according to the line edit

        Parameters
        ----------
        self : PHoleM53
            A PHoleM53 widget
        """
        self.hole.W2 = self.lf_W2.value()
        self.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_W3(self):
        """Signal to update the value of W3 according to the line edit

        Parameters
        ----------
        self : PHoleM53
            A PHoleM53 widget
        """
        self.hole.W3 = self.lf_W3.value()
        self.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_W4(self):
        """Signal to update the value of W4 according to the line edit

        Parameters
        ----------
        self : PHoleM53
            A PHoleM53 widget
        """
        self.hole.W4 = self.lf_W4.value()
        self.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_H0(self):
        """Signal to update the value of H0 according to the line edit

        Parameters
        ----------
        self : PHoleM53
            A PHoleM53 widget
        """
        self.hole.H0 = self.lf_H0.value()
        self.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_H1(self):
        """Signal to update the value of H1 according to the line edit

        Parameters
        ----------
        self : PHoleM53
            A PHoleM53 widget
        """
        self.hole.H1 = self.lf_H1.value()
        self.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_H2(self):
        """Signal to update the value of H2 according to the line edit

        Parameters
        ----------
        self : PHoleM53
            A PHoleM53 widget
        """
        self.hole.H2 = self.lf_H2.value()
        self.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_H3(self):
        """Signal to update the value of H3 according to the line edit

        Parameters
        ----------
        self : PHoleM53
            A PHoleM53 widget
        """
        self.hole.H3 = self.lf_H3.value()
        self.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def comp_output(self):
        """Compute and display the hole output

        Parameters
        ----------
        self : PHoleM53
            A PHoleM53 widget
        """
        if self.check() is None:
            # We compute the output only if the hole is correctly set
            # Compute all the needed output as string
            s_surf = format(self.u.get_m2(self.hole.comp_surface()), ".4g")
            m_surf = format(self.u.get_m2(self.hole.comp_surface_magnets()), ".4g")
            W5 = format(self.u.get_m(self.hole.comp_W5()), ".4g")

            # Update the GUI to display the Output
            self.out_slot_surface.setText(
                "Slot suface (2 part): " + s_surf + " " + self.u.get_m2_name()
            )
            self.out_magnet_surface.setText(
                "Magnet surface: " + m_surf + " " + self.u.get_m2_name()
            )
            self.out_W5.setText("W5: " + W5 + " " + self.u.get_m_name())

        else:
            # We can't compute the output => We erase the previous version
            # (that way the user know that something is wrong)
            self.out_slot_surface.setText("Slot suface (2 part): ?")
            self.out_magnet_surface.setText("Magnet surface: ?")
            self.out_W5.setText("W5: ?")

    def check(self):
        """Check that the current machine have all the needed field set

        Parameters
        ----------
        self : PHoleM53
            A PHoleM53 widget

        Returns
        -------
        error : str
            Error message (return None if no error)
        """

        # Check that everything is set
        if self.hole.W1 is None:
            return self.tr("You must set W1 !")
        elif self.hole.W2 is None:
            return self.tr("You must set W2 !")
        elif self.hole.W3 is None:
            return self.tr("You must set W3 !")
        elif self.hole.W4 is None:
            return self.tr("You must set W4 !")
        elif self.hole.H0 is None:
            return self.tr("You must set H0 !")
        elif self.hole.H1 is None:
            return self.tr("You must set H1 !")
        elif self.hole.H2 is None:
            return self.tr("You must set H2 !")
        elif self.hole.H3 is None:
            return self.tr("You must set H3 !")

        # Constraints
        try:
            self.hole.check()
        except SlotCheckError as error:
            return str(error)
