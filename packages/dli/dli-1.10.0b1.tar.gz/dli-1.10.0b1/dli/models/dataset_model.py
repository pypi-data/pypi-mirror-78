#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import io
import json
import os
import textwrap
import uuid
import warnings
import pandas
import pyarrow
import datetime

from typing import List, Optional
from urllib.parse import urljoin

from tabulate import tabulate
from s3transfer.manager import TransferManager


from dli.aws import create_refreshing_session
from dli.client import utils
from dli.models import log_public_functions_calls_using, SampleData, \
    AttributesDict
from dli.client.aspects import analytics_decorator, logging_decorator
from dli.client.components.urls import consumption_urls, dataset_urls
from dli.client.exceptions import DataframeStreamingException
from dli.models.dictionary_model import DictionaryModel
from dli.models.file_model import get_or_create_os_path


import logging
trace_logger = logging.getLogger('trace_logger')


class DatasetModel(AttributesDict):

    @property
    def sample_data(self) -> SampleData:
        return SampleData(self)

    @property
    def id(self):
        return self.dataset_id

    def __init__(self, **kwargs):
        super().__init__(**kwargs,)
        self.instances = self._client._InstancesCollection(dataset=self)
        self.fields_metadata = None

    @classmethod
    def _from_v2_response(cls, response_json):
        return cls._construct_dataset_using(
            response_json['data']['attributes'], response_json['data']['id']
        )

    @classmethod
    def _from_v2_response_unsheathed(cls, response_json):
        return cls._construct_dataset_using(
            response_json['attributes'], response_json['id']
        )

    @classmethod
    def _from_v1_response_to_v2(cls, v1_response):
        response = cls._client.session.get(
            dataset_urls.v2_by_id.format(
                id=v1_response['properties']['datasetId']
            )
        )

        return cls._from_v2_response(response.json())

    @classmethod
    def _from_v2_list_response(cls, response_json):
        return [
            cls._construct_dataset_using(
                dataset['attributes'], dataset['id']
            )
            for dataset in response_json['data']
        ]

    @classmethod
    def _construct_dataset_using(cls, attributes, dataset_id):
        location = attributes.pop('location')
        # In the interests of not breaking backwards compatability.
        # TODO find a way to migrate this to the new nested API.
        if not location:
            location = None
        else:
            location = location[next(iter(location))]
        return cls(
            **attributes,
            location=location,
            dataset_id=dataset_id
        )

    def dask_dataframe(
        self,
        # Parameters for reading from .parquet format files:
        columns=None,
        filters=None,
        categories=None,
        index=None,
        engine="auto",
        gather_statistics=None,
        split_row_groups=None,
        chunksize=None,
        # Parameters for reading from .csv format files:
        blocksize='default',
        lineterminator=None,
        compression=None,
        sample=256000,
        enforce=False,
        assume_missing=False,
        include_path_column=False,
        # Parameters for reading from .parquet and .csv formats:
        **kwargs
    ):
        """
        Read a dataset into a Dask DataFrame.

        A Dask DataFrame can be used to compute a Pandas Dataframe.
        Dask has the advantage of being able to
        process data that would be too large to fit into memory in a single
        Pandas Dataframe. The use case is to read the files with Dask, apply
        operations such as filtering and sorting to the Dask Dataframe (which
        implements most of the Pandas API) and finally compute the result to a
        Pandas Dataframe. As you have done the filtering in Dask, the Pandas
        Dataframe will be smaller in memory than if you tried to do everything
        in a single Pandas Dataframe.

        This endpoint can read data files in the following file formats:
            .parquet
            .csv
        into a Dask.dataframe, one file per
        partition.  It selects the index among the sorted columns if any exist.


        Examples
        --------
        >>> dataset.dask_dataframe()

        The Dask dataframe will calculate the tasks that need to be run, but
        it does not evaluate until you call an action on it. To run a full
        evaluation across the whole dataset and return a Pandas dataframe, run:

        >>> dataset.dask_dataframe().compute()

        To run the evaluation and only return the first ten results:

        >>> dataset.dask_dataframe().compute(10)

        An additional parameter needs to be added when you are reading from
        compressed .csv files, for example the .csv.gz format.

        >>> dataset.dask_dataframe(compression='gzip')

        Some datasets have problems with the column types changing between
        different data files. Dask will stop with an error message that
        explains the types you should pass. For example, if the error message
        that looks like this:

        /*
        ValueError: Mismatched dtypes found in `pd.read_csv`/`pd.read_table`.

        +------------+---------+----------+
        | Column     | Found   | Expected |
        +------------+---------+----------+
        | STATE_FIPS | float64 | int64    |
        +------------+---------+----------+

        Usually this is due to dask's dtype inference failing, and
        *may* be fixed by specifying dtypes manually by adding:

        dtype={'STATE_FIPS': 'float64'}
        */

        then you should do as the message says and add the parameters, then
        re-run. In this case the fix would look like this:

        >>> dataset.dask_dataframe(dtype = {'STATE_FIPS': 'float64'})



        You are able to provide extra parameters to this endpoint that will
        be used by dask.

        The following parameters are used to reading from
        .parquet format files:

        Parameters
        ----------
        columns : string, list or None (default)
            Field name(s) to read in as columns in the output. By default all
            non-index fields will be read (as determined by the pandas parquet
            metadata, if present). Provide a single field name instead of a list to
            read in the data as a Series.
        filters : Union[List[Tuple[str, str, Any]], List[List[Tuple[str, str, Any]]]]
            List of filters to apply, like ``[[('x', '=', 0), ...], ...]``. This
            implements partition-level (hive) filtering only, i.e., to prevent the
            loading of some row-groups and/or files.

            Predicates can be expressed in disjunctive normal form (DNF). This means
            that the innermost tuple describes a single column predicate. These
            inner predicates are combined with an AND conjunction into a larger
            predicate. The outer-most list then combines all of the combined
            filters with an OR disjunction.

            Predicates can also be expressed as a List[Tuple]. These are evaluated
            as an AND conjunction. To express OR in predictates, one must use the
            (preferred) List[List[Tuple]] notation.
        index : string, list, False or None (default)
            Field name(s) to use as the output frame index. By default will be
            inferred from the pandas parquet file metadata (if present). Use False
            to read all fields as columns.
        categories : list, dict or None
            For any fields listed here, if the parquet encoding is Dictionary,
            the column will be created with dtype category. Use only if it is
            guaranteed that the column is encoded as dictionary in all row-groups.
            If a list, assumes up to 2**16-1 labels; if a dict, specify the number
            of labels expected; if None, will load categories automatically for
            data written by dask/fastparquet, not otherwise.
        engine : {'auto', 'fastparquet', 'pyarrow'}, default 'auto'
            Parquet reader library to use. If only one library is installed, it
            will use that one; if both, it will use 'fastparquet'
        gather_statistics : bool or None (default).
            Gather the statistics for each dataset partition. By default,
            this will only be done if the _metadata file is available. Otherwise,
            statistics will only be gathered if True, because the footer of
            every file will be parsed (which is very slow on some systems).
        split_row_groups : bool or int
            Default is True if a _metadata file is available or if
            the dataset is composed of a single file (otherwise defult is False).
            If True, then each output dataframe partition will correspond to a single
            parquet-file row-group. If False, each partition will correspond to a
            complete file.  If a positive integer value is given, each dataframe
            partition will correspond to that number of parquet row-groups (or fewer).
            Only the "pyarrow" engine supports this argument.
        chunksize : int, str
            The target task partition size.  If set, consecutive row-groups
            from the same file will be aggregated into the same output
            partition until the aggregate size reaches this value.
        **kwargs: dict (of dicts)
            Passthrough key-word arguments for read backend.
            The top-level keys correspond to the appropriate operation type, and
            the second level corresponds to the kwargs that will be passed on to
            the underlying `pyarrow` or `fastparquet` function.
            Supported top-level keys: 'dataset' (for opening a `pyarrow` dataset),
            'file' (for opening a `fastparquet` `ParquetFile`), 'read' (for the
            backend read function), 'arrow_to_pandas' (for controlling the arguments
            passed to convert from a `pyarrow.Table.to_pandas()`)

        The following parameters are used to reading from
        .csv format files:

        Parameters
        ----------

        blocksize:str, int or None, optional
            Number of bytes by which to cut up larger files. Default value is
            computed based on available physical memory and the number of
            cores, up to a maximum of 64MB. Can be a number like 64000000` or
            a string like ``"64MB". If None, a single block is used for each
            file.
        lineterminator:str (length 1), optional
            Character to break file into lines. Only valid with C parser.
        compression: {‘infer’, ‘gzip’, ‘bz2’, ‘zip’, ‘xz’, None}, default
            ‘infer’
            For on-the-fly decompression of on-disk data.
        sample:int, optional
            Number of bytes to use when determining dtypes
        enforce:bool
        assume_missing:bool, optional
            If True, all integer columns that aren’t specified in dtype are
            assumed to contain missing values, and are converted to floats.
            Default is False.
        include_path_column:bool or str, optional
            Whether or not to include the path to each particular file. If
            True a new column is added to the dataframe called path. If str,
            sets new column name. Default is False.
        **kwargs
            Extra keyword arguments. See the docstring for pandas.read_csv()
            for more information on available keyword arguments.
        """
        try:
            import dask.dataframe as dd
        except ImportError:
            raise RuntimeError(
                'Before you can use Dask it must be installed into '
                'your virtual environment.'
                '\nNote: If you are running you code in a Jupyter Notebook, '
                'then before installing you will need to quit the '
                '`jupyter notebook` process that is running on the command '
                'line and start it again so that your notebooks see the '
                'version of Dask you have now installed.'
                '\nPlease install dask using one of the following options:'
                '\n1. Run `pip install dli[dask]` to install this SDK '
                'with a compatible version of dask.'
                '\n2. Run `pip install dask[dataframe]` to install the latest '
                'version of dask (which may be untested with this version '
                'of the SDK).'
            )

        if not self.has_access:
            raise Exception(
                'Unfortunately the user you are using '
                'does not have access to this dataset. '
                'Please request access to the package/dataset '
                "to be able to retrieve this content."
            )

        start = datetime.datetime.now()
        endpoint_url = f'https://{self._client._environment.s3_proxy}'
        request_id = str(uuid.uuid4())

        def add_request_id_to_session(**kwargs):
            kwargs["request"].headers['X-Request-ID'] = request_id
            trace_logger.info(
                f'GET Request to https://{self._client._environment.s3_proxy} '
                f'with request_id: {request_id}'
            )

        s3_resource = create_refreshing_session(
            dli_client_session=self._client.session,
            event_hooks=add_request_id_to_session
        ).resource(
            's3',
            endpoint_url=endpoint_url
        )

        bucket = s3_resource.Bucket(
            self.organisation_short_code
        )

        filter_prefix = self.short_code + (
            '' if self.short_code.endswith('/') else '/'
        )

        def _to_s3_proxy_path(object_summary):
            return f"s3://{self.organisation_short_code}/{object_summary.key}"

        paths = [_to_s3_proxy_path(object_summary) for object_summary in
                 bucket.objects.filter(
                     # Prefix searches for exact matches and folders
                     Prefix=filter_prefix
                 ) if not object_summary.key.endswith('/')]

        storage_options = {
            'client_kwargs': {
                'endpoint_url': endpoint_url,
            },
            'key': self._client.session.auth_key,
            'secret': 'noop',
        }

        data_format = self.data_format.lower()

        trace_logger.info(
            'dask_dataframe endpoint:'
            f"\nrequest_id: '{request_id}'"
            f"\nendpoint_url: '{endpoint_url}'"
            f"\ndata_format: '{data_format}'"
            '\nlisting paths (before filtering) elapsed time: '
            f"'{datetime.datetime.now() - start}'"
            f"\nnumber of paths (before filtering): '{len(paths)}'"
        )

        if data_format == 'parquet':
            return dd.read_parquet(
                path=paths,
                columns=columns,
                filters=filters,
                categories=categories,
                index=index,
                storage_options=storage_options,
                engine=engine,
                gather_statistics=gather_statistics,
                split_row_groups=split_row_groups,
                chunksize=chunksize,
                **kwargs
            )
        elif data_format == 'csv':
            return dd.read_csv(
                urlpath=paths,
                blocksize=blocksize,
                lineterminator=lineterminator,
                compression=compression,
                sample=sample,
                enforce=enforce,
                assume_missing=assume_missing,
                storage_options=storage_options,
                include_path_column=include_path_column,
                **kwargs
            )
        else:
            print(
                f"Sorry, the dataset is in the format '{data_format}'. This "
                'endpoint is only setup to handle parquet and csv.'
            )
            return None

    def download(
        self,
        destination_path: str,
        flatten: Optional[bool] = False,
        filter_path: Optional[str] = None
    ) -> List[str]:
        """
        Downloads all files from the latest instance into the provided
        destination path.
        This is a short-cut function for:
        `Dataset.instances.latest().download(destination_path)`

        :param destination_path: required. The path on the system, where the
            files should be saved. Must be a directory, if doesn't exist, will
            be created.

        :param bool flatten: The default behaviour (=False) is to use the s3
            file structure when writing the downloaded files to disk.

        :param str filter_path: if provided only a subpath matching the filter_path
            will be downloaded


        :return: the list of the files that were downloaded successfully. Any
            failures will be printed.


        :example:

            Downloading without flatten:

            .. code-block:: python

                >>> dataset.download('./local/path/')
                [
                  'as_of_date=2019-09-10/type=full/StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',
                  'as_of_date=2019-09-11/type=full/StormEvents_details-ftp_v1.0_d1951_c20160223.csv.gz'
                ]

        :example:

            Downloading with ``filter_path``

            .. code-block:: python

                >>> dataset.download(
                    './local/path/', filter_path='as_of_date=2019-09-10/'
                )
                [
                  'as_of_date=2019-09-10/type=full/StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',
                ]


        :example:

            When flatten = True, we remove the s3 structure. Example:

            Example output for new behaviour:

            .. code-block:: python

                >>> dataset.download('./local/path/', flatten=True)
                [
                  'StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',
                  'StormEvents_details-ftp_v1.0_d1951_c20160223.csv.gz'
                ]


        """

        if not self.has_access:
            raise Exception(
                'Unfortunately the user you are using '
                'does not have access to this dataset. '
                'Please request access to the package/dataset '
                "to be able to retrieve this content."
            )

        def add_request_id_to_session(**kwargs):
            request_id = str(uuid.uuid4())
            kwargs["request"].headers['X-Request-ID'] = request_id
            trace_logger.info(
                f'GET Request to https://{self._client._environment.s3_proxy} '
                f'with request_id: {request_id}'
            )

        s3_resource = create_refreshing_session(
            dli_client_session=self._client.session,
            event_hooks=add_request_id_to_session
        ).resource(
            's3',
            endpoint_url=f'https://{self._client._environment.s3_proxy}'
        )

        s3_client = s3_resource.meta.client
        with TransferManager(s3_client) as transfer_manager:

            bucket = s3_resource.Bucket(
                self.organisation_short_code
            )

            _paths_and_futures = []

            filter_prefix = self.short_code + (
                    '' if self.short_code.endswith('/') else '/'
            )

            if filter_path:
                filter_prefix = filter_prefix + filter_path.lstrip('/')

            # TODO parallelize this again?
            for object_summary in bucket.objects.filter(
                # Prefix searches for exact matches and folders
                Prefix=filter_prefix
            ):
                if not object_summary.key.endswith('/'):
                    to_path = get_or_create_os_path(
                        object_summary.key,
                        to=destination_path,
                        flatten=flatten
                    )

                    self._client.logger.info(
                        f'Downloading {object_summary.key} to: {to_path}...'
                    )

                    if os.path.exists(to_path):
                        warnings.warn(
                            'File already exists. Overwriting.'
                        )

                    # returns a future
                    future = transfer_manager.download(
                        self.organisation_short_code,
                        object_summary.key,
                        to_path
                    )

                    _paths_and_futures.append((to_path, future))

            _successful_paths = []
            for path, future in _paths_and_futures:
                try:
                    # This will block for this future to complete, but other
                    # futures will keep running in the background.
                    future.result()
                    _successful_paths.append(path)
                except Exception as e:
                    message = f'Problem while downloading:' \
                        f'\nfile path: {path}'\
                        f'\nError message: {e}\n\n'

                    self._client.logger.error(message)
                    print(message)

            return _successful_paths

    def _dataframe(self, nrows=None, partitions: List[str] = None, raise_=True):
        warnings.warn(
            'This method is deprecated. Please use `dataframe` (note the '
            'underscore has been removed)',
            DeprecationWarning
        )
        self.dataframe(nrows=nrows, partitions=partitions, raise_=raise_)

    def dataframe(self, nrows=None, partitions: List[str] = None, raise_=True,
                   use_compression: bool = False) -> 'pandas.DataFrame':
        """
        Return the data from the files in the latest instance of the dataset
        as a pandas DataFrame.

        We currently support .csv and .parquet as our data file formats. The
        data files in the latest instance could all be .csv format or all be
        .parquet format. If there is a mix of .csv and .parquet or some other
        file format then we will not be able to parse the data and will
        return an error message.

        :param int nrows: Optional. The max number of rows to return.
            We use the nrows parameter to limit the amount of rows that are
            returned, otherwise for very large dataset it will take a long time
            or you could run out of RAM on your machine!
            If you want all of the rows, then leave this parameter set to the
            default None.

        :param List[str] partitions: Optional. A dict of filters (partitions) to
            apply to the dataframe request in the form of: `["a=12","b>20190110"]`
            - will permit whitespace and equality operators `[<=, <, =, >, >=]`

        :param bool raise_: Optional. Raise exception if the dataframe stream
            stopped prematurely

        :param use_compression: Optional. Whether the response from the
        backend should use compression. Setting to false should result
        in a faster initial response before the streaming begins.

        :example:

            Basic usage:

            .. code-block:: python

                    dataframe = dataset.dataframe()

        :example:

            Dataframe filtered by partition with nrows (partitions can be fetched
            via `dataset.partitions()`:

            .. code-block:: python

                    dataframe = dataset.dataframe(
                        nrows=1000,
                        partitions=["as_of_date=2017-03-07"]
                    )

        """

        if not self.has_access:
            raise Exception(
                'Unfortunately the user you are using '
                'does not have access to this dataset. '
                'Please request access to the package/dataset '
                "to be able to retrieve this content."
            )

        params = {}

        if nrows is not None:
            params['filter[nrows]'] = nrows

        if partitions is not None:
            params['filter[partitions]'] = partitions

        dataframe_url = urljoin(
            self._client._environment.consumption,
            consumption_urls.consumption_dataframe.format(id=self.id)
        )

        headers = {}
        if not use_compression:
            headers['Accept-Encoding'] = 'identity;q=0'

        response = self._client.session.get(
            dataframe_url, stream=True,
            params=params,
            headers=headers,
        )

        # native_file only reads until end of dataframe
        # the rest of the stream has to be read from response raw.
        native_file = pyarrow.PythonFile(response.raw, mode='rb')

        # Now native_file "contains the complete stream as an in-memory
        # byte buffer. An important point is that if the input source supports
        # zero-copy reads (e.g. like a memory map, or pyarrow.BufferReader),
        # then the returned batches are also zero-copy and
        # do not allocate any new memory on read."
        reader = pyarrow.ipc.open_stream(native_file)
        dataframe = reader.read_pandas()

        # The pyarrow buffered stream reader stops once it
        # reaches the end of the IPC message. Afterwards we
        # get the rest of the data which contains the summary
        # of what we've downloaded including an error message.
        last_packet = response.raw.read()
        summary = json.loads(last_packet)

        if summary['status'] >= 400:
            exception = DataframeStreamingException(
                summary, dataframe_url, response=response,
            )

            # Optionally ignore bad data
            if raise_:
                raise exception
            else:
                warnings.warn(
                    str(exception),
                    UserWarning
                )

        return dataframe

    def _partitions(self):
        warnings.warn(
            'This method is deprecated. Please use `partitions` (note the '
            'underscore has been removed)',
            DeprecationWarning
        )
        self.partitions()

    def partitions(self) -> dict:
        """
        Retrieves the list of available partitions for a given dataset.

        The data onboarding team have structured the file paths on S3 with
        simple partitions e.g. `as_of_date` or `location`.

        Their aim was to separate the data to reduce the size of the
        individual files. For example, data that has a `location` column with
        the options `us`, `eu` and `asia` can be separated into S3 paths like
        so:

        .. code-block::

            package-name/dataset/as_of_date=2019-09-10/location=eu/filename.csv
            package-name/dataset/as_of_date=2019-09-10/location=us/filename.csv

        in this case the `partitions` will be returned as:

        .. code-block::

            {'as_of_date': ['2019-09-10'], 'location': ['eu', 'us]}
        """
        response = self._client.session.get(
            urljoin(
                self._client._environment.consumption,
                consumption_urls.consumption_partitions.format(id=self.id)
            )
        )

        return response.json()["data"]["attributes"]["partitions"]

    def contents(self):
        """
        Print IDs for all the instances in this dataset.

        Example output:

            INSTANCE 1111aaa-11aa-11aa-11aa-111111aaaaaa
        """
        for p in self.instances.all():
            print(str(p))

    def dictionary(self) -> List[dict]:

        if self.fields_metadata is None:
            # we have to do two calls
            # to get the latest dictionary id for the dataset
            try:
                response = self._client.session.get(
                    dataset_urls.dictionary_by_dataset_lastest.format(id=self.id)
                ).json()
            except:
                print("There is no current dictionary available.")
                return []

            # followed by the fields for the dictionary...


            self.fields_metadata = DictionaryModel(
                {'id': response["data"]["id"], 'attributes': {}}, client=self._client
            ).fields

            def subdict(field_dict, keep):
                return{k: v for k, v in field_dict.items() if k in keep}

            self.fields_metadata = list(
                map(lambda field: subdict(field, ["name", "nullable", "type"]),
                    self.fields_metadata)
            )

        return self.fields_metadata

    def info(self):
        fields = self.dictionary()

        df = pandas.DataFrame(fields)
        if df.shape[1] > 0:
            df["type"] = df.apply(
                lambda row: row["type"] + (" (Nullable)" if row["nullable"] else ""),
                axis=1)
            df = df[["name", "type"]]

            print(tabulate(df, showindex=False, headers=df.columns))
        else:
            print("No columns/info available.")

    def metadata(self):
        """
        Once you have selected a dataset, you can print the metadata (the
        available fields and values).

        :example:

            .. code-block:: python
                # Get all datasets.
                >>> datasets = client.datasets()

                # Get metadata of the 'ExampleDatasetShortCode' dataset.
                >>> datasets['ExampleDatasetShortCode'].metadata()

        :example:

            .. code-block:: python
                # Get an exact dataset using the dataset_short_code and
                # organisation_short_code.
                >>> dataset = client.get_dataset(dataset_short_code='ExampleDatasetShortCode', organisation_short_code='IHSMarkit')
                # Get metadata of the dataset.
                >>> dataset.metadata()

        :example:

            .. code-block:: python
                # Get all datasets.
                >>> dataset = client.datasets()['ExampleDatasetShortCode']
                # Get metadata of the dataset.
                >>> dataset.metadata()

        :return: Prints the metadata.
        """
        utils.print_model_metadata(self)

    def __repr__(self):
        return f'<Dataset short_code={self.short_code}>'

    def __str__(self):
        separator = "-" * 80
        splits = "\n".join(textwrap.wrap(self.description))

        return f"\nDATASET \"{self.short_code}\" [{self.data_format}]\n" \
               f">> Shortcode: {self.short_code}\n"\
               f">> Available Date Range: {self.first_datafile_at} to {self.last_datafile_at}\n" \
               f">> ID: {self.id}\n" \
               f">> Published: {self.publishing_frequency} by {self.organisation_name}\n" \
               f">> Accessible: {self.has_access}\n" \
               f"\n" \
               f"{splits}\n" \
               f"{separator}"


log_public_functions_calls_using(
    [analytics_decorator, logging_decorator],
    class_fields_to_log=['dataset_id']
)(DatasetModel)
