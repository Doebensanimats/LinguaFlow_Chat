from services.aws_service import translate_text, text_to_speech


def process_message(text, src_lang, tgt_lang, voice):
    """
    Core AI pipeline:
    text → translate → speech
    """

    translated = translate_text(text, src_lang, tgt_lang)
    audio = text_to_speech(translated, voice)

    return translated, audio