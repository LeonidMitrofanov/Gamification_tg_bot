class InvalidDefaultLanguageError(Exception):
    def __init__(self, default_language, message="Invalid default language specified"):
        self.default_language = default_language
        self.message = message
        super().__init__(f"{message}: {default_language}")
