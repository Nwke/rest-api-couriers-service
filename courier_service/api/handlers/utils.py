def containing_check(fields, data: dict):
    for field in fields:
        field_is_ok = data.get(field, False)
        if not field_is_ok:
            return False
    return True
