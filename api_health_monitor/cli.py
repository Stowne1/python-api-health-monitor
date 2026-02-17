import argparse
from api_health_monitor.checker import check_health


def main():
    parser = argparse.ArgumentParser(description="check on the health of one ore more APIs")
    parser.add_argument("urls", nargs="+", help="One or more URLs to check")
    args = parser.parse_args()

    for url in args.urls:
        result = check_health(url)
        if result.is_healthy:
            print(f"[HEALTHY] {result.url} - {result.status_code} ({result.response_time_ms}ms)")
        else:    
            print(f"[UNHEALTHY] {result.url} - {result.error or result.status_code}")


if __name__ == "__main__":
    main()
