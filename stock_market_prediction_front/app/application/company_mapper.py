# Author: Piotr Cieślak

class CompanyMapper:
    """This class provides methods for mapping company ticker to company name."""

    @staticmethod
    def map_name_to_ticker(name_enum):
        """Maps company ticker to company name."""

        dictionary = {
            "apple": "AAPL",
            "google": "GOOG",
            "nvidia": "NVDA",
            "amazon": "AMZN",
            "microsoft": "MSFT"
        }

        return dictionary.get(name_enum, "NULL")
