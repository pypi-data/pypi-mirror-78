class HandlerForCommandAlreadyExistsError(Exception):
    pass


class HandlerForCommandDoesNotExistError(Exception):
    pass


class HandlerIsNotAHandlerSubClassError(Exception):
    pass


class ResolverIsNotAResolverSubClassError(Exception):
    pass
