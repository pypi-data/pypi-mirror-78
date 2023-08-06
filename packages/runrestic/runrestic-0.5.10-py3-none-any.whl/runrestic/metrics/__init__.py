from typing import Any, List, Dict

from . import prometheus


def write_metrics(metrics: Dict[str, Any], config: Dict[str, Any], actions: List=None) -> None:
    configuration = config["metrics"]
    if "prometheus" in configuration.keys():
        lines = prometheus.generate_lines(metrics, config["name"])

        with open(configuration["prometheus"]["path"], "w") as file:
            file.writelines("".join(lines))
