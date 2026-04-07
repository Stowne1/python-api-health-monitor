import sys
import json
import argparse
import asyncio
from dataclasses import asdict
from api_health_monitor.checker import check_all

def main():
    parser = argparse.ArgumentParser(description="check on the health of one or more APIs")
    parser.add_argument("urls", nargs="+", help="One or more URLs to check")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()
    results = asyncio.run(check_all(args.urls))
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
