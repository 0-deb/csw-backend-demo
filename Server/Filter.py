from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status

from rest_framework.filters import SearchFilter


class Filter:
	def SearchAndFilter(self, Query_Set, FilterFields, SearchFields):
		self.queryset = Query_Set
		self.filter_backends = [DjangoFilterBackend, SearchFilter]
		self.filter_fields = FilterFields
		self.search_fields = SearchFields
		
		return self.filter_queryset(self.queryset)


class UpdateFilter:
	@staticmethod
	def BlacklistFilter(requestData, blackList):
		filteredData = requestData.copy()

		for entry in requestData:
			if entry in blackList:
				filteredData.pop(entry)

		return filteredData