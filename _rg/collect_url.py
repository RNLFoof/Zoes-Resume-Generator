import os
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import orjson
import pyperclip


class Consumption(Enum):
    COMPLETE = 0
    COMPLETE_QUESTIONABLE_UNDERSTANDING = 1
    REFERENCE = 2


@dataclass
class UrlMetadata:
    consumption: Consumption
    consumed_at: datetime = datetime.now(tz=timezone.utc)


url_collection_path = "../url_collection.json"


def main():
    url_collection: dict[str, list[UrlMetadata]]
    print("Getting", url := pyperclip.paste())
    if os.path.exists(url_collection_path):
        with open(url_collection_path, "rb") as f:
            url_collection = orjson.loads(f.read())
    else:
        url_collection = {}

    url_collection.setdefault(url, [])
    url_collection[url].append(UrlMetadata(Consumption.COMPLETE))

    with open(url_collection_path, "wb") as f:
        f.write(orjson.dumps(url_collection))


if __name__ == "__main__":
    main()
