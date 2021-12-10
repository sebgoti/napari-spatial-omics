import numpy as np
import pandas as pd
from napari_plugin_engine import napari_hook_implementation


class CSVIO:
    """Read data from csv file

    Parameters
    ----------
    file_path : str
        Path to the csv file

    """
    def __init__(self, file_path):
        self.file_path = file_path

    def is_compatible(self):
        if self.file_path.endswith('.csv'):
            return True
        return False

    def read(self):
        df = pd.read_csv(self.file_path)
        df = df.fillna('None')
        #df_gene = df[df['target'] != np.nan]
        #self.data = np.column_stack([df_gene['yc'], df_gene['xc']])
        self.total_data = (np.column_stack([df['yc'], df['xc']]), df['target'])

def is_compatible(file_path):
    # CSV
    csv_reader = CSVIO(file_path)
    if csv_reader.is_compatible():
        return True

    return None


def read_spots(file_path):
    print("read spots:", file_path)
    # CSV
    csv_reader = CSVIO(file_path)
    if csv_reader.is_compatible():
        csv_reader.read()
        return csv_reader.total_data

    return None

@napari_hook_implementation
def napari_get_reader(path):
    """A basic implementation of the napari_get_reader hook specification.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    function or None
        If the path is a recognized format, return a function that accepts the
        same path or list of paths, and returns a list of layer data tuples.
    """
    #if isinstance(path, list):
        # reader plugins may be handed single path, or a list of paths.
        # if it is a list, it is assumed to be an image stack...
        # so we are only going to look at the first file.
        #path = path[0]

    # if we know we cannot read the file, we immediately return None.
    #if not path.endswith(".csv"):
        #return None
    if isinstance(path, list):
        # reader plugins may be handed single path, or a list of paths.
        # if it is a list, it is assumed to be an image stack...
        # so we are only going to look at the first file.
        path = path[0]

    # if we know we cannot read the file, we immediately return None.
    if not is_compatible(path):
        return None

    # otherwise we return the *function* that can read ``path``.
    return reader_function


def reader_function(path):
    """Take a path or list of paths and return a list of LayerData tuples.

    Readers are expected to return data as a list of tuples, where each tuple
    is (data, [add_kwargs, [layer_type]]), "add_kwargs" and "layer_type" are
    both optional.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    layer_data : list of tuples
        A list of LayerData tuples where each tuple in the list contains
        (data, metadata, layer_type), where data is a numpy array, metadata is
        a dict of keyword arguments for the corresponding viewer.add_* method
        in napari, and layer_type is a lower-case string naming the type of layer.
        Both "meta", and "layer_type" are optional. napari will default to
        layer_type=="image" if not provided
    """
    # handle both a string and a list of strings
    #paths = [path] if isinstance(path, str) else path
    # load all files into array
    #arrays = [np.load(_path) for _path in paths]
    # stack arrays into single array
    #data = np.squeeze(np.stack(arrays))

    # optional kwargs for the corresponding viewer.add_* method
    if isinstance(path, list):
        path = path[0]

    data_frame1, data_frame2 = read_spots(path)

    spots = data_frame1

    add_kwargs = {
        'properties': {'gene': data_frame2}
    }  # optional kwargs for the corresponding viewer.add_* method

    layer_type = "points"  # optional, default is "image"

    layer_data = (
        spots,
        add_kwargs,
        layer_type
    )
    #return [(np.array(spot_coordinates), add_kwargs, layer_type)]

    return layer_data

