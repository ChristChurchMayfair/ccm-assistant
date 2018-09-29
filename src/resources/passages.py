import csv
import requests

from config import BIBLE_PASSAGES_CSV_URL


def get_passage(date, service):
    # Returns a dictionary of the book and start and end chapters and verses
    # for the given service

    try:
        response = requests.get(BIBLE_PASSAGES_CSV_URL)
        reader = csv.DictReader(response.iter_lines())
        for row in reader:
            if row['date'] == date.strftime('%Y-%m-%d'):
                if not row['{} book'.format(service)]:
                    return None

                return {
                    'book': row['{} book'.format(service)],
                    'start': {
                        'chapter': row['{} start chapter'.format(service)],
                        'verse': row['{} start verse'.format(service)]
                    },
                    'end': {
                        'chapter': row['{} end chapter'.format(service)],
                        'verse': row['{} end verse'.format(service)]
                    }
                }
        return None
    except requests.exceptions.RequestException as e:
        print(e)
        return None
