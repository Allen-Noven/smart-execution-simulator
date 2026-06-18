# ====================================
# ai_risk_classifier.py
# ====================================

import requests
import json

from utils.config import (

    DEEPSEEK_API_KEY
)


class AIRiskClassifier:

    def __init__(self):

        # ====================================
        # DEEPSEEK CONFIG
        # ====================================

        self.api_key = (
            DEEPSEEK_API_KEY
        )

        self.url = (
            "https://api.deepseek.com/chat/completions"
        )


    # ====================================
    # CLASSIFY NEWS RISK
    # ====================================

    def classify_news(

        self,

        news_event

    ):

        headline = (
            news_event["headline"]
        )

        summary = (
            news_event["summary"]
        )

        # ====================================
        # AI PROMPT
        # ====================================

        prompt = f"""

You are an institutional
execution risk analyst.

Analyze the following market news.

Headline:
{headline}

Summary:
{summary}

Determine:

1. Risk severity:
LOW / MEDIUM / HIGH

2. Should execution halt?
true / false

3. Is liquidity risk elevated?
true / false

4. Is volatility risk elevated?
true / false

5. Short reasoning.

Return ONLY valid JSON.

Example:

{{
    "severity": "HIGH",

    "halt_execution": true,

    "liquidity_risk": true,

    "volatility_risk": true,

    "reason":
    "Potential regulatory investigation"
}}

"""

        # ====================================
        # API HEADERS
        # ====================================

        headers = {

            "Authorization":
            f"Bearer {self.api_key}",

            "Content-Type":
            "application/json"
        }


        # ====================================
        # API PAYLOAD
        # ====================================

        payload = {

            "model": "deepseek-chat",

            "messages": [

                {
                    "role": "user",

                    "content": prompt
                }
            ],

            "temperature": 0
        }


        # ====================================
        # SEND REQUEST
        # ====================================

        response = requests.post(

            self.url,

            headers=headers,

            json=payload
        )


        # ====================================
        # HANDLE API ERROR
        # ====================================

        if response.status_code != 200:

            print(

                "\nAI Classification Failed.\n"
            )

            print(response.text)

            return None


        result = response.json()


        # ====================================
        # EXTRACT AI RESPONSE
        # ====================================

        content = (

            result["choices"][0]
            ["message"]["content"]
        )


        # ====================================
        # CONVERT JSON STRING
        # ====================================

        try:

            classification = (
                json.loads(content)
            )

            return classification

        except Exception as e:

            print(

                "\nJSON Parsing Error.\n"
            )

            print(content)

            return None


    # ====================================
    # SHOW AI RESULT
    # ====================================

    def show_classification(

        self,

        result

    ):

        if result is None:

            return

        print(

            "\n========== AI RISK ANALYSIS ==========\n"
        )

        print(

            f"Severity: "
            f"{result['severity']}"
        )

        print(

            f"Halt Execution: "
            f"{result['halt_execution']}"
        )

        print(

            f"Liquidity Risk: "
            f"{result['liquidity_risk']}"
        )

        print(

            f"Volatility Risk: "
            f"{result['volatility_risk']}"
        )

        print(

            f"Reason: "
            f"{result['reason']}"
        )

        print(

            "\n======================================\n"
        )


# ====================================
# MAIN
# ====================================

if __name__ == "__main__":

    sample_news = {

        "headline":
        "NVDA under DOJ investigation",

        "summary":
        "The Department of Justice has "
        "opened an investigation into "
        "NVDA regarding potential "
        "anti-competitive practices."
    }

    classifier = (
        AIRiskClassifier()
    )

    result = (

        classifier.classify_news(
            sample_news
        )
    )

    classifier.show_classification(
        result
    )