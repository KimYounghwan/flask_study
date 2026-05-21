#연락처 관리
from flask import Flask,render_template, request
app = Flask(__name__)

#메인
@app.route("/")
def home():
    return render_template("/contact/index.html")

#등록폼
@app.route("/contact/insert_form")
def insert_form():
    return render_template("/contact/insert_form.html")

contacts = [] # 연락처 저장용
FILE_NAME = 'contacts.json'
def load_contacts():
    import os, json
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME,"r",encoding="utf-8") as f:
            contacts = json.load(f)

def save_contact(contact):
    for ct in contacts:
        if ct["tel"] == contact["tel"]:
            return "전화번호 중복입니다"
        
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        import json
        contacts.append(contact)
        json.dump(contacts,f,ensure_ascii=False,indent=2)
        print(f"{FILE_NAME} 저장완료")
    return "등록성공"

#등록작업
@app.route("/contact/insert_action",methods=["GET","POST"])
def insert_action():
    name = request.form.get("name")
    tel = request.form.get("tel")
    company = request.form.get("company")
    buseo = request.form.get("buseo")
    jikgup = request.form.get("jikgup")
    contact = {'name':name,'tel':tel,'company':company,'buseo':buseo,'jikup':jikgup}
    msg = save_contact(contact)
    return render_template("/contact/insert_action.html", msg=msg)

@app.route("/contact/list")
def contact_list():
    count = len(contacts)
    return render_template(
        "contact/list.html", 
        count=count,
        contacts = contacts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)