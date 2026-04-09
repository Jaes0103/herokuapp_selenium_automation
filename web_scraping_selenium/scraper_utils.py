"""Utility functions for web scraping operations."""

import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any


class DataExporter:
    """Handles exporting scraped data to various formats."""

    @staticmethod
    def to_json(data: Dict[str, Any], filename: str) -> str:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return filename

    @staticmethod
    def to_csv(data: List[Dict[str, Any]], filename: str, fieldnames: List[str]) -> str:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        return filename

    @staticmethod
    def generate_filename(base_name: str, extension: str, output_dir: str = "scraped_data") -> str:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{output_dir}/{base_name}_{timestamp}.{extension}"


class ScraperStats:
    """Track scraping statistics."""

    def __init__(self):
        self.start_time = datetime.now()
        self.items_scraped = 0
        self.errors = 0
        self.pages_visited = 0

    def record_item(self):
        self.items_scraped += 1

    def record_error(self):
        self.errors += 1

    def record_page(self):
        self.pages_visited += 1

    def get_summary(self) -> Dict[str, Any]:
        duration = (datetime.now() - self.start_time).total_seconds()
        return {
            "duration_seconds": round(duration, 2),
            "items_scraped": self.items_scraped,
            "errors": self.errors,
            "pages_visited": self.pages_visited,
            "items_per_second": round(self.items_scraped / duration, 2) if duration > 0 else 0
        }
