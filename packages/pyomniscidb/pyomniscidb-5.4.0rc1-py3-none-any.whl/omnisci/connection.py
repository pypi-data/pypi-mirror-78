"""

Connect to an OmniSci database.
"""
from collections import namedtuple
import base64
from sqlalchemy.engine.url import make_url
from thrift.protocol import TBinaryProtocol, TJSONProtocol
from thrift.transport import TSocket, TSSLSocket, THttpClient, TTransport
from thrift.transport.TSocket import TTransportException
from omnisci.thrift.OmniSci import Client
from omnisci.thrift.ttypes import TOmniSciException

from .cursor import Cursor
from .exceptions import _translate_exception, OperationalError

from ._parsers import _extract_column_details

from ._loaders import _build_input_rows
from ._transforms import change_dashboard_sources
from ._samlutils import get_saml_response

from packaging.version import Version


ConnectionInfo = namedtuple(
    "ConnectionInfo",
    [
        'user',
        'password',
        'host',
        'port',
        'dbname',
        'protocol',
        'bin_cert_validate',
        'bin_ca_certs',
    ],
)


def connect(
    uri=None,
    user=None,
    password=None,
    host=None,
    port=6274,
    dbname=None,
    protocol='binary',
    sessionid=None,
    bin_cert_validate=None,
    bin_ca_certs=None,
    idpurl=None,
    idpformusernamefield='username',
    idpformpasswordfield='password',
    idpsslverify=True,
):
    """
    Create a new Connection.

    Parameters
    ----------
    uri: str
    user: str
    password: str
    host: str
    port: int
    dbname: str
    protocol: {'binary', 'http', 'https'}
    sessionid: str
    bin_cert_validate: bool, optional, binary encrypted connection only
        Whether to continue if there is any certificate error
    bin_ca_certs: str, optional, binary encrypted connection only
        Path to the CA certificate file
    idpurl : str
        EXPERIMENTAL Enable SAML authentication by providing
        the logon page of the SAML Identity Provider.
    idpformusernamefield: str
        The HTML form ID for the username, defaults to 'username'.
    idpformpasswordfield: str
        The HTML form ID for the password, defaults to 'password'.
    idpsslverify: str
        Enable / disable certificate checking, defaults to True.

    Returns
    -------
    conn: Connection

    Examples
    --------
    You can either pass a string ``uri``, all the individual components,
    or an existing sessionid excluding user, password, and database

    >>> connect('mapd://admin:HyperInteractive@localhost:6274/omnisci?'
    ...         'protocol=binary')
    Connection(mapd://mapd:***@localhost:6274/mapd?protocol=binary)

    >>> connect(user='admin', password='HyperInteractive', host='localhost',
    ...         port=6274, dbname='omnisci')

    >>> connect(user='admin', password='HyperInteractive', host='localhost',
    ...         port=443, idpurl='https://sso.localhost/logon',
                protocol='https')

    >>> connect(sessionid='XihlkjhdasfsadSDoasdllMweieisdpo', host='localhost',
    ...         port=6273, protocol='http')

    """
    return Connection(
        uri=uri,
        user=user,
        password=password,
        host=host,
        port=port,
        dbname=dbname,
        protocol=protocol,
        sessionid=sessionid,
        bin_cert_validate=bin_cert_validate,
        bin_ca_certs=bin_ca_certs,
        idpurl=idpurl,
        idpformusernamefield=idpformusernamefield,
        idpformpasswordfield=idpformpasswordfield,
        idpsslverify=idpsslverify,
    )


def _parse_uri(uri):
    """
    Parse connection string

    Parameters
    ----------
    uri: str
        a URI containing connection information

    Returns
    -------
    info: ConnectionInfo

    Notes
    ------
    The URI may include information on

    - user
    - password
    - host
    - port
    - dbname
    - protocol
    - bin_cert_validate
    - bin_ca_certs
    """
    url = make_url(uri)
    user = url.username
    password = url.password
    host = url.host
    port = url.port
    dbname = url.database
    protocol = url.query.get('protocol', 'binary')
    bin_cert_validate = url.query.get('bin_cert_validate', None)
    bin_ca_certs = url.query.get('bin_ca_certs', None)

    return ConnectionInfo(
        user,
        password,
        host,
        port,
        dbname,
        protocol,
        bin_cert_validate,
        bin_ca_certs,
    )


class Connection:
    """Connect to your OmniSci database."""

    def __init__(
        self,
        uri=None,
        user=None,
        password=None,
        host=None,
        port=6274,
        dbname=None,
        protocol='binary',
        sessionid=None,
        bin_cert_validate=None,
        bin_ca_certs=None,
        idpurl=None,
        idpformusernamefield='username',
        idpformpasswordfield='password',
        idpsslverify=True,
    ):

        self.sessionid = None
        self._closed = 0
        if sessionid is not None:
            if any([user, password, uri, dbname, idpurl]):
                raise TypeError(
                    "Cannot specify sessionid with user, password,"
                    " dbname, uri, or idpurl"
                )
        if uri is not None:
            if not all(
                [
                    user is None,
                    password is None,
                    host is None,
                    port == 6274,
                    dbname is None,
                    protocol == 'binary',
                    bin_cert_validate is None,
                    bin_ca_certs is None,
                    idpurl is None,
                ]
            ):
                raise TypeError("Cannot specify both URI and other arguments")
            (
                user,
                password,
                host,
                port,
                dbname,
                protocol,
                bin_cert_validate,
                bin_ca_certs,
            ) = _parse_uri(uri)
        if host is None:
            raise TypeError("`host` parameter is required.")
        if protocol != 'binary' and not all(
            [bin_cert_validate is None, bin_ca_certs is None]
        ):
            raise TypeError(
                "Cannot specify bin_cert_validate or bin_ca_certs,"
                " without binary protocol"
            )
        if protocol in ("http", "https"):
            if not host.startswith(protocol):
                # the THttpClient expects http[s]://localhost
                host = '{0}://{1}'.format(protocol, host)
            transport = THttpClient.THttpClient("{}:{}".format(host, port))
            proto = TJSONProtocol.TJSONProtocol(transport)
            socket = None
        elif protocol == "binary":
            if any([bin_cert_validate is not None, bin_ca_certs]):
                socket = TSSLSocket.TSSLSocket(
                    host,
                    port,
                    validate=(bin_cert_validate),
                    ca_certs=bin_ca_certs,
                )
            else:
                socket = TSocket.TSocket(host, port)
            transport = TTransport.TBufferedTransport(socket)
            proto = TBinaryProtocol.TBinaryProtocolAccelerated(transport)
        else:
            raise ValueError(
                "`protocol` should be one of"
                " ['http', 'https', 'binary'],"
                " got {} instead".format(protocol),
            )
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._dbname = dbname
        self._transport = transport
        self._protocol = protocol
        self._socket = socket
        self._tdf = None
        self._rbc = None
        try:
            self._transport.open()
        except TTransportException as e:
            if e.NOT_OPEN:
                err = OperationalError("Could not connect to database")
                raise err from e
            else:
                raise
        self._client = Client(proto)
        try:
            # If a sessionid was passed, we should validate it
            if sessionid:
                self._session = sessionid
                self.get_tables()
                self.sessionid = sessionid
            else:
                if idpurl:
                    self._user = ''
                    self._password = get_saml_response(
                        username=user,
                        password=password,
                        idpurl=idpurl,
                        userformfield=idpformusernamefield,
                        passwordformfield=idpformpasswordfield,
                        sslverify=idpsslverify,
                    )
                    self._dbname = ''
                    self._idpsslverify = idpsslverify
                    user = self._user
                    password = self._password
                    dbname = self._dbname

                self._session = self._client.connect(user, password, dbname)
        except TOmniSciException as e:
            raise _translate_exception(e) from e
        except TTransportException:
            raise ValueError(
                f"Connection failed with port {port} and "
                f"protocol '{protocol}'. Try port 6274 for "
                "protocol == binary or 6273, 6278 or 443 for "
                "http[s]"
            )

        # if OmniSci version <4.6, raise RuntimeError, as data import can be
        # incorrect for columnar date loads
        # Caused by https://github.com/omnisci/pymapd/pull/188
        semver = self._client.get_version()
        if Version(semver.split("-")[0]) < Version("4.6"):
            raise RuntimeError(
                f"Version {semver} of OmniSci detected. "
                "Please use pymapd <0.11. See release notes "
                "for more details."
            )

    def __repr__(self):
        tpl = (
            'Connection(omnisci://{user}:***@{host}:{port}/{dbname}?'
            'protocol={protocol})'
        )
        return tpl.format(
            user=self._user,
            host=self._host,
            port=self._port,
            dbname=self._dbname,
            protocol=self._protocol,
        )

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def closed(self):
        return self._closed

    def close(self):
        """Disconnect from the database unless created with sessionid"""
        if not self.sessionid and not self._closed:
            try:
                self._client.disconnect(self._session)
            except (TOmniSciException, AttributeError, TypeError):
                pass
        self._closed = 1
        self._rbc = None

    def commit(self):
        """This is a noop, as OmniSci does not provide transactions.

        Implemented to comply with the DBI specification.
        """
        return None

    def execute(self, operation, parameters=None):
        """Execute a SQL statement

        Parameters
        ----------
        operation: str
            A SQL statement to exucute

        Returns
        -------
        c: Cursor
        """
        c = Cursor(self)
        return c.execute(operation, parameters=parameters)

    def cursor(self):
        """Create a new :class:`Cursor` object attached to this connection."""
        return Cursor(self)

    # --------------------------------------------------------------------------
    # Convenience methods
    # --------------------------------------------------------------------------
    def get_tables(self):
        """List all the tables in the database

        Examples
        --------
        >>> con.get_tables()
        ['flights_2008_10k', 'stocks']
        """
        return self._client.get_tables(self._session)

    def get_table_details(self, table_name):
        """Get the column names and data types associated with a table.

        Parameters
        ----------
        table_name: str

        Returns
        -------
        details: List[tuples]

        Examples
        --------
        >>> con.get_table_details('stocks')
        [ColumnDetails(name='date_', type='STR', nullable=True, precision=0,
                       scale=0, comp_param=32, encoding='DICT'),
         ColumnDetails(name='trans', type='STR', nullable=True, precision=0,
                       scale=0, comp_param=32, encoding='DICT'),
         ...
        ]
        """
        details = self._client.get_table_details(self._session, table_name)
        return _extract_column_details(details.row_desc)

    def load_table_rowwise(self, table_name, data):
        """Load data into a table row-wise

        Parameters
        ----------
        table_name: str
        data: Iterable of tuples
            Each element of `data` should be a row to be inserted

        See Also
        --------
        load_table
        load_table_arrow
        load_table_columnar

        Examples
        --------
        >>> data = [(1, 'a'), (2, 'b'), (3, 'c')]
        >>> con.load_table('bar', data)
        """
        input_data = _build_input_rows(data)
        self._client.load_table(self._session, table_name, input_data)

    def render_vega(self, vega, compression_level=1):
        """Render vega data on the database backend,
        returning the image as a PNG.

        Parameters
        ----------

        vega: dict
            The vega specification to render.
        compression_level: int
            The level of compression for the rendered PNG. Ranges from
            0 (low compression, faster) to 9 (high compression, slower).
        """
        result = self._client.render_vega(
            self._session,
            widget_id=None,
            vega_json=vega,
            compression_level=compression_level,
            nonce=None,
        )
        rendered_vega = RenderedVega(result)
        return rendered_vega

    def get_dashboard(self, dashboard_id):
        """Return the dashboard object of a specific dashboard

        Examples
        --------
        >>> con.get_dashboard(123)
        """
        dashboard = self._client.get_dashboard(
            session=self._session, dashboard_id=dashboard_id
        )
        return dashboard

    def get_dashboards(self):
        """List all the dashboards in the database

        Examples
        --------
        >>> con.get_dashboards()
        """
        dashboards = self._client.get_dashboards(session=self._session)
        return dashboards

    def duplicate_dashboard(
        self, dashboard_id, new_name=None, source_remap=None
    ):
        """
        Duplicate an existing dashboard, returning the new dashboard id.

        Parameters
        ----------

        dashboard_id: int
            The id of the dashboard to duplicate
        new_name: str
            The name for the new dashboard
        source_remap: dict
            EXPERIMENTAL
            A dictionary remapping table names. The old table name(s)
            should be keys of the dict, with each value being another
            dict with a 'name' key holding the new table value. This
            structure can be used later to support changing column
            names.

        Examples
        --------
        >>> source_remap = {'oldtablename1': {'name': 'newtablename1'}, \
'oldtablename2': {'name': 'newtablename2'}}
        >>> newdash = con.duplicate_dashboard(12345, "new dash", source_remap)
        """
        source_remap = source_remap or {}
        d = self._client.get_dashboard(
            session=self._session, dashboard_id=dashboard_id
        )

        newdashname = new_name or '{0} (Copy)'.format(d.dashboard_name)
        d = change_dashboard_sources(d, source_remap) if source_remap else d

        new_dashboard_id = self._client.create_dashboard(
            session=self._session,
            dashboard_name=newdashname,
            dashboard_state=d.dashboard_state,
            image_hash='',
            dashboard_metadata=d.dashboard_metadata,
        )

        return new_dashboard_id

    def __call__(self, *args, **kwargs):
        """Runtime UDF decorator.

        The connection object can be applied to a Python function as
        decorator that will add the function to bending registration
        list.
        """
        try:
            from rbc.omniscidb import RemoteOmnisci
        except ImportError:
            raise ImportError("The 'rbc' package is required for `__call__`")
        if self._rbc is None:
            self._rbc = RemoteOmnisci(
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port,
                dbname=self._dbname,
            )
            self._rbc._session_id = self.sessionid
        return self._rbc(*args, **kwargs)

    def register_runtime_udfs(self):
        """Register any bending Runtime UDF functions in OmniSci server.

        If no Runtime UDFs have been defined, the call to this method
        is noop.
        """
        if self._rbc is not None:
            self._rbc.register()


class RenderedVega:
    def __init__(self, render_result):
        self._render_result = render_result
        self.image_data = base64.b64encode(render_result.image).decode()

    def _repr_mimebundle_(self, include=None, exclude=None):
        return {
            'image/png': self.image_data,
            'text/html': (
                '<img src="data:image/png;base64,{}" '
                'alt="OmniSci Vega">'.format(self.image_data)
            ),
        }
