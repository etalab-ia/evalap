from pytest import fail


def log_and_assert(response, code):
    if code != 200:
        assert response.status_code == code
        return

    if response.status_code != 200:
        fail(
            f"Expected status code 200, but got {response.status_code}.\nError details: {response.text if isinstance(response.text, str) else response}"
        )
