class AgentError(BaseException):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
