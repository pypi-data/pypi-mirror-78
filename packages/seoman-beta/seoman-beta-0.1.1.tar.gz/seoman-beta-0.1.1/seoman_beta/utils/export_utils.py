from typing import Optional, Dict, Any, Union, List

import json
import csv
from collections import OrderedDict


# TODO Simplify - Debug
class ExportCSV:
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

            key = key[2]

            if key not in self.keys:
                self.keys.append(key)

            self.values.append(value)

    def export_to_csv(self, filename: Optional[str] = "analytics.csv") -> None:

        self._split_to_kv(self._flatten(self.data))

        with open(filename, "w") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(self.keys)
            for ctr, _ in enumerate(self.values):
                if ctr % 5 == 0:
                    csvwriter.writerow(self.values[ctr : ctr + 5])

        print(f"Analytics successfully created in CSV format ✅")


class ExportJSON:
    def __init__(self, data: Dict[Any, Any] = {}) -> None:
        self.data = data

    def export_to_json(self, filename: Optional[str] = "analytics.json") -> None:
        with open(filename, "w") as file:
            json.dump(self.data, file, indent=4)

        print(f"Analytics successfully created in JSON format ✅")


# TODO
class ExportTable:
    def __init__(self, data: Dict[Any, Any]):
        self.data = data

    def export_to_table(self):
        pass

