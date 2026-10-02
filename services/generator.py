import json
from services.llm import ask_llm

def make_questions(txt,sub,marks,cnt,diff,typ,dist):
    marks=int(marks)
    cnt=int(cnt)

    base=marks//cnt
    rem=marks%cnt
    ms=[]

    for i in range(cnt):
        ms.append(base+(1 if i<rem else 0))

    p=f"""
You are a university question paper generator.

Subject: {sub}

Syllabus:
{txt}

Requirements:
Total marks: {marks}
Number of questions: {cnt}
Difficulty: {diff}
Question type: {typ}
Unit distribution: {dist}

Generate exactly {cnt} questions.

The marks for each question must be exactly:
{ms}

Every question must be based only on the provided syllabus.

Return ONLY valid JSON in this format:

{{
    "questions":[
        {{
            "question":"...",
            "type":"...",
            "marks":5,
            "difficulty":"...",
            "unit":"..."
        }}
    ]
}}

Do not add explanations or markdown.
"""

    ans=ask_llm(p,True)
    return json.loads(ans)