# main.py - CRUD 함수 사용 예시

from db_utils import (
    create_student,
    get_all_students,
    get_student_by_id,
    update_student,
    delete_student
)

print("=" * 50)
print("🎓 학생 관리 시스템")
print("=" * 50)

# 1. 학생 추가 (CREATE)
# print("\\n[1] 학생 추가")
# new_id = create_student("홍길동", 25, "M")
# create_student("임꺽정", 30, "M")
# create_student("장옥정", 28, "F")

# 2. 전체 조회 (READ)
print("\\n[2] 전체 학생 목록")
students = get_all_students()
total_age = 0
if students: # [ {'id:'1,'name':'kk','age':25},{'id:'1,'name':'kk','age':25}, ]
    for s in students:
        total_age += s['age']
        print(f"  ID:{s['student_id']} | {s['name']} | {s['age']}세 | {s['gender']}")
student_count = len(students)
avg_age = total_age / student_count
print(f"총학생수={student_count}")
print(f"학생 평균나이 = {avg_age}")