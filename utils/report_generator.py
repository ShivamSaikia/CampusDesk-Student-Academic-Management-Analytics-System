from datetime import datetime
from utils.file_manager import ensure_dir

def generate_html_report(students, marks, attendance, filename="reports/student_report.html"):
    ensure_dir("reports")
    rows_students = "".join(
        f"<tr><td>{s[0]}</td><td>{s[1]}</td><td>{s[2]}</td><td>{s[3]}</td><td>{s[4]}</td></tr>"
        for s in students
    )
    rows_marks = "".join(
        f"<tr><td>{m[0]}</td><td>{m[1]}</td><td>{m[6]:.2f}</td><td>{m[7]}</td></tr>"
        for m in marks
    )
    rows_att = "".join(
        f"<tr><td>{a[0]}</td><td>{a[1]}</td><td>{a[2]}</td><td>{a[3]}</td><td>{a[4]:.2f}%</td></tr>"
        for a in attendance
    )
    html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>CampusDesk Report</title>
<style>
body{{font-family:Arial;margin:30px}} table{{border-collapse:collapse;width:100%;margin-bottom:25px}}
th,td{{border:1px solid #bbb;padding:8px;text-align:left}} th{{background:#eee}}
</style></head><body>
<h1>CampusDesk Academic Report</h1>
<p>Generated: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}</p>
<h2>Students</h2><table><tr><th>ID</th><th>Name</th><th>Email</th><th>Course</th><th>Semester</th></tr>{rows_students}</table>
<h2>Marks</h2><table><tr><th>ID</th><th>Subject</th><th>Total</th><th>Grade</th></tr>{rows_marks}</table>
<h2>Attendance</h2><table><tr><th>ID</th><th>Subject</th><th>Total</th><th>Attended</th><th>Percentage</th></tr>{rows_att}</table>
</body></html>"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    return filename
