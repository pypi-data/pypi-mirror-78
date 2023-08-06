from typing import Dict, Any, List, IO, Optional, Union
from .utils.export_utils import Export
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

    def sites(self, url: Union[None, str] = None):
        """
        List all the web sites associated with the account.

        Info: https://developers.google.com/resources/api-libraries/documentation/webmasters/v3/python/latest/webmasters_v3.sites.html
        """

        if url:
            self.data.update(self.service.sites().get(siteUrl=url).execute())

        else:
            self.data.update(self.service.sites().list().execute())

    def sitemaps(self, url: str, feedpath: Union[None, str] = None):
        """
        Lists the sitemaps-entries submitted for the given site.

        Info: https://developers.google.com/resources/api-libraries/documentation/webmasters/v3/python/latest/webmasters_v3.sitemaps.html
        """

        if url and feedpath:
            self.data.update(
                self.service.sitemaps().get(siteUrl=url, feedpath=feedpath).execute()
            )

        elif url:
            self.data.update(self.service.sitemaps().list(siteUrl=url).execute())

    def export(
        self,
        export_type: Union[None, str] = None,
        url: Union[None, str] = None,
        command: Union[None, str] = None,
    ) -> None:
        """
        Specify the export type.
        """

        if export_type == "csv":
            export_data = Export(self.data)
            export_data.export_to_csv(
                filename=self._create_filename(
                    url=url, command=command, filetype=export_type
                )
            )

        if export_type == "json":
            data = Export(self.data)
            data.export_to_json(
                filename=self._create_filename(
                    url=url, command=command, filetype=export_type
                )
            )

        if export_type == "excel":
            export_data = Export(self.data)
            export_data.export_to_excel(
                filename=self._create_filename(
                    url=url, command=command, filetype=export_type
                )
            )

        if export_type == "tsv":
            export_data = Export(self.data)
            export_data.export_to_tsv(
                filename=self._create_filename(url=url, command=command, filetype="tsv")
            )

        if not export_type or export_type == "table":
            export_data = Export(self.data)
            export_data.export_to_table()

    def _create_filename(self, url: str, command: str, filetype: str) -> str:
        """
        Creates a file name from timestamp, url and command.
        """

        from datetime import datetime

        def clean_url(url: str) -> str:
            for t in (
                ("https", ""),
                ("http", ""),
                (":", ""),
                ("sc-domain", ""),
                ("//", ""),
                ("/", "-"),
                ("--", "-"),
                (".", "-"),
                (",", "-"),
            ):
                url = url.lower().replace(*t)

            return url

        return "-".join(
            [
                clean_url(url) or "",
                command,
                datetime.now().strftime("%d-%B-%Y-%H-%M") + f".{filetype}",
            ]
        )
