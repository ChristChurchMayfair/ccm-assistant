import csv
from typing import Optional, Dict, Any
import datetime

import requests
from requests import Response


from config import BIBLE_PASSAGES_CSV_URL
from custom_types import Service


def get_passage(date: datetime.date, service: Service) -> Optional[Dict[str, Any]]:
    # Returns a dictionary of the book and start and end chapters and verses
    # for the given service

    try:
        response: Response = requests.get(BIBLE_PASSAGES_CSV_URL)
        reader: csv.DictReader = csv.DictReader(response.iter_lines(decode_unicode=True))
        for row in reader:
            if row['date'] == date.strftime('%Y-%m-%d'):
                if not row[f'{service.name} book']:
                    return None

                return {
                    'book': row[f'{service.name} book'],
                    'start': {
                        'chapter': row[f'{service.name} start chapter'],
                        'verse': row[f'{service.name} start verse']
                    },
                    'end': {
                        'chapter': row[f'{service.name} end chapter'],
                        'verse': row[f'{service.name} end verse']
                    }
                }
        raise RuntimeError(f"Couldn't find Bible passage for {date.strftime('%Y-%m-%d')}")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error getting Bible passage: {e}")
