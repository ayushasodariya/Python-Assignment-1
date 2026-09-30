n, k, m = map(int, input().split())

students = []
semesters = {}

for _ in range(n):
    data = input().split()
    enrollment = data[0]
    name = data[1]
    semester = int(data[2])
    cpi = float(data[3])
    marks = list(map(int, data[4:]))

    avg = sum(marks) / m
    student = (enrollment, name, semester, cpi, marks, avg)

    students.append(student)
    semesters.setdefault(semester, []).append(student)

# Top K students for each semester
for sem in sorted(semesters):
    top = sorted(
        semesters[sem],
        key=lambda x: (-x[3], -x[5], x[0])
    )[:k]

    print(f"Semester {sem}:", *[s[0] for s in top])

# Subject-wise toppers
for i in range(m):
    highest = max(s[4][i] for s in students)
    toppers = sorted(s[0] for s in students if s[4][i] == highest)
    print(f"S{i + 1}:", *toppers)