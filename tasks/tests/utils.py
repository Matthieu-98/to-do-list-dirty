def test_id(id_value):
    
    def decorator(func):
        setattr(func, "test_case_id", id_value)
        return func
    return decorator