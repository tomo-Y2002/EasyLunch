from google.cloud.logging import Client


class Logging:
    """
    Google Cloud Loggingを操作するためのクラス。
    """

    def __init__(self, is_gc=False):
        self.is_gc = is_gc
        if is_gc:
            self.logging_client = Client()
            self.logger = self.logging_client.logger("easylunch")

    def log_text(self, text):
        """
        ログにテキストを出力します。
        """
        if self.is_gc:
            self.logger.log_text(text)
