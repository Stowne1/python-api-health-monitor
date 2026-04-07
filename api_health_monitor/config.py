import yaml
from dataclasses import dataclass


@dataclass
class EndpointConfig:
    url: str
    name: str = ""
    timeout: float = 5.0

def load_config(path: str) -> list[EndpointConfig]:
    with open(path) as f:
        data = yaml.safe_load(f)
    return [EndpointConfig(**endpoint) for endpoint in data["endpoints"]]    
