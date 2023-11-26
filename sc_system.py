from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
import sqlite3

# 数据库设置
conn = sqlite3.connect(':memory:', check_same_thread=False)  # 使用内存数据库
cursor = conn.cursor()
cursor.execute('''CREATE TABLE courses (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    teacher TEXT NOT NULL
                  )''')

# 课程类定义
class Course:
    def __init__(self, name, teacher):
        self.name = name
        self.teacher = teacher

    def add_to_db(self):
        cursor.execute('INSERT INTO courses (name, teacher) VALUES (?, ?)', (self.name, self.teacher))
        conn.commit()

    @staticmethod
    def delete_from_db(course_id):
        cursor.execute('DELETE FROM courses WHERE id = ?', (course_id,))
        conn.commit()

    @staticmethod
    def find_course(course_id):
        cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
        return cursor.fetchone()

    @staticmethod
    def update_course(course_id, new_name=None, new_teacher=None):
        if new_name and new_teacher:
            cursor.execute('UPDATE courses SET name = ?, teacher = ? WHERE id = ?', (new_name, new_teacher, course_id))
        elif new_name:
            cursor.execute('UPDATE courses SET name = ? WHERE id = ?', (new_name, course_id))
        elif new_teacher:
            cursor.execute('UPDATE courses SET teacher = ? WHERE id = ?', (new_teacher, course_id))
        conn.commit()

# 前端界面函数
def main():
    while True:
        # 显示所有课程
        cursor.execute('SELECT * FROM courses')
        courses = cursor.fetchall()
        clear()  # 清除旧的输出
        put_html("<h1>已选课程</h1>")
        put_table([['ID', '课程名称', '教师']] + [[course[0], course[1], course[2]] for course in courses])

        # 选项操作
        operation = radio("选择操作", options=['增加课程', '删除课程', '修改课程', '退出'])
        
        if operation == '增加课程':
            course_data = input_group("增加新课程", [
                input("课程名称", name="name"),
                input("教师姓名", name="teacher")
            ])
            Course(course_data['name'], course_data['teacher']).add_to_db()

        elif operation == '删除课程':
            course_id = input("请输入要删除的课程ID", type=NUMBER)
            Course.delete_from_db(course_id)

        elif operation == '修改课程':
            course_data = input_group("修改课程", [
                input("课程ID", type=NUMBER, name="id"),
                input("新的课程名称（可选）", name="new_name", required=False),
                input("新的教师姓名（可选）", name="new_teacher", required=False)
            ])
            Course.update_course(course_data['id'], course_data['new_name'], course_data['new_teacher'])

        elif operation == '退出':
            break

# 启动服务器
if __name__ == '__main__':
    start_server(main, port=8080)

