"""Module of custom exceptions"""


class FileReadError(Exception):
    """Custom exception"""
    def __init__(self, filename):
        super().__init__(f"Error was occurred while reading {filename}")


class FieldNotFoundError(Exception):
    """Custom exception"""
    def __init__(self, field_name):
        super().__init__(f"Field: '{field_name}' not found")


class InsertActionImpossibleError(Exception):
    """Custom exception"""
    def __init__(self):
        super().__init__("Can't do insert action")


class RemoveActionImpossibleError(Exception):
    """Custom exception"""
    def __init__(self):
        super().__init__("Can't do remove action")


class DataBaseTypeNotFound(Exception):
    """Custom exception"""
    def __init__(self, db_name):
        super().__init__(f"DataBase type '{db_name}' not supported yet")


class ActionNotFound(Exception):
    """Custom exception"""
    def __init__(self, action):
        super().__init__(f"Action '{action}' not supported yet")


class ActionConfigSyntaxError(Exception):
    """Custom exception"""
    def __init__(self):
        super().__init__(f"Syntax error in action config file")
