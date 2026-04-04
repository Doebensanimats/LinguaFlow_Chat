import json
import boto3

translate = boto3.client('translate')

def lambda_handler(event, context):
    try:
        print("EVENT:", event)

        # Parse API Gateway body
        body = json.loads(event.get("body", "{}"))

        text = body.get("text", "")
        source = body.get("source_lang", "en")
        target = body.get("target_lang", "es")

        # Call AWS Translate
        response = translate.translate_text(
            Text=text,
            SourceLanguageCode=source,
            TargetLanguageCode=target
        )

        translated_text = response["TranslatedText"]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "original": text,
                "translated": translated_text
            })
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }