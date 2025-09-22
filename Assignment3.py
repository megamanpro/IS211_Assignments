import csv
import re
import argparse
import io
import urllib.request
from collections import Counter

def parse_args():
    p = argparse.ArgumentParser(
        description='Report image‐hit percentage and top browser from a CSV log.'
    )
    p.add_argument(
        'filepath',
        help='Local path or HTTP URL to the weblog CSV'
    )
    return p.parse_args()

def open_source(source):
    if source.startswith(('http://', 'https://')):
        resp = urllib.request.urlopen(source)
        return io.TextIOWrapper(resp, encoding='utf-8', errors='replace')
    else:
        return open(source, newline='', encoding='utf-8')

def main():
    args = parse_args()

    image_re = re.compile(r'\.(jpg|gif|png)$', re.IGNORECASE)
    browser_patterns = {
        'Firefox': re.compile(r'Firefox/'),
        'Chrome': re.compile(r'Chrome/'),
        'Internet Explorer': re.compile(r'MSIE |Trident/'),
        'Safari': re.compile(r'Safari/')
    }

    total_hits = 0
    image_hits = 0
    browser_counts = Counter()

    with open_source(args.filepath) as f:
        reader = csv.reader(f)
        for row in reader:
            total_hits += 1
            path, timestamp, ua, status, size = row

            if image_re.search(path):
                image_hits += 1

            for name, pattern in browser_patterns.items():
                if pattern.search(ua):
                    if name == 'Safari' and browser_patterns['Chrome'].search(ua):
                        continue
                    browser_counts[name] += 1
                    break
            else:
                browser_counts['Other'] += 1

    pct = (image_hits / total_hits * 100) if total_hits else 0
    print(f'Image requests account for {pct:.1f}% of all requests '
          f'({image_hits}/{total_hits})')

    top_browser, top_count = browser_counts.most_common(1)[0]
    print(f'The most popular browser is {top_browser} with {top_count} requests')

if __name__ == '__main__':
    main()
