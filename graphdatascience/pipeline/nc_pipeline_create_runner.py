from typing import Any, Tuple

from pandas import Series

from ..caller_base import CallerBase
from ..error.illegal_attr_checker import IllegalAttrChecker
from ..error.uncallable_namespace import UncallableNamespace
from .nc_training_pipeline import NCTrainingPipeline


class NCPipelineCreateRunner(CallerBase, UncallableNamespace, IllegalAttrChecker):
    def create(self, name: str) -> Tuple[NCTrainingPipeline, "Series[Any]"]:
        self._namespace += ".create"

        query = f"CALL {self._namespace}($name)"
        params = {"name": name}
        result = self._query_runner.run_query(query, params).squeeze()

        return NCTrainingPipeline(name, self._query_runner, self._server_version), result
