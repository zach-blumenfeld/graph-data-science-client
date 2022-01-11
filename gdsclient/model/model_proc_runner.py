from typing import Optional, Union

from ..query_runner.query_runner import QueryResult, QueryRunner
from .model import Model

ModelId = Union[Model, str]


class ModelProcRunner:
    def __init__(self, query_runner: QueryRunner, namespace: str):
        self._query_runner = query_runner
        self._namespace = namespace

    @staticmethod
    def _model_name(model_id: ModelId) -> str:
        if isinstance(model_id, str):
            return model_id
        elif isinstance(model_id, Model):
            return model_id.name()

        raise ValueError(
            f"Provided model identifier is of the wrong type: {type(model_id)}"
        )

    # TODO: Figure out how to integration test
    def store(
        self, model_id: ModelId, failIfUnsupportedType: bool = True
    ) -> QueryResult:
        self._namespace += ".store"

        query = f"CALL {self._namespace}($model_name, $fail_flag)"
        params = {
            "model_name": ModelProcRunner._model_name(model_id),
            "fail_flag": failIfUnsupportedType,
        }

        return self._query_runner.run_query(query, params)

    def list(self, model_id: Optional[ModelId] = None) -> QueryResult:
        self._namespace += ".list"

        if model_id:
            query = f"CALL {self._namespace}($model_name)"
            params = {"model_name": ModelProcRunner._model_name(model_id)}
        else:
            query = f"CALL {self._namespace}()"
            params = {}

        return self._query_runner.run_query(query, params)

    def exists(self, model_id: ModelId) -> QueryResult:
        self._namespace += ".exists"

        query = f"CALL {self._namespace}($model_name)"
        params = {"model_name": ModelProcRunner._model_name(model_id)}

        return self._query_runner.run_query(query, params)

    def publish(self, model_id: ModelId) -> Model:
        self._namespace += ".publish"

        query = f"CALL {self._namespace}($model_name)"
        params = {"model_name": ModelProcRunner._model_name(model_id)}

        result = self._query_runner.run_query(query, params)

        return Model(result[0]["modelInfo"]["modelName"], self._query_runner)

    def drop(self, model_id: ModelId) -> QueryResult:
        self._namespace += ".drop"

        query = f"CALL {self._namespace}($model_name)"
        params = {"model_name": ModelProcRunner._model_name(model_id)}

        return self._query_runner.run_query(query, params)

    # TODO: Figure out how to integration test
    def load(self, model_name: str) -> Model:
        self._namespace += ".load"

        query = f"CALL {self._namespace}($model_name)"
        params = {"model_name": model_name}

        result = self._query_runner.run_query(query, params)

        return Model(result[0]["modelName"], self._query_runner)

    # TODO: Figure out how to integration test
    def delete(self, model_id: ModelId) -> QueryResult:
        self._namespace += ".delete"

        query = f"CALL {self._namespace}($model_name)"
        params = {"model_name": ModelProcRunner._model_name(model_id)}

        return self._query_runner.run_query(query, params)

    def get(self, model_name: str) -> Model:
        if self._namespace != "gds.model":
            raise SyntaxError(f"There is no {self._namespace + '.get'} to call")

        self._namespace = "gds.beta.model"
        if not self.exists(model_name)[0]["exists"]:
            raise ValueError(f"No loaded model named '{model_name}' exists")

        return Model(model_name, self._query_runner)