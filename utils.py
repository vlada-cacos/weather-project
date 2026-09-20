def round_json(data, digits=None):
    if type(data) == dict: 
        return {key: round_json(value, digits) for key, value in data.items()}
    elif type(data) == list: 
        return [round_json(item, digits) for item in data]
    elif type(data) == float: 
        return round(data, digits)
    else:
        return data