class AudioUndecodableException(Exception):
    """
    Bad audio
    """

    def __init__(self):
        super().__init__(self)
        self.msg = "Invalid audio file, seems to be decodable text"

    def __str__(self):
        return self.msg
