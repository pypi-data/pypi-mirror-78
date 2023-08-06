import datetime as dt
from pathlib import Path
from .constants import TRUE_VALUES, FALSE_VALUES
import pandas as pd


class DataFolder:
    def __init__(self, root_data_folder):
        self._root = _ensure_path(root_data_folder)

    def get_root(self):
        return self._root

    def get_procesed(self):
        return self._root / "processed"

    def get_raw(self):
        return self._root / "raw"

    def get_interim(self):
        return self._root / "interim"

    def get_external(self):
        return self._root / "external"

    ROOT = property(get_root)
    RAW = property(get_raw)
    PROCESSED = property(get_procesed)
    EXTERNAL = property(get_external)
    INTERIM = property(get_interim)


def _ensure_path(f):
    return f if isinstance(f, Path) else Path(f)


def get_latest_filename(path, filename_like, file_ext):
    """
    Find absolute path to the file with the latest timestamp 
    given the datasource name and file extension in the path
    
    Parameters
    ----------
    path : Path
        Folder to look for the file
    datasource : str
        Stem name of the file
    file_ext : str
        The name file extension to be looking for
    
    Returns
    -------
    str
        the name of the file (just the file and extension, no directory)

    """
    file_ext = file_ext if "." in file_ext else f".{file_ext}"
    path = _ensure_path(path)
    all_files = [f for f in path.glob(f"{filename_like}*{file_ext}",)]
    assert (
        len(all_files) > 0
    ), f"Unable to find any files like {path / filename_like}{file_ext}"
    fname = max(all_files, key=lambda x: x.stat().st_mtime).name
    return fname


def get_latest_data_filename(path, filename_like):
    """
    Utility method for finding .csv files
    
    Parameters
    ----------
    file_path : Path or str
        Folder to look for the file
    datasource : str
        Stem name of the file
    
    Returns
    -------
    str
        The absolute path of the file, if it exists or None

    """
    return get_latest_filename(path, filename_like, file_ext=".csv")


def make_ts_filename(path, src_name, suffix, with_ts=True):
    """
    Get a path with the filename specified by src_name 
    with or without a timestamp, in the appropriate directory.

    The filename created will have the form 
    'src_name'_[MMdd_HHmmss].'suffix' or
    else the timestamp will be replace with 'latest'.  
    See examples
    
    Parameters
    ----------
    path : str or Path
        The directory where the file will live
    
    src_name: str
        The stem of the filename

    suffix : str
        The file suffix
    
    with_ts : bool, default True
        if True, use the current datetime as a 
        timestamp (MMddHHmmss) to version the file
        if False, do not add a timestamp to the
        filename
    
    Returns
    -------
    A PosixPath representing the full path to 
    the new filename created by the function

    Examples
    --------
    >>> make_ts_fname('/usr/tmp','hello','csv', with_ts=False)
    PosixPath('/usr/tmp/hello_latest.csv')

    """
    NOW = dt.datetime.now()
    TODAY = dt.datetime.today()
    path = _ensure_path(path)
    filename_suffix = (
        f"{TODAY.month:02d}{TODAY.day:02d}_"
        f"{NOW.hour:02d}{NOW.minute:02}{NOW.second:02d}"
        if with_ts
        else "latest"
    )
    fn = f"{src_name}_{filename_suffix}"
    suffix = suffix if "." in suffix else f".{suffix}"
    filename = (path / fn).with_suffix(suffix)
    return filename


def write_data(df, path, src_name, with_ts=True, **kwargs):
    """
    Export the dataset to a file
    
    Parameters:
    ----------
    df : pandas.DataFrame 
        the dataset to write
    path : str or Path
        the path where the file will finally live
    datasource_name : str
        the basefilename to write
    with_ts : bool
        if True, then append timestamp to the filename to be written
        otherwise, append the suffix 'latest' to the basename
    ```***kwargs```
        Keyword arguments supported by `pandas.DataFrame.to_csv()`__ 
            
    Return: Path
    ------
    the name of the file written

    __ https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html

    """
    fn = make_ts_filename(path, src_name=src_name, suffix=".csv", with_ts=with_ts)

    if "float_format" not in kwargs.keys():
        kwargs["float_format"] = "%.3f"
    df.to_csv(fn, **kwargs)
    return fn


def read_latest(path, src_name, **kwargs):
    """
    Read the most recent version of a file (assumes a .csv file) as a `pandas.DataFrame`
    
    Parameters
    ----------
    path : os.Pathlike or str
        the path to search for the data file

    src_name : str
        the stem of the file used to locate the file
   
    Return
    ------
    pandas.DataFrame
        If a file exists it will be attempted to be opened as a pandas dataframe.

    
    """
    fname = get_latest_data_filename(path, src_name)
    # logging.info(f"read from {fname}")
    return pd.read_csv(
        path / fname,
        index_col=0,
        infer_datetime_format=True,
        true_values=TRUE_VALUES,
        false_values=FALSE_VALUES,
        **kwargs,
    )


# def write_excel(data, filename='combined', data_version=False, folder=INTERIM, with_ts=True, **kwargs):
#     """
#     Write multiple data items to a single Excel file.  Where the data is a dictionary of
#     datasources and dataframes
#     :param data: dictionary of sheet names and dataframes
#     :param filename: the name of the excel file to save
#     :param folder: folder to store the excel file
#     :param with_ts: if true, add a timestamp to the filename
#     :param kwargs: other arguments to be passed to the pandas to_excel function
#     :return: the filename of the excel file that was written
#     """
#     logger = logging.getLogger(__name__)
#     logger.info(f"writing {len(data)} to excel... {folder}")
#     fn = make_ts_filename(DATA_PATH / folder, filename, suffix='.xlsx', with_ts=with_ts)

#     if 'float_format' not in kwargs.keys():
#         kwargs['float_format'] = '%.3f'
#     if type(data_version) is bool:
#         data_version = f'_{TODAY.month:02d}{TODAY.day:02d}' if data_version else ''

#     with pd.ExcelWriter(fn) as writer:
#         for datasource, df in data.items():
#             if type(df) is not pd.DataFrame:
#                 continue
#             df.to_excel(writer, sheet_name=f'{datasource}{data_version}', **kwargs)
#     logger.info(f"finished writing df to file... {filename}")
#     return filename


# def get_file_version_from_name(fn):
#     return fn.split('_')[1]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
