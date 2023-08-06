import pandas as pd
import pkg_resources


def load_data():
    resource_path = '/'.join(('data', 'USArrests.zip'))
    return pd.read_csv(pkg_resources.resource_filename(__name__,
                                                       resource_path),
                       index_col=0)
