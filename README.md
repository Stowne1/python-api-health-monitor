# api-health-monitor

A CLI tool that checks the health of one or more HTTP endpoints concurrently, with retry logic and structured output.

## Install

```bash
pip install -e .
```

## Usage

Check one or more URLs directly:
```bash
api-health-monitor https://example.com https://api.example.com
```

Load endpoints from a config file:
```bash
api-health-monitor --config health.yml
```

Output as JSON:
```bash
api-health-monitor --json https://example.com
```

Set number of retries:
```bash
api-health-monitor --retries 5 https://example.com
```

## Config file format

```yaml
endpoints:
  - name: My API
    url: https://example.com
    timeout: 5
```

## Exit codes

- `0` — all endpoints healthy
- `1` — one or more endpoints unhealthy

## Docker

```bash
docker build -t api-health-monitor .
docker run api-health-monitor https://example.com
```

## Development

```bash
pip install -e ".[dev]"
pytest
```
