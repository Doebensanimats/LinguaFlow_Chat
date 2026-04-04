# 🌐 LinguaFlow – AI-Powered Translation App

A serverless translation web application built on AWS, featuring a Streamlit frontend, AWS Lambda backend, API Gateway REST API, SQS batch queue, and S3 storage — all provisioned with Terraform.

---

## 📐 Architecture

```
User (Streamlit UI)
        │
        ▼
API Gateway (REST)
        │
        ▼
AWS Lambda (Python 3.11)
        │
        ├──► AWS Translate
        │
        └──► SQS Queue (batch jobs)
                │
                ▼
           S3 Buckets (input / responses)
```

---

## 🚀 Features

- **Single text translation** — translate any text instantly via the web UI
- **Batch file upload** — upload CSV or TXT files for bulk translation
- **SQS queue support** — large batch jobs sent asynchronously via SQS
- **Translation history** — session history with CSV export
- **Download results** — download single or batch translations
- **26 languages supported** — including African languages (Swahili, Hausa, Yoruba, Amharic)

---

## 🗂️ Project Structure

```
translation-app/
│
├── app.py                        # Streamlit frontend
├── requirements.txt              # Python dependencies
├── README.md
├── .gitignore
│
└── terraform/
    ├── main.tf                   # Root Terraform config
    ├── variables.tf
    ├── outputs.tf
    ├── terraform.tfvars          # ⚠️ Not committed (secrets)
    │
    └── modules/
        ├── lambda/
        │   ├── main.tf
        │   ├── variables.tf
        │   ├── outputs.tf
        │   └── lambda_function.py
        ├── api_gateway/
        │   ├── main.tf
        │   ├── variables.tf
        │   └── outputs.tf
        ├── s3/
        │   ├── main.tf
        │   ├── variables.tf
        │   └── outputs.tf
        └── sqs/
            ├── main.tf
            ├── variables.tf
            └── outputs.tf
```

---

## ⚙️ Prerequisites

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) configured (`aws configure`)
- [Terraform](https://developer.hashicorp.com/terraform/downloads) >= 1.3
- Python >= 3.11
- pip

---

## 🛠️ Infrastructure Setup (Terraform)

```bash
cd terraform

# Initialise providers
terraform init

# Preview changes
terraform plan

# Deploy
terraform apply
```

After apply, note the outputs:

```
api_url                = "https://xxxx.execute-api.us-east-1.amazonaws.com/prod/translate"
sqs_queue_url          = "https://sqs.us-east-1.amazonaws.com/..."
input_bucket_arn       = "arn:aws:s3:::translation-app-input-2026"
responses_bucket_arn   = "arn:aws:s3:::translation-app-response-2026"
```

---

## 💻 Running the App Locally

**1. Clone the repo**
```bash
git clone https://github.com/your-username/translation-app.git
cd translation-app
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure AWS credentials**
```bash
aws configure
```

**4. Set your API URL**

Open `app.py` and update:
```python
API_URL       = "https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/translate"
SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/your-account-id/translation-batch-queue"
```

**5. Run the app**
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧪 Testing the API Directly

```bash
curl -X POST https://your-api-url/prod/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "source_lang": "en", "target_lang": "es"}'
```

Expected response:
```json
{
  "original": "Hello",
  "translated": "Hola"
}
```

Or test Lambda directly via CLI:
```bash
aws lambda invoke \
  --function-name translation-lambda \
  --payload '{"body": "{\"text\": \"Hello\", \"source_lang\": \"en\", \"target_lang\": \"es\"}"}' \
  --cli-binary-format raw-in-base64-out \
  response.json && cat response.json
```

---

## 🌍 Supported Languages

| Language | Code | Language | Code |
|----------|------|----------|------|
| English | `en` | Arabic | `ar` |
| Spanish | `es` | Hindi | `hi` |
| French | `fr` | Swahili | `sw` |
| German | `de` | Hausa | `ha` |
| Italian | `it` | Yoruba | `yo` |
| Portuguese | `pt` | Amharic | `am` |
| Chinese (Simplified) | `zh` | Turkish | `tr` |
| Japanese | `ja` | Korean | `ko` |

Full list of AWS Translate supported languages: [AWS docs](https://docs.aws.amazon.com/translate/latest/dg/what-is-languages.html)

---

## 🔐 IAM Permissions Required

The Lambda execution role needs:

```json
{
  "Effect": "Allow",
  "Action": ["translate:TranslateText"],
  "Resource": "*"
}
```

```json
{
  "Effect": "Allow",
  "Action": ["sqs:SendMessage", "sqs:ReceiveMessage", "sqs:DeleteMessage"],
  "Resource": "arn:aws:sqs:us-east-1:YOUR_ACCOUNT_ID:translation-batch-queue"
}
```

---

## 🧹 Tear Down

To destroy all AWS resources:
```bash
cd terraform
terraform destroy
```

---

## 📄 License

MIT License — free to use and modify.

---

## 🙋 Author

Built by **[Your Name]** · [GitHub](https://github.com/your-username) · [LinkedIn](https://linkedin.com/in/your-profile)
