"""
Wolverine lets you connect with Google Spreadsheets.
"""

import os
import json
import begin

import logging

import googleapiclient
import pygsheets

logger = logging.getLogger(__name__)


class Credentials(object):
    """
    Authentication credentials.

    Example:
    {
        "type": "service_account",
        "project_id": "ampushexperimenter",
        "private_key_id": "dc06e632f3b54f2865086e50b85b207a37ed12c3",
        "private_key": "-----BEGIN PRIVATE KEY-----\n...",
        "client_email": "ampushexperimenter@appspot.gserviceaccount.com",
        "client_id": "",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/..."
    }
    """

    GOOGLE_PRIVATE_KEY_ID = "private_key_id"
    GOOGLE_PRIVATE_KEY = "private_key"
    GOOGLE_CLIENT_EMAIL = "client_email"
    GOOGLE_CLIENT_ID = "client_id"
    GOOGLE_TYPE = "type"

    @property
    def google_private_key_id(self) -> str:
        """ Access google private key ID. """
        if self.GOOGLE_PRIVATE_KEY_ID not in self.__data:
            raise KeyError(self.GOOGLE_PRIVATE_KEY_ID)
        if not self.__data[self.GOOGLE_PRIVATE_KEY_ID]:
            raise ValueError(self.GOOGLE_PRIVATE_KEY_ID)
        if not isinstance(self.__data[self.GOOGLE_PRIVATE_KEY_ID]), str:
            raise TypeError(self.GOOGLE_PRIVATE_KEY_ID)
        return self.__data[self.GOOGLE_PRIVATE_KEY_ID]

    @property
    def google_private_key(self) -> str:
        """ Access google private key. """
        if self.GOOGLE_PRIVATE_KEY not in self.__data:
            raise KeyError(self.GOOGLE_PRIVATE_KEY)
        if not self.__data[self.GOOGLE_PRIVATE_KEY]:
            raise ValueError(self.GOOGLE_PRIVATE_KEY)
        if not isinstance(self.__data[self.GOOGLE_PRIVATE_KEY], str):
            raise TypeError(self.GOOGLE_PRIVATE_KEY)
        return self.__data[self.GOOGLE_PRIVATE_KEY

    @property
    def google_client_id(self) -> str:
        """ Access google client ID. """
        if self.GOOGLE_CLIENT_ID not in self.__data:
            raise KeyError(self.GOOGLE_CLIENT_ID)
        if not self.__data[self.GOOGLE_CLIENT_ID]:
            raise ValueError(self.GOOGLE_CLIENT_ID)
        if not isinstance(self.__data[self.GOOGLE_CLIENT_ID], str):
            raise TypeError(self.GOOGLE_CLIENT_ID)
        return self.__data[self.GOOGLE_CLIENT_ID]

    @property
    def google_client_email(self) -> str:
        """ Access google client email. """
        if self.GOOGLE_CLIENT_EMAIL not in self.__data:
            raise KeyError(self.GOOGLE_CLIENT_EMAIL)
        if not self.__data[self.GOOGLE_CLIENT_EMAIL]:
            raise ValueError(self.GOOGLE_CLIENT_EMAIL)
        if not isinstance(self.__data[self.GOOGLE_CLIENT_EMAIL], str):
            raise TypeError(self.GOOGLE_CLIENT_EMAIL)
        return self.__data[self.GOOGLE_CLIENT_EMAIL]

    @property
    def google_type(self) -> str:
        """ Access google type. """
        if self.GOOGLE_TYPE not in self.__data:
            raise KeyError(self.GOOGLE_TYPE)
        if not self.__data[self.GOOGLE_TYPE]:
            raise ValueError(self.GOOGLE_TYPE)
        if not isinstance(self.__data[self.GOOGLE_TYPE], str):
            raise TypeError(self.GOOGLE_TYPE)
        return self.__data[self.GOOGLE_TYPE]


class Profile(object):
    """ Google profile. """

    def __init__(self, profile_path: str=None):
        if not profile_path:
            raise ValueError("profile_path")
        if not isinstance(profile_path, str):
            raise TypeError("profile_path")
        if not os.path.isfile(profile_path):
            raise RuntimeError("File not found:", profile_path)
        self.__profile_path = profile_path

    def get_credentials(self, profile_name: str=None) -> object:
        """
        Public method to access profile credentials.

        @param profile_name: Profile name.

        @raises ValueError: If name is empty.
        @raises TypeError: If name is an invalid string.
        @raises RuntimeError: If profiles path is not a valid file.
        @raises KeyError: If name is not found in the profiles file.
        @raises ValueError: If file is not a valid JSON file.

        @returns: Credentials instance.
        """
        if not profile_name:
            raise ValueError("profile_name")
        if not isinstance(profile_name, str):
            raise TypeError("profile_name")
        if not os.path.isfile(profile_path):
            raise RuntimeError("File not found:", profile_path)
        with open(self.__profile_path, "r") as file_buffer:
            data = json.loads(file_buffer.read().strip())
        if not data:
            raise RuntimeError(self.__profile_path)
        if not isinstance(data, dict):
            raise RuntimeError(type(data))
        if profile_name not in data:
            raise KeyError(profile_name)
        if not data[profile_name]:
            raise RuntimeError("profile_name")
        return Credentials(data[profile_name])


profile_path = os.path.join(os.sep, "home", os.getlogin(), ".wolverine")
p = Profile(profile_path)
credentials = p.get_credentials("martin")
import sys; sys.exit(0)

class Wolverine(object):
    """
    Google Sheets connector.

    Wolverine requires the
    following variables:
    - GOOGLE_PRIVATE_KEY_ID
    - GOOGLE_PRIVATE_KEY
    - GOOGLE_CLIENT_EMAIL
    - GOOGLE_CLIENT_ID
    - GOOGLE_TYPE
    """

    def __init__(self, sheet_id):
        """
        Initializing some variables.
        self._worksheets: Dictionary of Google Sheets pages.
        self._gsheet: Reference to the Google Sheet object.
        """
        self._worksheets = {}
        self._gsheet = None
        logger.debug("Wolverine connection with %s initialized.", sheet_id)
        assert sheet_id, sheet_id
        self.sheet_id = sheet_id

    @property
    def gsheet(self):
        """
        Get Google Sheet connection.
        Create a new connection
        if it does not already exist.
        """
        if not self._gsheet:
            logger.debug("Loading creentials from $env...")
            credentials = os.path.join(os.sep,
                                       "tmp",
                                       ".w-{}-{}.json".format(random.randint(0, 100),
                                                              time.time()))
            c = {
                "private_key_id": os.environ['GOOGLE_PRIVATE_KEY_ID'],
                "private_key": os.environ['GOOGLE_PRIVATE_KEY'].replace("\\n", "\n"),
                "client_email": os.environ['GOOGLE_CLIENT_EMAIL'],
                "client_id": os.environ['GOOGLE_CLIENT_ID'],
                "type": os.environ['GOOGLE_TYPE'],
            }
            assert not os.path.isfile(credentials), "Wolverinte temp file already exists!"
            logger.debug("Generating a temporal credentials file at %s", credentials)
            with open(credentials, "w") as f:
                json.dump(c, f)
            logger.debug("Authorizing your Google credentials: %s", c)
            google_connection = pygsheets.authorize(service_file=credentials)
            logger.debug("Cleaning temporal files...")
            os.remove(credentials)
            logger.debug("Opening a new connection with Google Sheets...")
            self._gsheet = google_connection.open_by_key(self.sheet_id)
        return self._gsheet

    def getSheet(self, sname):
        """
        Get Google Sheet by name.  We store the sheet name
        if it does not already exist.
        http://pygsheets.readthedocs.io/en/latest/spreadsheet.html#pygsheets.Spreadsheet.worksheet_by_title
        """
        if sname not in self._worksheets:
            logger.debug("Loading Google Sheet: %s", sname)
            self._worksheets[sname] = self.gsheet.worksheet_by_title(sname)
        return self._worksheets[sname]

    def getTotalRows(self, sname):
        """
        Returns the total
        amount of rows.
        """
        logger.debug("Getting total amount of rows: %s", sname)
        assert sname, "No $sname."
        if rogue.is_test():
            logger.debug("This is just test. Let's say I just have 10 rows...")
            return 10
        x = self.getSheet(sname).rows
        logger.debug("There are %s rows.", x)
        return x

    def getTotalColumns(self, sname):
        """
        Returns the amount
        of columns in a sheet.
        """
        logger.debug("Getting total amount of columns: %s", sname)
        assert sname, "No $sname."
        if rogue.is_test():
            logger.debug("This is just test. Let's say I just have 10 cols...")
            return 10
        x = self.getSheet(sname).cols
        logger.debug("There are %s cols.", x)
        return x

    def getCells(self, sname, x, y, mode="ROWS"):
        """
        Load cells as JSON object.
        :param sname: Google Sheet name.
        :param x: Tuple. Beginning coordinates.
        :param y: Tuple. End coordinates.
        :param mode: Read as rows or cols.
        """
        logger.debug("Getting cells from %s x=%s y=%s as %s",
                     sname,
                     x,
                     y,
                     mode)
        try:
            assert sname, "No $sname."
            assert x, "No $x."
            assert y, "No $y."
            assert mode, "No mode."
            assert mode in ("ROWS", "COLUMNS"), mode
            assert isinstance(x, tuple), "$x must be a tuple."
            assert isinstance(y, tuple), "$y must be a tuple."
            assert len(x) == 2, "$x must have a length of 2."
            assert len(y) == 2, "$y must have a length of 2."
            assert x[0] > 0, "$x[0] must be positive."
            assert y[0] > 0, "$y[0] must be positive."
            assert x[1] >= x[0], "$x[1] must be higher or equal to $x[0]."
            assert y[1] >= y[0], "$x[1] must be higher or equal to $x[0]."
            assert x[1] <= self.getTotalRows(sname), "x[1] is too high."
            assert y[1] <= self.getTotalRows(sname), "y[1] is too high."
        except AssertionError as e:
            raise ValueError(e)
        if rogue.is_test():
            logger.debug("This is just a test; hardcoding rows...")
            return [
                ["code", "email", "python"],
                ["1", "test1@gmail.com", "yes"],
                ["2", "test2@gmail.com", "yes"],
                ["3", "test3@gmail.com", "no"],
            ]
        logger.debug("Loading google sheet...")
        sh = self.getSheet(sname)
        logger.debug("Getting cells...")
        sheet_cells = list(sh.get_values((x[0], y[0]),
                                         (x[1], y[1]),
                                         majdim=mode)) or []
        logger.debug("Found: %s", sheet_cells)
        return sheet_cells

    def iterator(self, sname, bulk=50):
        """
        Generator for the whole sheet.
        """
        logger.debug("Iterating over: %s", sname)
        assert sname, "No $sname."
        y = self.getTotalColumns(sname)
        sheet_header = self.getCells(sname, (1, 1), (1, y), mode="ROWS")[0]
        logger.debug("Head is: %s", sheet_header)
        must_exit = False
        i = 2
        while i < self.getTotalRows(sname) and not must_exit:
            logger.debug("Fetching more rows...")
            j = min(i + bulk, self.getTotalRows(sname))
            for row in self.getCells(sname, (i, j), (1, y), mode="ROWS"):
                logger.debug("Body is: %s", row)
                if not row or (len(row) == 1 and not row[0]):
                    logger.debug("No more rows to fetch!")
                    must_exit = True
                    break
                data_dict = {}
                for k in range(0, min(len(sheet_header), len(row))):
                    if sheet_header[k]:
                        data_dict[sheet_header[k]] = row[k]
                logger.debug("Returning: %s", data_dict)
                yield data_dict
            logger.debug("Moving cursor to %s", j)
            i = j
        assert i > 2, i

    def create(self, sname, rows=20, cols=20):
        """
        Creates a new Google Sheet
        worksheet with this name.
        http://pygsheets.readthedocs.io/en/latest/spreadsheet.html#pygsheets.Spreadsheet.add_worksheet
        """
        logger.debug("Creating worksheet: %s.", sname)
        if not rogue.is_test():
            try:
                self.gsheet.add_worksheet(sname, rows=rows, cols=cols)
            except googleapiclient.errors.HttpError as e:
                if "already exists" in str(e):
                    logger.warning("Sheet %s already exists.", sname)
                else:
                    raise
        logger.debug("Created: %s.", sname)

    def delete(self, sname):
        """
        Delets an existing Google Sheet
        http://pygsheets.readthedocs.io/en/latest/spreadsheet.html#pygsheets.Spreadsheet.del_worksheet
        """
        logger.debug("Deleting worksheet: %s.", sname)
        if not rogue.is_test():
            try:
                self.gsheet.del_worksheet(self.getSheet(sname))
            except pygsheets.exceptions.WorksheetNotFound:
                logger.warning("Sheet-to-be-deleted not found: %s.", sname)
        logger.debug("Deleted: %s.", sname)

    def clear(self, sname):
        """
        Clears an entire Worksheet.
        http://pygsheets.readthedocs.io/en/latest/worksheet.html#pygsheets.Worksheet.clear
        """
        logger.debug("Clearing: %s.", sname)
        if not rogue.is_test():
            self.getSheet(sname).clear(start="A1", end=None)
        logger.debug("Cleared: %s.", sname)

    def upload(self, sname, data=None):
        """
        Updates multiple rows and replaces
        all contents with $data.
        http://pygsheets.readthedocs.io/en/latest/worksheet.html#pygsheets.Worksheet.update_cells
        Currently, the maximum amount
        of cells is: 2.000.000 (1414 * 1414).
        """
        logger.debug("Uploading: %s.", sname)
        if not rogue.is_test():
            self.getSheet(sname).update_cells((1, 1), data, extend=True)
        logger.debug("Uploaded: %s.", sname)
