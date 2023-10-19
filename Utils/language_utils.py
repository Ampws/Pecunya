class LanguageUtils:
    def __init__(self):
        import json
        print('初始化語言工具')
        with open('Utils/languages.json', 'r', encoding='utf-8') as file:
            self.languages = json.load(file)

    def translate(self, language_code, text_key):
        language_data = self.languages.get(language_code, {})
        return language_data.get(text_key, text_key)