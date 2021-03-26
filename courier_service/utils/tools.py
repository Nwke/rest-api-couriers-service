def containing_check(fields, data):
    for field in fields:
        if not field in data:
            return False
    return True
