from typing import Any


def formatResultSetToDict(data) -> Any:
    result = []

    for row in data:
        result.append(dict(row))

    return result[0] if len(result) == 1 else result
