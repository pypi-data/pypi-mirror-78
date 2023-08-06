from typing import List

OS_TYPE_LINUX = "LINUX"
OS_TYPE_WINDOWS = "WINDOWS"

TYPE_ENVIRONMENT = "ENVIRONMENT"
TYPE_ENVIRONMENT_MULTI = "ENVIRONMENT_MULTI"

UPDATE_STATUS_INCOMPATIBLE = "INCOMPATIBLE"
UPDATE_STATUS_OUTDATED = "OUTDATED"
UPDATE_STATUS_SUPPRESSED = "SUPPRESSED"
UPDATE_STATUS_UNKNOWN = "UNKNOWN"
UPDATE_STATUS_UP2DATE = "UP2DATE"
UPDATE_STATUS_UPDATE_IN_PROGRESS = "UPDATE_IN_PROGRESS"
UPDATE_STATUS_UPDATE_PENDING = "UPDATE_PENDING"
UPDATE_STATUS_UPDATE_PROBLEM = "UPDATE_PROBLEM"

VERSION_COMPARE_TYPE_EQUAL = "EQUAL"
VERSION_COMPARE_TYPE_GREATER = "GREATER"
VERSION_COMPARE_TYPE_GREATER_EQUAL = "GREATER_EQUAL"
VERSION_COMPARE_TYPE_LOWER = "LOWER"
VERSION_COMPARE_TYPE_LOWER_EQUAL = "LOWER_EQUAL"

from dynatrace.metric import MetricSeries
from dynatrace.dynatrace_object import DynatraceObject


class ActiveGate(DynatraceObject):
    @property
    def id(self) -> str:
        return self._id

    def network_addresses(self) -> List[str]:
        return self._network_addresses

    def _create_from_raw_data(self, raw_element: dict):
        self._id = raw_element.get("id")
        self._network_addresses = raw_element.get("networkAddresses", [])
