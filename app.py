from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

def get_system_prompt(role_name):
    roles = {
        "연애 고수 친구": "너는 연애 경험 많은 친구처럼, 친근하고 센스 있게 조언해줘. 감정 표현도 자연스럽게.",
        "진지한 상담가": "너는 인간관계를 잘 파악하는 성실하고 조심스러운 상담용 AI야.",
        "장난기 있는 절친": "넌 오랜 친구처럼 장난도 섞어가며 재밌고 솔직하게 말해줘.",
        "무심한 회사 동료": "넌 감정 표현이 별로 없는 무심한 직장 동료처럼 툭툭 던지듯 조언해줘."
    }
    return roles.get(role_name, roles["진지한 상담가"])

def generate_prompt(chat_text):
    return f"""
다음은 어떤 사람의 최근 카카오톡 대화 내용이야:
\"\"\"
{chat_text}
\"\"\"
이 대화를 분석해서 지금 선톡(먼저 연락)해도 어색하지 않을 타이밍인지 알려줘. 
가능하면 선톡 멘트도 한두 개 추천해줘. 너무 무겁거나 부담스럽지 않게, 자연스럽고 일상적인 말투로 알려줘.

답변은 아래 형식으로:
- 선톡 타이밍 판단: [지금 / 조금 기다려 / 아예 하지 말기]
- 이유:
- 추천 선톡 멘트:
1. ...
2. ...
"""

def ask_gpt(prompt_text, system_prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_text}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[GPT 오류] {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        chat_text = request.form.get("chat_text")
        role = request.form.get("role")
        if chat_text:
            prompt = generate_prompt(chat_text)
            system_prompt = get_system_prompt(role)
            result = ask_gpt(prompt, system_prompt)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
