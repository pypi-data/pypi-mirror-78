from typing import Optional, Dict, Any, Union, List

import json
import csv
from collections import OrderedDict
from pytablewriter import UnicodeTableWriter, CsvTableWriter, ExcelXlsxTableWriter


# TODO Simplify - Debug
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

        for key, value in data.items():
            key = key.split("_")

            if key[0] == "responseAggregationType":
                break

            if key[2] == "keys" and key[3]:
                # If there are multiple keys, add key number to keys eg. [keys1, keys2]
                key = key[2] + key[3]

            key = key[2] if isinstance(key, list) else key

            if key not in self.keys:
                self.keys.append(key)

            self.values.append(value)

    def __preprocess(self):
        """
        Preprocess the data.
        """

        self._split_to_kv(self._flatten(self.data))

    def export_to_json(self, filename: Optional[str] = "analytics.json") -> None:
        with open(filename, "w") as file:
            json.dump(self.data, file, indent=4)

        print(f"Analytics successfully created in JSON format ✅")

    def export_to_table(self) -> UnicodeTableWriter:
        self.__preprocess()

        sub = len(self.keys)

        writer = UnicodeTableWriter()

        writer.table_name = "Analytics"
        writer.margin = 2

        writer.headers = self.keys
        writer.value_matrix = [
            self.values[ctr : ctr + sub]
            for ctr, _ in enumerate(self.values)
            if ctr % sub == 0
        ]

        writer.write_table()

    def export_to_csv(self, filename: Optional[str] = "analytics.csv") -> None:
        self.__preprocess()

        sub = len(self.keys)

        writer = CsvTableWriter()

        writer.table_name = "Analytics"
        writer.headers = self.keys
        writer.value_matrix = [
            self.values[ctr : ctr + sub]
            for ctr, _ in enumerate(self.values)
            if ctr % sub == 0
        ]

        writer.dump(filename)

        print(f"Analytics successfully created in CSV format ✅")

    def export_to_excel(self, filename: Optional[str] = "analytics.xlsx") -> None:
        self.__preprocess()

        sub = len(self.keys)

        writer = ExcelXlsxTableWriter()

        writer.table_name = "Analytics"

        writer.headers = self.keys
        writer.value_matrix = [
            self.values[ctr : ctr + sub]
            for ctr, _ in enumerate(self.values)
            if ctr % sub == 0
        ]

        writer.dump(filename)

        print(f"Analytics successfully created in XLSX format ✅")

