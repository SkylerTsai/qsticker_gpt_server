from deep_translator import GoogleTranslator

class Translator:
    def __init__(self, lang = 'zh-TW') -> None:
        self.lang_init(lang)
    
    def lang_init(self, lang):
        self.lang = lang
        self.translator = GoogleTranslator(source='auto', target=lang)
    
    def translate(self, msg):
        return self.translator.translate(text=msg)