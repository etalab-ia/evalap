import re

from fastapi.responses import JSONResponse


class SchemaError(Exception):
    pass


class CustomIntegrityError(Exception):
    """Example usage:

    except IntegrityError as e:
        raise CustomIntegrityError.from_integrity_error(e.orig)

    """

    def __init__(self, message="Integrity error occurred"):
        self.message = message
        super().__init__(self.message)

    def to_http_response(self):
        """Convert the exception to a JSON response."""
        return JSONResponse(status_code=400, content={"error": "IntegrityError", "detail": self.message})

    @classmethod
    def from_integrity_error(cls, orig_error):
        error_message = str(orig_error)

        # Handle duplicate entry error
        duplicate_match = re.search(r"Key \((.*?)\)=\((.*?)\) already exists", error_message)
        constraint_match = re.search(r'unique constraint "(.*?)"', error_message)

        if duplicate_match:
            key, value = duplicate_match.groups()
            constraint_name = constraint_match.group(1)
            return DuplicateEntryError(key, value, constraint=constraint_name)

        # Placeholder for future integrity error types
        # Example: if some_other_condition:
        #     return SomeOtherIntegrityError(details)

        # If no specific case matched, return a general integrity error
        return cls("An integrity error occurred: " + error_message)


class DuplicateEntryError(CustomIntegrityError):
    def __init__(self, key, value, message="Duplicate entry detected", constraint=None):
        self.key = key
        self.value = value
        if constraint:
            message = f"{message} for constraint '{constraint}'"
        self.message = f"{message}: {key} = {value}"
        self.contraint = None
        super().__init__(self.message)

    def to_http_response(self):
        """Convert the exception to a JSON response."""
        return JSONResponse(
            status_code=409,
            content={
                "error": "DuplicateEntryError",
                "detail": self.message,
                "key": self.key,
                "value": self.value,
            },
        )
