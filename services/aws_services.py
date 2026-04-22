import boto3
import os
import concurrent.futures

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

translate_client = boto3.client("translate", region_name=AWS_REGION)
polly_client = boto3.client("polly", region_name=AWS_REGION)


def translate_text(text, source, target):
    return translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source,
        TargetLanguageCode=target,
    )["TranslatedText"]


def text_to_speech(text, voice):
    try:
        with concurrent.futures.ThreadPoolExecutor() as ex:
            return ex.submit(
                polly_client.synthesize_speech,
                Text=text,
                OutputFormat="mp3",
                VoiceId=voice,
            ).result(timeout=5)["AudioStream"].read()
    except:
        return None