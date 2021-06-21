class StorageException(Exception):
    """ StorageException - base exception for other class of exceptions. """

    pass


class LogicalException(StorageException):
    """ LogicalError - raises, when user tries to perform an illogical operation. """

    def __init__(self, message: str):
        self.msg = message
        super().__init__(self.msg)


class NotFoundException(StorageException):
    """ NotFoundError - raises, when user trying to get an nonexistent object. """

    def __init__(self, object_type: str, object_name: str):
        """
        Raises, when user trying to get an nonexistent object.
        :param object_name: name of the object, that user trying to found;
        :param object_type: type of the object (file, directory, ...) that
        user user trying to found.
        """
        self.msg = f"Could not find the {object_type} '{object_name}'"
        super().__init__(self.msg)


class AlreadyExistException(StorageException):
    """ AlreadyExistException - raises, when user trying to create already existent
    object.
    """

    def __init__(self, object_name: str):
        """
        Raises, when user trying to create already existent object.
        :param object_name: name of the object, that user trying to found;
        user user trying to found.
        """
        self.msg = f"Resource '{object_name}' already exists"
        super().__init__(self.msg)


class UnacceptableMimetypeException(StorageException):
    """
    UnacceptableMimetypeException - raises, when user trying to load file with
    unacceptable mimetype.
    """

    def __init__(self, object_name: str):
        """
        Raises, when user trying to load file with unacceptable mimetype.
        :param object_name: name of the object, that user trying to found;
        user user trying to found.
        """
        self.msg = f"Resource '{object_name}' has unacceptable mimetype"
        super().__init__(self.msg)
