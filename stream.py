class Stream:
    def __init__(self, putFunc):
        self.putFunc = putFunc
        self.stream = None

    def respondToPut(self, data):
        self.putFunc(data)

    def close(self):
        if self.stream is not None:
            try:
                self.stream.close()
            except RuntimeError: # These errors are thrown due to bugs in the Pyrebase library 
                pass
            except AttributeError:
                pass

        self.stream = None