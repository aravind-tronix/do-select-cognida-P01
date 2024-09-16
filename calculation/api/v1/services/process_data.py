from fastapi.encoders import jsonable_encoder
from calculation.api.v1.services.parsers import parse_currency, parse_datetime, parse_percentage
from datetime import datetime, timedelta
import re


def process_variables(entry, var_type, var_name, data_entry):
    if var_type == "currency":
        data_entry[var_name] = parse_currency(entry[var_name])
        return data_entry
    elif var_type == "percentage":
        data_entry[var_name] = parse_percentage(
            entry[var_name])
        return data_entry
    elif var_type == "datetime":
        data_entry[var_name] = parse_datetime(entry[var_name])
        return data_entry
    else:
        data_entry[var_name] = entry[var_name]
        return data_entry


async def evaluate_expression(expression, data_entry):
    """Evaluate the expression safely using controlled variables and datetime handling."""
    for var, val in data_entry.items():
        if isinstance(val, datetime):
            expression = re.sub(
                r'\b' + var + r'\b', f"datetime({val.year}, {val.month}, {val.day}, {val.hour}, {val.minute}, {val.second})", expression)
        else:
            expression = re.sub(r'\b' + var + r'\b', str(val), expression)

    return eval(expression, {"timedelta": timedelta, "datetime": datetime})


async def process_data(data):
    data = jsonable_encoder(data)
    results = {}
    for formula in data['formulas']:
        results[formula['outputVar']] = []
    for entry in data['data']:
        temp_results = {}
        for formula in data['formulas']:
            expression = formula['expression']
            input_vars = formula['inputs']
            data_entry = {}
            for var in input_vars:
                var_name = var['varName']
                var_type = var['varType']
                if var_name in entry:
                    data_entry = process_variables(
                        entry, var_type, var_name, data_entry)
                elif var_name in temp_results:
                    data_entry[var_name] = temp_results[var_name]

            result = await evaluate_expression(expression, data_entry)
            temp_results[formula['outputVar']] = result
            results[formula['outputVar']].append(result)

    return {
        "results": results,
        "status": "success",
        "message": "The formulas were executed successfully."
    }
