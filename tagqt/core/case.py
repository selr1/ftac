class CaseConverter:
    @staticmethod
    def to_title_case(text):
        if not text: return ""
        # Simple title case, can be improved with library like titlecase if needed
        return text.title()

    @staticmethod
    def to_sentence_case(text):
        if not text: return ""
        return text.capitalize()

    @staticmethod
    def to_upper_case(text):
        if not text: return ""
        return text.upper()
    
    @staticmethod
    def to_lower_case(text):
        if not text: return ""
        return text.lower()
