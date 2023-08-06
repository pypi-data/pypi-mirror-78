from typing import Dict, Any, List, IO, Optional
from .utils.export_utils import ExportCSV, ExportJSON, ExportTable
from datetime import datetime


class Service:
    def __init__(
        self, service, credentials, body: Dict[Any, Any] = {}, data: Dict[Any, Any] = {}
    ) -> None:
        self.service = service
        self.credentials = credentials
        self.body = body
        self.data = data

    def update_body(self, body) -> None:
        """
        Updates the body, that we are going to use in the query
        """

        self.body.update({k: v for k, v in body.items()})

    def query(self, url: str) -> None:
        """
        Just a simplified wrapper to the searchanalytics
        """

        self.data.update(
            self.service.searchanalytics().query(siteUrl=url, body=self.body).execute()
        )

    def export(self, export_type: Optional[str]) -> None:
        if export_type == "csv":
            export_data = ExportCSV(self.data)
            export_data.export_to_csv()

        if export_type == "json":
            data = ExportJSON(self.data)
            data.export_to_json()

        if not export_type or export_type == "table":
            data = ExportTable(self.data)
            data.export_to_table()

    # TODO DELETE
    def show_data(self):
        return self.data

    # TODO DELETE
    def show_body(self):
        return self.body
