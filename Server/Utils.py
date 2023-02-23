from enum import Enum
from datetime import datetime, time


class DateTimeParser:
    
    DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    TIME_FORMAT = "%H:%M:%S"

    @staticmethod
    def EncodeDatetime(timeObject):
        return datetime.strftime(timeObject, DateTimeParser.DATETIME_FORMAT)

    @staticmethod
    def DecodeDatetime(timeString):
        return datetime.strptime(timeString, DateTimeParser.DATETIME_FORMAT)

    @staticmethod
    def EncodeTime(timeObject):
        return time.strftime(timeObject, DateTimeParser.TIME_FORMAT)

    @staticmethod
    def DecodeTime(timeString):
        return datetime.strptime(timeString, DateTimeParser.TIME_FORMAT).time()


class EnumChoices(Enum):
	
	@classmethod
	def choices(cls):
		return [(key.name, key.value) for key in cls]

	@classmethod
	def fetch(cls, keyword):
		for key in cls:
			if key.name == keyword:
				return key.value