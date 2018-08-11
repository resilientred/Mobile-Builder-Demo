class Letter:

    def __init__(self,
                 sender: str,
                 addressee: str,
                 title: str="Empty Gootax Mobile Builder",
                 message: str="",
                 files=None):
        if files is None:
            files = []
        self.message = message
        self.title = title
        self.sender = sender
        self.addressee = addressee
        self.files = files



