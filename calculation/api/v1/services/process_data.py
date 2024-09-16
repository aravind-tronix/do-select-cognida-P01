import re
from datetime import datetime, timedelta

from fastapi.encoders import jsonable_encoder

from calculation.api.v1.services.parsers import parse_currency, parse_datetime, parse_percentage


def process_variables(entry: dict, var_type: str, var_name: str, data_entry: str):
    """
    entry: entries in data received
    var_type: has variable type
    var_name: holds variable name
    data_entry: a dict to build the processed data
    """
    if var_type == "currency":
        data_entry[var_name] = parse_currency(entry[var_name])
        return data_entry
    elif var_type == "percentage":
        data_entry[var_name] = parse_percentage(entry[var_name])
        return data_entry
    elif var_type == "datetime":
        data_entry[var_name] = parse_datetime(entry[var_name])
        return data_entry
    else:
        data_entry[var_name] = entry[var_name]
        return data_entry


async def evaluate_expression(expression: str, data_entry: dict):
    """Evaluate the expression safely using controlled variables and datetime handling."""
    for var, val in data_entry.items():
        if isinstance(val, datetime):
            expression = re.sub(
                r"\b" + var + r"\b",
                f"datetime({val.year}, {val.month}, {val.day}, {val.hour}, {val.minute}, {val.second})",
                expression,
            )
        else:
            expression = re.sub(r"\b" + var + r"\b", str(val), expression)

    return eval(expression, {"timedelta": timedelta, "datetime": datetime})


async def process_data(data: dict):
    """
    data: request from the user
    parses the data and stages it for further process
    """
    data = jsonable_encoder(data)
    results = {}
    for formula in data["formulas"]:
        results[formula["outputVar"]] = []
    for entry in data["data"]:
        temp_results = {}
        for formula in data["formulas"]:
            expression = formula["expression"]
            input_vars = formula["inputs"]
            data_entry = {}
            for var in input_vars:
                var_name = var["varName"]
                var_type = var["varType"]
                if var_name in entry:
                    data_entry = process_variables(entry, var_type, var_name, data_entry)
                elif var_name in temp_results:
                    data_entry[var_name] = temp_results[var_name]

            result = await evaluate_expression(expression, data_entry)
            temp_results[formula["outputVar"]] = result
            results[formula["outputVar"]].append(result)
    if len(data["formulas"]) > 1:
        return {
            "results": results,
            "status": "success",
            "message": "The formulas were executed successfully with variable-based chaining.",
        }
    return {
        "results": results,
        "status": "success",
        "message": "The formulas were executed successfully.",
    }
