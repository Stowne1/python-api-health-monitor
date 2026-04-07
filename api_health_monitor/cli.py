import sys
import json
import argparse
import asyncio
from dataclasses import asdict
from api_health_monitor.config import load_config
from api_health_monitor.checker import check_all

def main():
    parser = argparse.ArgumentParser(description="check on the health of one or more APIs")
    parser.add_argument("urls", nargs="*", help="One or more URLs to check")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--config", help="Path to YAML config file")
    args = parser.parse_args()

    if args.config:
        endpoints = load_config(args.config)
        urls = [e.url for e in endpoints]
    else:
        urls = args.urls

    results = asyncio.run(check_all(urls))
    any_unhealthy = False

    for result in results:
        if not result.is_healthy:
            any_unhealthy = True
        if args.json:
            print(json.dumps(asdict(result), default=str))
        elif result.is_healthy:        
            print(f"[HEALTHY] {result.url} - {result.status_code} ({result.response_time_ms}ms)")
        else:    
            print(f"[UNHEALTHY] {result.url} - {result.error or result.status_code}")
    if any_unhealthy:
        sys.exit(1)    


if __name__ == "__main__":
    main()
