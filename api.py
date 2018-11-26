import json
import requests
from .api_paths import API

# Successful API response
SUCCESS = 200

def _get_api_response(url):
    """Gets the response from GET request
    Converts GET request from JSON string to dict
    
    Arguments:
        url {str} -- Target API url

    Raises:
        APIAccessError -- Error occured in accessing the API

    Returns:
        {dict} -- API response
    """
    resp = requests.get(url)
    if resp.status_code != SUCCESS:
        raise APIAccessError("Error: {}".format(resp.text))
    
    return json.loads(resp.text)


class APIKeyNotSet(Exception):
    """Exception for when the API key is not set for the client
    """
    pass

class APIAccessError(Exception):
    """Exception for when API response is not SUCCESS
    """
    pass



class WTDApi(object):
    """Class for handling access to the WorldTradeData API
    
    Arguments:
        api_key {str} -- API key for accessing the service
    """
    def __init__(self, api_key=None):
        if not api_key:
            raise APIKeyNotSet(
                """
                API Key not set for this client.\n
                Obtain one from https://worldtradingdata.com/
                """
            )    
        self.api_key = api_key


    def set_api_key(self, api_key):
        """Sets the API key for accessing the service
        
        Arguments:
            api_key {str} -- Sets the API key for the client
        """
        self.api_key = api_key


    def _build_misc_string(self, **kwargs):
        """Builds the API URL string with arguments

        Arguments:
            kwargs {variable} -- Variable keyword args to add to the string

        Returns:
            {str} -- URL string
        """
        misc = "?"
        for key, value in kwargs.items():
            if value == None:
                continue
            key = str(key) + "="
            if isinstance(value, list):
                key += (",".join(str(x) for x in value) + "&")
            else:
                key += (str(value) + "&")
            misc += key
        misc += ("api_token=" + self.api_key)

        return misc
    

    def stocks(self, symbols, sort_by=None, sort_order=None):
        """Accesses the Stock API
        Symbols can be str for single symbol or list for numerous symbols
        
        Arguments:
            symbols {str/list} -- Str for single, list for multiple stocks
        
        Keyword Arguments:
            sort_by {str} -- How to sort data (symbol, name, list_order) (default: {None})
            sort_order {str} -- Order the sort (asc, desc) (default: {None})
        """
        url = API["stock"] + self._build_misc_string(
            symbol=symbols,
            sort_by=sort_by,
            sort_order=sort_order
        )

        return _get_api_response(url)


    def mutual_fund(self, symbols, sort_order=None, sort_by=None):
        """Access the Mutual Fund API
        Symbols can be str for single symbol or list for numerous symbols

        Arguments:
            symbols {str/list} -- Str for single, list for multiple funds
        
        Keyword Arguments:
            sort_order {str} -- How to sort data (symbol, name, list_order) (default: {None})
            sort_by {str} -- Order the sort (asc, desc) (default: {None})
        """
        url = API["mutual_fund"] + self._build_misc_string(
            symbol=symbols,
            sort_order=sort_order,
            sort_by=sort_by
        )

        return _get_api_response(url)


    def intraday(self, symbol, interval=1, range=7, sort=None, formatted=None):
        """Accesses the Intraday API
        
        Arguments:
            symbol {str} -- Stock/index/mutual fund symbol
        
        Keyword Arguments:
            interval {int} -- Minutes between the data (default: {1})
            range {int} -- Number of days for the data (default: {7})
            sort {str} -- Sort order of values (asc, desc) (default: {None})
            formatted {bool} -- Alter JSON data format (true/false) (default: {None})
        """
        url = API["intraday"] + self._build_misc_string(
            symbol=symbol,
            interval=interval,
            range=range,
            sort=sort,
            formatted=formatted
        )

        return _get_api_response(url)


    def historic_data(self, symbol, date_from=None, date_to=None, sort=None, formatted=None):
        """Accesses the Historic Market Data API
        
        Arguments:
            symbol {str} -- Stock/index/mutual fund symbol
        
        Keyword Arguments:
            date_from {str} -- Date to start data retrieval from (default: {None})
            date_to {str} -- Date to end data retrieval (default: {None})
            sort {str} -- Sort by date (newest, oldest, asc, desc) (default: {None})
            formatted {bool} -- Alter JSON data format (default: {None})
        """
        url = API["history"] + self._build_misc_string(
            symbol=symbol,
            date_from=date_from,
            date_to=date_to,
            sort=sort,
            formatted=formatted
        )
        
        return _get_api_response(url)


    def historic_multi_single_day(self, symbol, date, sort=None, formatted=None):
        """Accesses the Multi Single Day History API
        Symbols can be str for single symbol or list for multiple symbols
        
        Arguments:
            symbol {str/list -- Str for single, list for multiple stocks/index/mutual fund
            date {str} -- Date to retrieve the data for
        
        Keyword Arguments:
            sort {str} -- Sort order by name (asc, desc) (default: {None})
            formatted {bool} -- Alter JSON data format (default: {None})
        """
        url = API["history_msd"] + self._build_misc_string(
            symbol=symbol,
            date=date,
            sort=sort,
            formatted=formatted
        )

        return _get_api_response(url)


    def forex(self, base):
        """Accesses the Forex API
        Obtains all combinations for specified currency base
        
        Arguments:
            base {str} -- Base currency
        """
        url = API["forex"] + self._build_misc_string(base=base)

        return _get_api_response(url)


    def forex_historic(self, base, convert_to, sort=None, formatted=None):
        """Accesses the Forex Historic Data API
        
        Arguments:
            base {str} -- Base currency
            convert_to {str} -- Currency to convert to
        
        Keyword Arguments:
            sort {str} -- Sort by newest or oldest (newest, oldest) (default: {None})
            formatted {bool} -- Alter JSON data format (default: {None})
        """
        url = API["forex_history"] + self._build_misc_string(
            base=base,
            convert_to=convert_to,
            sort=sort,
            formatted=formatted
        )

        return _get_api_response(url)


    def forex_historic_single_day(self, base, date, formatted=None):
        """Accesses the Forex Single Day History API
        
        Arguments:
            base {str} -- Base currency
            date {str} -- Date to obtain data for
        
        Keyword Arguments:
            formatted {str} -- Alter JSON data format (default: {None})
        """
        url = API["forex_single_day"] + self._build_misc_string(
            base=base,
            date=date,
            formatted=formatted
        )

        return _get_api_response(url)


    def search(self, search_term, search_by=None, stock_exchange=None, currency=None, limit=None, page=None, sort_by=None, sort_order=None):
        """Accesses the Stock Search API
        
        Arguments:
            search_term {str} -- Search term to find stocks for
        
        Keyword Arguments:
            search_by {str} -- Search by symbol, name, or both (default: {None})
            stock_exchange {list} -- Filter data by list of stock exchanges (default: {None})
            currency {list} -- Filter data by list of currencies (default: {None})
            limit {int} -- Limit number of results (default: {None})
            page {int} -- Value of page to see values for (default: {None})
            sort_by {str} -- Sort by column (symbol, name, currency, stock_exchange_long, stock_exchange_short) (default: {None})
            sort_order {str} -- Sort order of Sort By column (asc, desc) (default: {None})
        """
        url = API["search"] + self._build_misc_string(
            search_term=search_term,
            search_by=search_by,
            stock_exchange=stock_exchange,
            currency=currency,
            limit=limit,
            page=page,
            sort_by=sort_by,
            sort_order=sort_order
        )

        return _get_api_response(url)
