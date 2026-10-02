from flask import Flask,request,jsonify,send_from_directory
from werkzeug.utils import secure_filename
from services.parser import get_text
from services.generator import make_questions
import os

app=Flask(__name__,static_folder="frontend",static_url_path="")
up="uploads"
os.makedirs(up,exist_ok=True)

@app.route("/")
def home():
    return send_from_directory("frontend","index.html")

@app.route("/upload",methods=["POST"])
def upload():
    f=request.files.get("file")

    if not f:
        return jsonify({"ok":False,"msg":"No file uploaded"}),400

    name=secure_filename(f.filename)
    path=os.path.join(up,name)
    f.save(path)

    txt=get_text(path)

    if not txt:
        return jsonify({"ok":False,"msg":"Could not extract text from file"}),400

    sub=request.form.get("sub")
    marks=request.form.get("marks")
    cnt=request.form.get("cnt")
    diff=request.form.get("diff")
    typ=request.form.get("type")
    dist=request.form.get("dist")

    try:
        paper=make_questions(txt,sub,marks,cnt,diff,typ,dist)
    except Exception as e:
        print("Generation error:",e)
        return jsonify({"ok":False,"msg":"Could not generate questions"}),500

    print("\n--- GENERATED QUESTIONS ---")
    print(paper)
    print("----------------------------\n")

    return jsonify({
        "ok":True,
        "file":name,
        "sub":sub,
        "dur":request.form.get("dur"),
        "marks":marks,
        "cnt":cnt,
        "diff":diff,
        "type":typ,
        "dist":dist,
        "paper":paper
    })

if __name__=="__main__":
    app.run(debug=True)