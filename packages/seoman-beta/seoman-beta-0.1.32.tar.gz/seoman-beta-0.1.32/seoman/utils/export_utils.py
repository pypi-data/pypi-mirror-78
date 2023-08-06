from typing import Optional, Dict, Any, Union, List

import json
import csv
from collections import OrderedDict
from pytablewriter import (
    UnicodeTableWriter,
    ExcelXlsxTableWriter,
    TsvTableWriter,
)


class Export:
    def __init__(
        self, data: Dict[Any, Any] = {}, keys: List[Any] = [], values: List[Any] = []
    ) -> None:
        self.data = data
        self.keys = keys
        self.values = values

    def _flatten(self, data: Dict[Any, Any], sep="_") -> OrderedDict:

        obj = OrderedDict()

        def recurse(temp, parent_key=""):
            """
            Recursive iterator to reach everything inside data.
            """

            if isinstance(temp, list):
                for i in range(len(temp)):
                    recurse(
                        temp[i], parent_key + sep + str(i) if parent_key else str(i)
                    )
            elif isinstance(temp, dict):
                for key, value in temp.items():
                    recurse(value, parent_key + sep + key if parent_key else key)
            else:
                obj[parent_key] = temp

        recurse(data)
        return obj

    def _split_to_kv(self, data: Dict[Any, Any]) -> None:
        """
        Split data to key value pair.
        """

        if data.keys().__contains__("path") or data.keys().__contains__(
            "permissionLevel"
        ):
            """
            If data contains path, it must be a sitemap instance.
            If data contains permissionLevel, it must be sites instance.
            """

            for key, value in data.items():
                if key.__contains__("_"):
                    key = key.split("_")
                    key = " ".join([key[0], key[2], key[1]])

                if key not in self.keys:
                    self.keys.append(key)

                self.values.append(value)

        else:
            for key, value in data.items():
                key = key.split("_")

                if key[0] == "responseAggregationType":
                    break

                if key[2] == "keys" and key[3] != "0":
                    # If there are multiple keys, add key number to keys eg. [keys1, keys2]
                    key = key[2] + key[3]

                key = key[2] if isinstance(key, list) else key

                if key not in self.keys:
                    self.keys.append(key)

                self.values.append(value)

    def __preprocess(self) -> None:
        """
        Preprocess the data.
        """

        self._split_to_kv(self._flatten(self.data))

    def export_to_table(self) -> None:
        """
        Export in Unicode Table format.
        """

        self.__preprocess()

        sub = len(self.keys)

        writer = UnicodeTableWriter()

        writer.table_name = "Analytics"
        writer.margin = 2

        writer.headers = self.keys
        writer.value_matrix = [
            self.values[ctr : ctr + sub] for ctr in range(0, len(self.values), sub)
        ]

        writer.write_table()

    def export_to_json(self, filename: str) -> None:
        """
        Export in JSON format.
        """

        with open(filename, "w") as file:
            json.dump(self.data, file, indent=4)

        print(f"Analytics successfully created in JSON format ✅")

    def export_to_csv(self, filename: str) -> None:
        """
        Export in CSV format.
        """

        self.__preprocess()

        sub = len(self.keys)

        from csv import writer

        with open(filename, "w") as file:
            csv_writer = writer(file)
            csv_writer.writerow(self.keys)
            for ctr in range(0, len(self.values), sub):
                csv_writer.writerow(self.values[ctr : ctr + sub])

        print(f"Analytics successfully created in CSV format ✅")

    def export_to_excel(self, filename: str) -> None:
        """
        Export in XLSX format.
        """

        self.__preprocess()

        sub = len(self.keys)

        writer = ExcelXlsxTableWriter()

        writer.table_name = "Analytics"

        writer.headers = self.keys
        writer.value_matrix = [
            self.values[ctr : ctr + sub] for ctr in range(0, len(self.values), sub)
        ]

        writer.dump(filename)

        print(f"Analytics successfully created in XLSX format ✅")

    def export_to_tsv(self, filename: str) -> None:
        """
        Export in TSV format.
        """

        self.__preprocess()

        sub = len(self.keys)

        writer = TsvTableWriter()

        writer.headers = self.keys
        writer.value_matrix = [
            self.values[ctr : ctr + sub] for ctr in range(0, len(self.values), sub)
        ]

        writer.dump(filename)
