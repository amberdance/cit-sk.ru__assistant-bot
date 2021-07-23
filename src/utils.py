from typing import Any


def pretty(data, indent=0):
    for key, value in data.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))


def formatResultSetToDict(data) -> Any:
    result = []

    for row in data:
        print(row)
        # result.append(row.__dict__) if isinstance(
        #     row, object) else result.append(dict(row))
        result.append(dict(row))

    return result[0] if len(result) == 1 else result
