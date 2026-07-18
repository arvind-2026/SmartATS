import config


def get_file_extension(file_name):
    """Return the lowercase extension from a file name."""

    if config.FILE_NAME_SEPARATOR not in file_name:
        return ""

    return file_name.rsplit(config.FILE_NAME_SEPARATOR, 1)[-1].lower()


def validate_file(file_name, file_size):
    """Check a resume file name and size before text extraction."""

    result = {
        "valid": False,
        "file_name": file_name,
        "file_extension": get_file_extension(file_name),
        "message": "",
    }

    if file_size == 0:
        result["message"] = config.EMPTY_FILE_MESSAGE
        return result

    maximum_size = config.MAX_FILE_SIZE_MB * config.BYTES_PER_MB

    if file_size > maximum_size:
        result["message"] = config.TOO_LARGE_FILE_MESSAGE
        return result

    if result["file_extension"] not in config.ALLOWED_FILE_TYPES:
        result["message"] = config.INVALID_FILE_MESSAGE
        return result

    result["valid"] = True
    result["message"] = "File validation passed."

    return result


def validate_file_count(number_of_files):
    """Check that the resume batch is not larger than the configured limit."""

    if number_of_files > config.MAX_FILES_PER_BATCH:
        return False, config.TOO_MANY_FILES_MESSAGE

    return True, ""

