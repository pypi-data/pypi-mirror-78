import logging

from psf.jivrtt.flow.base import BaseIngress


class CSVIngress(BaseIngress):

    def ingress(self, input_dfs):
        """
        Just for traceability purposes. Logs summary of data
        :param input_dfs: the input data frames read
        """
        for ts_df in input_dfs:
            logging.info(f"Ingress: Got data from CSV as data frame")
            logging.debug(f"{ts_df.head(2)}")
