# (C) Copyright 2018 ECMWF.
# (C) Copyright 2019 Fondazione Centro Euro-Mediterraneo sui Cambiamenti Climatici
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.
# In applying this licence, CMCC Foundation does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

from __future__ import absolute_import, division, print_function, unicode_literals

import json
import time
import os
import logging

import requests
import xarray as xr


def bytes_to_string(n):
    u = ['', 'K', 'M', 'G', 'T', 'P']
    i = 0
    while n >= 1024:
        n /= 1024.0
        i += 1
    return '%g%s' % (int(n * 10 + 0.5) / 10.0, u[i])


def read_config(path):
    config = {}
    with open(path) as f:
        for l in f.readlines():
            if ':' in l:
                k, v = l.strip().split(':', 1)
                if k in ('url', 'key', 'verify'):
                    config[k] = v.strip()
    return config


class Result(object):

    def __init__(self, client, reply):

        self.reply = reply

        self._url = client.url

        self.session = client.session
        self.robust = client.robust
        self.verify = client.verify
        self.cleanup = client.delete

        self.debug = client.debug
        self.info = client.info
        self.warning = client.warning
        self.error = client.error

        self._deleted = False

    def _download(self, url, size, target):

        if target is None:
            target = url.split('/')[-1]

        ext = url.split('.')[-1]
        if ext == 'zip':
            target = f'{target}.zip'

        self.info("Downloading %s to %s (%s)", url, target, bytes_to_string(size))
        start = time.time()

        r = self.robust(requests.get)(url, stream=True, verify=self.verify)
        try:
            r.raise_for_status()

            total = 0
            with open(target, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        total += len(chunk)
        finally:
            r.close()

        if total != size:
            raise Exception("Download failed: downloaded %s byte(s) out of %s" % (total, size))

        elapsed = time.time() - start
        if elapsed:
            self.info("Download rate %s/s", bytes_to_string(size / elapsed))

        return target

    def download(self, target=None):
        self.debug("Location %s", self.location)
        return self._download(self.location,
                              self.content_length,
                              target)

    def dataset(self):
        return xr.open_dataset(self.location)

    @property
    def content_length(self):
        return int(self.reply['message'].get('file_size'))

    @property
    def location(self):
        return self.reply['message'].get('resource_url')

    @property
    def content_type(self):
        return self.reply['message'].get('content_type')

    def __repr__(self):
        return "Result(content_length=%s,content_type=%s,location=%s)" % (self.content_length,
                                                                          self.content_type,
                                                                          self.location)

    def check(self):
        self.debug("HEAD %s", self.reply['resources_url'])
        metadata = self.robust(self.session.head)(self.reply['resource_url'],
                                                  verify=self.verify)
        metadata.raise_for_status()
        self.debug(metadata.headers)
        return metadata

    # def delete(self):

    #     if self._deleted:
    #         return

    #     if 'job_id' in self.reply:
    #         rid = self.reply['request_id']

    #         task_url = '%s/tasks/%s' % (self._url, rid)
    #         self.debug("DELETE %s", task_url)

    #         delete = self.session.delete(task_url, verify=self.verify)
    #         self.debug("DELETE returns %s %s", delete.status_code, delete.reason)

    #         try:
    #             delete.raise_for_status()
    #         except Exception:
    #             self.warning("DELETE %s returns %s %s",
    #                          task_url, delete.status_code, delete.reason)

    #         self._deleted = True

    # def __del__(self):
    #     try:
    #         if self.cleanup:
    #             self.delete()
    #     except Exception as e:
    #         print(e)

status = {}
status[202] = 'Running' 
status[201] = 'Completed'
status[400] = 'Bad request'


class Client(object):
    """
    Represents the client.

    Parameters
    ----------
    url : str, optional
        The URL.
        Default ``os.environ.get('DIASAPI_URL')``

    key : str, optional
        The key.
        Default ``os.environ.get('DIASAPI_KEY')``

    quiet : bool, optional
        Whether to use quite mode.
        Default ``False``.

    debug : bool, optional
        Whether to use debug mode.
        Default ``False``.

    verify : bool or None, optional
        Whether to verify.
        Default ``None``.

    timeout : int or None, optional
        The session timeout, in seconds. If ``None``, no timeout.
        Default ``None``.

    full_stack : bool, optional
        Whether it is fullstack.
        Default ``False``.

    delete : bool, optional
        Whether to delete.
        Default ``True``.

    retry_max : int, optional
        Maximal number of retry attempts.
        Default ``500``.

    sleep_max : int, optional
        Maximal sleep time, in seconds.
        Default ``120``.

    info_callback : callable or None, optional
        The callback for information.
        Default ``None``.

    warning_callback=None : callable or None, optional
        The callback for warnings.
        Default ``None``.

    error_callback=None : callable or None, optional
        The callback for errors.
        Default ``None``.

    debug_callback=None : callable or None, optional
        The callback for debugging.
        Default ``None``.

    """

    logger = logging.getLogger('diasapi')

    def __init__(self,
                 url=os.environ.get('DIASAPI_URL'),
                 key=os.environ.get('DIASAPI_KEY'),
                 quiet=False,
                 debug=False,
                 verify=None,
                 timeout=None,
                 full_stack=False,
                 delete=True,
                 retry_max=500,
                 sleep_max=120,
                 info_callback=None,
                 warning_callback=None,
                 error_callback=None,
                 debug_callback=None,
                 ):
        """Initialize :class:`Client`."""
        if not quiet:

            if debug:
                level = logging.DEBUG
            else:
                level = logging.INFO

            logging.basicConfig(level=level,
                                format='%(asctime)s %(levelname)s %(message)s')

        dotrc = os.environ.get('DIASAPI_RC', os.path.expanduser('~/.diasapirc'))

        if url is None or key is None:
            if os.path.exists(dotrc):
                config = read_config(dotrc)

                if key is None:
                    key = config.get('key')

                if url is None:
                    url = config.get('url')

                if verify is None:
                    verify = int(config.get('verify', 1))

        if url is None or key is None or key is None:
            raise Exception('Missing/incomplete configuration file: %s' % (dotrc))

        self.url = url
        self.key = key

        self.quiet = quiet
        self.verify = True if verify else False
        self.timeout = timeout
        self.sleep_max = sleep_max
        self.retry_max = retry_max
        self.full_stack = full_stack
        self.delete = delete
        self.last_state = None

        self.debug_callback = debug_callback
        self.warning_callback = warning_callback
        self.info_callback = info_callback
        self.error_callback = error_callback

        self.session = requests.Session()
        self.session.headers.update({'User-Token': self.key})
        self.debug("DIASAPI %s", dict(url=self.url,
                                     key=self.key,
                                     quiet=self.quiet,
                                     verify=self.verify,
                                     timeout=self.timeout,
                                     sleep_max=self.sleep_max,
                                     retry_max=self.retry_max,
                                     full_stack=self.full_stack,
                                     delete=self.delete
                                     ))

    def _submit(self, url, request):

        session = self.session

        self.info("Sending request to %s", url)
        self.debug("POST %s %s", url, json.dumps(request))

        reply = self.robust(session.post)(url, json=request, verify=self.verify)
        return reply

    def _get(self, url):

        session = self.session

        self.info("Sending GET request to %s", url)
        self.debug("GET %s %s", url)

        reply = self.robust(session.get)(url, verify=self.verify)
        return reply

    def retrieve(self, name, request, target=None):
        """
        Retrieve the dataset.

        Creates and saves the dataset that contains the desired data
        from the CMCC catalogs.

        Parameters
        ----------
        name : str
            The name of the dataset.

        request : dict-like
            The arguments passed with the request. Possible options are:

                variable : str, array-like of str
                    The name(s) of the variable(s) that should be loaded
                    from the dataset.

                year, month, day, time : array-like of str or int
                    Years, months, days, and times for which the data
                    and coordinates are loaded.

                area : array-like or dict-like, optional
                    The northern, western, southern, and eastern
                    coordinate bounds of the analyzed area, in degrees.

                    If sequence, it should hold four values in the
                    following order:

                    * north bound latitude coordinate
                    * west bound longitude coordinate
                    * south bound latitude coordinate
                    * east bound longitude coordinate

                    If mapping, the order is not important, but it
                    should hold four key-value pairs:

                    * ``'north':`` north bound latitude coordinate
                    * ``'west':`` west bound longitude coordinate
                    * ``'south':`` south bound latitude coordinate
                    * ``'east':`` east bound longitude coordinate

                reversed_latitude : bool, optional
                    ``True`` if the values of latitude are aranged from
                    south to north and ``False`` otherwise.
                    Default: ``False``.
                    Ignored if `area` is omitted.

                reversed_longitude : bool, optional
                    ``True`` if the values of longitude are aranged from
                    east to west and ``False`` otherwise.
                    Default: ``False``.
                    Ignored if `area` is omitted.

                location : array-like or dict-like, optional
                    The latitude and longitude of the single point, in
                    degrees.

                    If sequence, it should hold two values in the
                    following order:

                    * latitude coordinate
                    * longitude coordinate

                    If mapping, the order is not important, but it
                    should hold two key-value pairs:

                    * ``'latitude':`` latitude coordinate
                    * ``'longitude':`` longitude coordinate

                    Ignored if `area` is provided.

                location_method : {'pad', 'backfill', 'nearest'}, optional
                    The method to use when choosing an inexact location.
                    Default: ``'nearest'``.
                    Ignored if `area` is provided or `location` is
                    omitted.

                format : {'netcdf', 'pickle'}, optional
                    The format of the file to save the data and
                    coordinates.
                    It should match the extension of `target`.

        target : str or None, optional.
            The name of the target file where the dataset is saved.

        Raises
        ------
        Exception
            If any of the following problems occur:

            * Unauthorized access
            * Invalid request
            * Resource not found
            * Unknown API state

        Examples
        --------
        In order to retrieve some data, it is required to create an
        instance of :class:`Client` and call :meth:`retrieve`:

        >>> import diasapi
        >>> client = diasapi.Client()
        >>> client.retrieve(
        ...     name='era5',
        ...     request={
        ...         'variable': 'tp',
        ...         'product_type': 'reanalysis',
        ...         'year': ['2005', '2006', '2012', '2018'],
        ...         'month': ['01', '11', '12'],
        ...         'day': ['01', '02', '31'],
        ...         'time': ['00:00', '06:00', '12:00', '18:00'],
        ...         'area': [55.4, 8.0, 12.1, 23.0],
        ...         'format': 'netcdf',
        ...     },
        ...     target='era5_tp1.nc'
        ... )

        The values that correspond to the keys ``'year'``, ``'month'``,
        ``'day'``, and ``'time'`` can be integers as well, not
        necessarily sorted:

        >>> client.retrieve(
        ...     name='era5',
        ...     request={
        ...         'variable': 'tp',
        ...         'product_type': 'reanalysis',
        ...         'year': [2005, 2006, 2012, 2018],
        ...         'month': [11 , 12, 1],
        ...         'day': [1, 2, 31],
        ...         'time': [0, 6, 12, 18],
        ...         'area': [55.4, 8.0, 12.1, 23.0],
        ...         'format': 'netcdf',
        ...     },
        ...     target='era5_tp1.nc'
        ... )

        If the value of ``'time'`` is an array-like object of integers,
        its items are interpreted as hours.
        The value that corresponds to the key ``'area'`` can be defined
        with a dict-like object as well:

        >>> client.retrieve(
        ...     name='era5',
        ...     request={
        ...         'variable': 'tp',
        ...         'product_type': 'reanalysis',
        ...         'year': [2005, 2006, 2012, 2018],
        ...         'month': [11 , 12, 1],
        ...         'day': [1, 2, 31],
        ...         'time': [0, 6, 12, 18],
        ...         'area': {'east': 23.0, 'west': 8.0,
        ...                  'north': 55.4, 'south': 12.1},
        ...         'format': 'netcdf',
        ...     },
        ...     target='era5_tp1.nc'
        ... )

        If a single location is required, it can be defined by using the
        key ``'location'`` instead of ``'area'``:

        >>> client.retrieve(
        ...     name='era5',
        ...     request={
        ...         'variable': 'rr',
        ...         'product_type': 'reanalysis',
        ...         'year': [2005, 2006, 2012, 2018],
        ...         'month': [11 , 12, 1],
        ...         'day': [1, 2, 31],
        ...         'time': [0, 6, 12, 18],
        ...         'location': [55.68, 12.57],
        ...         'format': 'netcdf',
        ...     },
        ...     target='era5_rr.nc'
        ... )

        >>> client.retrieve(
        ...     name='era5',
        ...     request={
        ...         'variable': 'tp',
        ...         'product_type': 'reanalysis',
        ...         'year': [2005, 2006, 2012, 2018],
        ...         'month': [11 , 12, 1],
        ...         'day': [1, 2, 31],
        ...         'time': [0, 6, 12, 18],
        ...         'location': {'latitude': 55.68,
        ...                      'longitude': 12.57},
        ...         'format': 'netcdf',
        ...     },
        ...     target='era5_tp1.nc'
        ... )

        """
        session = self.session
        if 'format' not in request:
            request['temp_file'] = target
        jreply = self._submit('%s/job/submit/%s' % (self.url, name), request)
        self.info("Request is Submitted")

        job_reply = jreply.json()
        self.debug("JSON reply %s", job_reply)

        if 'job_id' not in job_reply:
            self.warning(f"Job id was not generated. Error occured: {job_reply.get('message')}")
            return job_reply.get('message')
        job_id = job_reply['job_id'] 
        job_url = '%s/job/status/%s' % (self.url, job_id)

        sleep = 1
        start = time.time()

        while True:
            reply = self.robust(session.get)(job_url, verify=self.verify)

            self.debug("REPLY %s", reply)

            if reply.status_code != self.last_state:
                self.info("Request is %s" % (status[reply.status_code]))
                self.last_state = reply.status_code

            if reply.status_code == 201:
                self.debug("Done: %s" % (reply.json()))
                result = Result(self, reply.json())
                if target is not None:
                    result.download(target)
                    return result
                else:
                    return result.dataset()

            if reply.status_code == 202:
                if self.timeout and (time.time() - start > self.timeout):
                    raise Exception('TIMEOUT')

                self.debug("Request ID is %s, sleep %s", job_id, sleep)
                time.sleep(sleep)
                sleep *= 1.5
                if sleep > self.sleep_max:
                    sleep = self.sleep_max

                continue

            if reply.status_code == 401:
                raise Exception("Unauthorized access")

            if reply.status_code == 400:
                self.info(f"Provided request was not valid: {reply.json().get('message')}")
                return

            if reply.status_code == 404:
                raise Exception("Resource not found")

            raise Exception('Unknown API state [%s]' % (reply.status_code,))

    def datasets(self, dataset_name = None):
        """
        Retrieve details for the dataset of the given name or if dataset_name is None, returns
        names of all datasets available in the Catalog.

        Parameters
        ----------
        dataset_name : str
            The name of the dataset.

        Raises
        ------
        Exception
            If any of the following problems occur:

            * Unauthorized access
            * Invalid request
            * Resource not found
            * Unknown API state
        """
        if dataset_name is None:
            self.info("Names of all available datasets were requested")
            req_url = '%s/datasets' % self.url
        else:
            self.info("Details requested for the dataset with the name %s" % dataset_name)
            req_url = '%s/datasets/%s' % (self.url, dataset_name)

        session = self.session
        jreply = self._get(req_url)
        self.info("Request is Submitted")

        job_reply = jreply.json()
        self.debug("JSON reply %s", job_reply)
        return job_reply

    def info(self, *args, **kwargs):
        """Handle info."""
        if self.info_callback:
            self.info_callback(*args, **kwargs)
        else:
            self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        """Handle warning."""
        if self.warning_callback:
            self.warning_callback(*args, **kwargs)
        else:
            self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        """Handle error."""
        if self.error_callback:
            self.error_callback(*args, **kwargs)
        else:
            self.logger.error(*args, **kwargs)

    def debug(self, *args, **kwargs):
        """Debug."""
        if self.debug_callback:
            self.debug_callback(*args, **kwargs)
        else:
            self.logger.debug(*args, **kwargs)

    def robust(self, call):
        """Define helper functions."""
        def retriable(code, reason):

            if code in [requests.codes.internal_server_error,
                        requests.codes.bad_gateway,
                        requests.codes.service_unavailable,
                        requests.codes.gateway_timeout,
                        requests.codes.too_many_requests,
                        requests.codes.request_timeout]:
                return True

            return False

        def wrapped(*args, **kwargs):
            tries = 0
            while tries < self.retry_max:
                try:
                    r = call(*args, **kwargs)
                except requests.exceptions.ConnectionError as e:
                    r = None
                    self.warning("Recovering from connection error [%s], attemps %s of %s",
                                 e, tries, self.retry_max)

                if r is not None:
                    if not retriable(r.status_code, r.reason):
                        return r
                    self.warning("Recovering from HTTP error [%s %s], attemps %s of %s",
                                 r.status_code, r.reason, tries, self.retry_max)

                tries += 1

                self.warning("Retrying in %s seconds", self.sleep_max)
                time.sleep(self.sleep_max)

        return wrapped

