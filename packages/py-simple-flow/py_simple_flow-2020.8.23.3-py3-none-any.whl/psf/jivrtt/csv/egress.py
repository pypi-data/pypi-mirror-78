import os
import time
from logging import info

from psf.jivrtt.flow.base import BaseEgress


class CSVEgress(BaseEgress):

    def __init__(
            self,
            output_dir=None,
            file_name=None,
            auto_increment_file_name=False,
            unique_name_column=None,
            append_time_to_file_name=False,
            **kwargs
    ):
        """
        Egresses to a CSV output dir
        :param output_dir: str: the output directory
        :param file_name: str: the file name
        :param auto_increment_file_name: bool: automatically append number to file name
        :param unique_name_column: str: column name, if given would be used to get a file name from data frame
        :param append_time_to_file_name: bool: appends time to the file name
        :param kwargs: any other kwargs that needs to be passed on to pandas.to_csv method
        """
        self._output_dir = output_dir
        self._file_name = file_name
        self._auto_increment_file_name = auto_increment_file_name
        self._unique_name_column = unique_name_column
        self._append_time_to_file_name = append_time_to_file_name
        self._kwargs = kwargs

    def egress(self, transformed_output_dfs):
        """
        Given a list data frames, outputs as CSV to the specified directory
        :param transformed_output_dfs: list of transformed data frames
        """
        for df_index, out_df in enumerate(transformed_output_dfs, 1):
            file_name = self._get_file_name(df_index, out_df)
            file_name = f'{file_name}.csv'
            file_path = os.path.join(self._output_dir or os.getcwd(), file_name)
            out_df.to_csv(file_path, **self._kwargs)
            info(f'Egress-ed to CSV: {file_path}')

    def _get_file_name(self, df_index, out_df):
        file_name = self._file_name or ''
        file_name_from_df = out_df[self._unique_name_column].unique()[0] if self._unique_name_column else ''
        file_name = file_name or file_name_from_df or ''
        file_name = f'{df_index}_{file_name}' if self._auto_increment_file_name else file_name
        time_to_append = time.strftime("%Y%m%d-%H%M%S") if self._append_time_to_file_name else ''
        file_name = f'{file_name}_{time_to_append}'
        return file_name
