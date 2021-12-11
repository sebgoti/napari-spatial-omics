from typing import TYPE_CHECKING
#from enum import Enum
import numpy as np
from napari.layers import Points
from napari_plugin_engine import napari_hook_implementation
if TYPE_CHECKING:
    import napari


# This is the actual plugin function, where we export our function
# (The functions themselves are defined below)
@napari_hook_implementation
def napari_experimental_provide_function():
    # we can return a single function
    # or a tuple of (function, magicgui_options)<-------
    # or a list of multiple functions with or without options, as shown here:
    return read_spots

def read_spots(
        points: "napari.layers.Points",
        gene: str = 'IGHG1',
        gene_color: str = 'red',
        marker_size: str = '10'
) -> "napari.layers.Points":#"napari.types.LayerDataTuple":
    """Retrieve points' data from selected group of genes.

    Parameters
    ----------
    points: napari.types.PointsData
        The raw data from a decoded CSV file
    gene: str
        string of gene to visualize.
    gene_color: str
        color to display points in layer
    marker_size: str
        size of points

    Returns
    -------
    layer_data: napari.types.LayerDataTuple
        The layer data tuple containing the corresponding
        points and metadata for visualization.
    """
    #genes_list = genes.split(',')
    #genes_dict_cmap = {g: i for i, g in enumerate(genes_list)}

    #color_cycle = color_s.split(',')
    #size_cycle = [int(i) for i in size_s.split(',')]

    #spots_idx = [genes_dict_cmap[g] for g in points.properties['gene'] if g in genes_list]
    # spots_idx = [genes_dict_cmap[gene] for gene in points.properties['gene']]
    selected_points = [points.data[i].tolist() for i in range(len(points.data)) if points.properties['gene'][i] == gene]

    # List with indices of selected genes by user.
    #selected_points_idx = [i for i in range(len(points.data)) if points.properties['gene'][i] in genes_list]

    # Here we select the data coordinates and labels/index of requested genes:
    #selected_data = [points.data[i] for i in selected_points_idx]
    #selected_idx = spots_idx#[spots_idx[i] for i in selected_points_idx]

    #spot_properties = {'label': selected_idx}
    gene_color_prop = [gene_color for i in range(len(selected_points))]
    marker_size_prop = [int(marker_size) for k in range(len(selected_points))]
    #face_color = {
    #    'colors': 'label',
    #    'color_mode': 'cycle',
    #    'categorical_colormap': color_cycle
    #}
    #layer_type = "points"
    #layer_data = (
    #    selected_data,
        #{'face_color': 'magenta',
        # 'symbol': 'ring'},
    #    {'properties': spot_properties,
    #     'size': size_cycle,
    #     'face_color': face_color},
    #    layer_type
    #)

    #return (selected_points, {'face_color': gene_color_prop, 'size': marker_size_prop}, 'points')
    #return (np.random.rand(1200, 1200),)
    return Points(selected_points, size=int(marker_size), face_color=gene_color)


