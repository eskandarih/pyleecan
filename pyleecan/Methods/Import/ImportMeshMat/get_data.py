# -*- coding: utf-8 -*-

from os.path import splitext

import numpy as np
from numpy import int32

from ....Classes.ElementMat import ElementMat
from ....Classes.ImportMeshUnv import ImportMeshUnv
from ....Classes.Interpolation import Interpolation
from ....Classes.MeshMat import MeshMat
from ....Classes.NodeMat import NodeMat
from ....Classes.RefQuad4 import RefQuad4
from ....Classes.RefTriangle3 import RefTriangle3


def get_data(self):
    """Import mesh and generate MeshMat object

    Parameters
    ----------
    self : ImportData
        An ImportData object

    Returns
    -------
    mesh: MeshMat
        The generated MeshMat object

    """

    # Get mesh data (nodes and elements)
    if splitext(self.file_path)[1] == ".unv":
        nodes, elements = ImportMeshUnv(self.file_path).get_data()
    else:
        raise Exception(splitext(self.file_path)[1] + " files are not supported")

    # Define MeshMat object
    if min(nodes[:, 0]) == 0 and max(nodes[:, 0]) == len(nodes[:, 0]) - 1:
        is_renum = False
    else:
        is_renum = True

    mesh = MeshMat(_is_renum=is_renum)
    mesh.label = "Imported mesh"

    node_indices = nodes[:, 0].astype(int32)

    # Node indices must start at 0 and be consecutive
    unique_node_indices = np.sort(np.unique(node_indices))
    if np.any(unique_node_indices != np.arange(unique_node_indices.size)):
        for new_index, old_index in enumerate(unique_node_indices):
            node_indices[node_indices == old_index] = new_index

            # Change indices in element connectivity value
            for element in elements.values():
                element[:, 1:][element[:, 1:] == old_index] = new_index

    # Define NodeMat object
    mesh.node = NodeMat(
        coordinate=nodes[:, 1:],
        nb_node=nodes.shape[0],
        indice=node_indices,
    )

    # Ensure that element indices are between 0 and nb_element - 1
    element_indices = np.hstack(
        [elt[:, 0].astype(np.int32) for elt in elements.values()]
    )

    unique_element_indices = np.unique(element_indices)  # Values returned are sorted

    if unique_element_indices.size < element_indices.size:
        raise ValueError("Duplicated element index")

    min_indice = 0
    if (
        unique_element_indices[0] != 0
        or unique_element_indices[-1] != unique_element_indices.size - 1
    ):
        # Refactor indices
        for element in elements.values():
            nb_element = element.shape[0]
            indices = np.arange(min_indice, min_indice + nb_element)
            element[:, 0] = indices
            min_indice += nb_element

    # Define ElementMat objects
    for elt_type, elt in elements.items():
        element = ElementMat(
            connectivity=elt[:, 1:],
            nb_element=elt.shape[0],
            nb_node_per_element=elt.shape[1] - 1,
            indice=elt[:, 0].astype(np.int32),
        )
        # Add element of reference using names from pyUFF
        if elt_type == "triangle":
            element.interpolation = Interpolation(ref_element=RefTriangle3())
        elif elt_type == "quad":
            element.interpolation = Interpolation(ref_element=RefQuad4())
        else:
            raise ValueError(f"Wrong element type {elt_type}.")

        mesh.element[elt_type] = element

    return mesh
