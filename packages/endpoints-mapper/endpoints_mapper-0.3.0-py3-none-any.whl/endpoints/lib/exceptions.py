class HttpMethodIsNotSupported(Exception):
    def __init__(self, method, methods):
        '''
        Params:
            method (str):
                String representing the method that's not supported
            methods (list of str):
                List of Strings representing the supported methods
        '''
        msg = f'"{method}" is not in the list of supported methods: {methods}'
        super().__init__(msg)
