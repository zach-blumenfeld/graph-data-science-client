from gdsclient.topological_lp.topological_lp_runner import TopologicalLPRunner

from ..query_runner.query_runner import QueryRunner


class TopologicalLPEndpoints:
    def __init__(self, query_runner: QueryRunner, namespace: str):
        self._query_runner = query_runner
        self._namespace = namespace

    @property
    def linkprediction(self) -> TopologicalLPRunner:
        return TopologicalLPRunner(
            self._query_runner, f"{self._namespace}.linkprediction"
        )
