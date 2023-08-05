import pandas

from psf.jivrtt.flow.base import BaseSource


class CSVSource(BaseSource):

    def read(self, file_names=None, **kwargs):
        """
        Reads the data from file names provided
        :param file_names: list of file names
        :param kwargs: the keyword args to be passed in to pandas.read_csv
        :return: list of data frames with the time series
        """
        ts_dfs = [pandas.read_csv(file_name, **kwargs) for file_name in file_names]
        return ts_dfs
