# 회원관리기능(회원등록,목록,검색,상세,수정,삭제)
"""
1.회원목록    /member/list
2.회원등록폼   /member/insert_form
3.회원등록작업 /member/insert_action
4.회원상세보기 /member/<mid>
5.회원수정폼  /member/update_form/<mid>
6.회원수정작업 /member/update_action
7.회원삭제폼 /member/delete_form/<mid>
8.회원삭제작업 /member/delete_action

** 작업순서
- 작업명의 url 지정  /member/XXX
- url을 app.py 등록및 작업처리코드 작성
- 작업결과 html을 템플릿으로 작성
"""
from flask import Flask, render_template, request
app = Flask(__name__)

members = [] # 회원전체정보
FILE_NAME = "members.json"

def load_members(): 
    global members
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        import json
        members = json.load(f)

load_members()

@app.route("/") # 메인화면
def home():
    return render_template("index.html")

@app.route("/member/insert_form") #등록폼
def member_insert_form():
    return render_template("member/insert_form.html")

@app.route("/member/insert_action", methods=['GET','POST']) #등록작업
def member_insert_action():
    # 입력정보추출
    mid = request.form.get("mid") #회원아이디
    mnm = request.form.get("mnm") #회원이름
    mpw = request.form.get("mpw") #회원비번
    mem = {"mid":mid, "mnm":mnm, "mpw":mpw}
    msg = save_member(mem)
    print('회원입력정보',mem)
    return render_template(
        "member/insert_action.html",msg=msg)

def save_member(member):
    for mem in members:
        if mem["mid"] == member["mid"]:
            return "이미 등록된 ID입니다"
        
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        import json
        members.append(member)
        json.dump(members,f,ensure_ascii=False,indent=2)
        print(f"{FILE_NAME} 저장완료")
    return "등록성공"

def update_member(member):
    for mem in members:
        if mem['mid'] == member['mid']:
            mem['mnm'] = member['mnm']
            mem['mpw'] = member['mpw']
            break

    with open(FILE_NAME, "w", encoding="utf-8") as f:
        import json
        
        json.dump(members,f,ensure_ascii=False,indent=2)
        print(f"{FILE_NAME} 저장완료")

def delete_member(member): #회원삭제
    target_mem = 0 #삭제하려는 회원정보 저장용
    for mem in members:
        if mem['mid'] == member['mid']:
            target_mem = mem
            break
    if target_mem == 0:
        return "못찾았음"
    #비번 비교
    if target_mem["mpw"] != member["mpw"]:
        return "암호 틀림"
    #회원삭제
    members.remove(target_mem)

    with open(FILE_NAME, "w", encoding="utf-8") as f:
        import json
        json.dump(members,f,ensure_ascii=False,indent=2)
        print(f"{FILE_NAME} 삭제완료")
    return "삭제완료"

@app.route("/member/list")
def member_list():
    mem_count = len(members)#회원수
    return render_template(
        "member/list.html", 
        mem_count=mem_count,
        members = members)

# 회원정보상세보기
@app.route("/member/<mid>")
def member_detail(mid):
    # [ {mid:.., mnm:..., mpw:...}  ]
    target_mem = 0
    for mem in members:
        if mem["mid"] == mid:
            target_mem = mem
            break #찾았으면 검색중지
    msg = "못찾았음" if target_mem==0 else "찾았음"
    return render_template(
        "member/detail.html", 
        msg=msg, 
        target_mem = target_mem)     

@app.route("/member/update_form/<mid>")
def update_form(mid):
    target_mem = 0
    for mem in members:
        if mem["mid"] == mid:
            target_mem = mem
            break #찾았으면 검색중지
    if target_mem == 0:
        return render_template(
            "error.html",
            msg= f"{mid} : 없거나 삭제된 회원")
    return render_template(
        "member/update_form.html", 
        mem = target_mem)     

@app.route("/member/update_action", methods=['GET','POST']) # 수정작업
def member_update_action():
    # 입력정보추출
    mid = request.form.get("mid") #회원아이디
    mnm = request.form.get("mnm") #회원이름
    mpw = request.form.get("mpw") #회원비번
    mem = {"mid":mid, "mnm":mnm, "mpw":mpw}
    update_member(mem)
    print('회원수정',mem)
    return render_template("member/update_action.html",msg="수정성공")

@app.route("/member/delete_form/<mid>")
def delete_form(mid):
    target_mem = 0
    for mem in members:
        if mem["mid"] == mid:
            target_mem = mem
            break #찾았으면 검색중지
    if target_mem == 0:
        return render_template(
            "error.html",
            msg= f"{mid} : 없거나 삭제된 회원")
    return render_template(
        "member/delete_form.html",  
        mem = target_mem)     

@app.route("/member/delete_action", methods=['GET','POST']) # 삭제작업
def member_delete_action():
    # 입력정보추출
    mid = request.form.get("mid") #회원아이디
    mpw = request.form.get("mpw") #회원비번
    mem = {"mid":mid, "mpw":mpw}
    msg = delete_member(mem)
    print('회원삭제',mem)
    return render_template(
        "member/delete_action.html",msg=msg)


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True,)