import requests

def ask_llm(prompt,json_mode=False):
    url="http://localhost:11434/api/generate"
    data={
        "model":"qwen2.5:7b",
        "prompt":prompt,
        "stream":False
    }

    if json_mode:
        data["format"]="json"

    res=requests.post(url,json=data)
    res.raise_for_status()

    return res.json()["response"]