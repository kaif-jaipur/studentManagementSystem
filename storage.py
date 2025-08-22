# # # from student import student
# # # import os
# # # import pickle

# # # file_name="student.pkl"
# # # def save_student(s):
# # #     student = []
# # #     if os.path.exists(file_name):
# # #         with open(file_name,"rb") as f:
# # #             student=pickle.load(f)
# # #     student.append(s)
# # #     with open(file_name,"wb") as f:
# # #         pickle.dump(student,f)
# # # '''s1=student("Alice",20)
# # # s2=student("Bob",22)
# # # save_student(s1)
# # # save_student(s2)'''
# # # def load_students():
# # #     if os.path.exists(file_name):
# # #         with open(file_name,"rb") as f:
# # #             data=pickle.load(f)
# # #             return[student.display() for student in data]
# # #     else:
# # #         print("file not exist")
# # #         return[]
    
# # # def search_student(serch_el):
# # #     if os.path.exists(file_name):
# # #         #serch_el=input("Enter seach student name")
# # #         l=[]
# # #         with open(file_name,"rb") as f:
# # #             data=pickle.load(f)
# # #            # return[student.display() for student in data]
# # #             for i in data:
# # #                 if i.name==serch_el:
# # #                     l.append(i)
# # #             if l:
# # #                 return[student.display() for student in l]
# # #             else:
# # #                 print(f"no result found")
# # #                 return []
# # #     else:
# # #         print(f"no file found")
# # #         return []
# # # # def remove_user ():
# # # #     name=input("Enter User you want to delete :- ")
# # # #     if os.path.exists(file_name):
# # # #         #serch_el=input("Enter seach student name")
# # # #         l=[]
# # # #         with open(file_name,"rb") as f:
# # # #             data=list(pickle.load(f))
# # # #             for i in data:

# # # #     else:
# # # #         print(f"no file found")
# # # #         return []


# # # if __name__=="__storage__":
# # #     print("student in storage")
# # #     print(load_students())
        

# # import os
# # import pickle

# # file_name = "student.pkl"

# # def save_student(s):
# #     students = []
# #     if os.path.exists(file_name):
# #         with open(file_name, "rb") as f:
# #             students = pickle.load(f)
# #     students.append(s)
# #     with open(file_name, "wb") as f:
# #         pickle.dump(students, f)

# # def load_students():
# #     if os.path.exists(file_name):
# #         with open(file_name, "rb") as f:
# #             data = pickle.load(f)
# #             return [f"Name: {student.name}, Age: {student.age}" for student in data]
# #     return []

# # def search_student(search_name):
# #     if os.path.exists(file_name):
# #         with open(file_name, "rb") as f:
# #             data = pickle.load(f)
# #             return [f"Name: {s.name}, Age: {s.age}" for s in data if s.name.lower() == search_name.lower()]
# #     return []



# import pickle
# import os

# FILE = "student.pkl"

# def save_student(student):
#     students = load_students()
#     students.append(student)
#     with open(FILE, "wb") as f:
#         pickle.dump(students, f)

# def load_students():
#     if os.path.exists(FILE):
#         with open(FILE, "rb") as f:
#             return pickle.load(f)
#     return []

# def search_student(name):
#     students = load_students()
#     results = [s for s in students if s.name.lower() == name.lower()]
#     return results   # 🔹 Ab return karega


import pickle
import os
from student import student

def save_student(student_obj):
    """Save a student object to a file."""
    students = load_students()
    students.append(student_obj)
    with open("students.dat", "wb") as file:
        pickle.dump(students, file)

def load_students():
    """Load all students from a file."""
    if not os.path.exists("students.dat"):
        return []
    try:
        with open("students.dat", "rb") as file:
            return pickle.load(file)
    except:
        return []

def search_student(query):
    """Search for students by name (case-insensitive)."""
    students = load_students()
    query = query.lower()
    return [s for s in students if query in s.name.lower()]

def delete_student(name):
    """Delete a student by name (case-insensitive)."""
    students = load_students()
    name = name.lower()
    updated_students = [s for s in students if s.name.lower() != name]
    with open("students.dat", "wb") as file:
        pickle.dump(updated_students, file)