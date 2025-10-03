# db_wrapper.py
import sqlite3
import pandas as pd

class DBWrapper:
    def __init__(self, db_path="students.db"):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def fetch_df(self, sql, params=None):
        conn = self._connect()
        df = pd.read_sql_query(sql, conn, params=params or {})
        conn.close()
        return df

    def fetch_all(self, sql, params=None):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(sql, params or [])
        rows = cursor.fetchall()
        conn.close()
        return rows

    def execute(self, sql, params=None):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(sql, params or [])
        conn.commit()
        conn.close()

    # Helper to get eligible students with dynamic criteria
    def get_eligible_students(self, criteria: dict):
        """
        criteria: dict with keys optional:
         - problems_solved_min
         - latest_project_score_min
         - mock_interview_min
         - communication_min
         - internships_min
         - enrollment_years (list)
         - batch_names (list)
         - city (list)
        """
        where_clauses = []
        params = {}

        if "problems_solved_min" in criteria:
            where_clauses.append("p.problems_solved >= :problems_solved_min")
            params["problems_solved_min"] = criteria["problems_solved_min"]
        if "latest_project_score_min" in criteria:
            where_clauses.append("p.latest_project_score >= :latest_project_score_min")
            params["latest_project_score_min"] = criteria["latest_project_score_min"]
        if "mock_interview_min" in criteria:
            where_clauses.append("pl.mock_interview_score >= :mock_interview_min")
            params["mock_interview_min"] = criteria["mock_interview_min"]
        if "communication_min" in criteria:
            where_clauses.append("s.communication >= :communication_min")
            params["communication_min"] = criteria["communication_min"]
        if "internships_min" in criteria:
            where_clauses.append("pl.internships_completed >= :internships_min")
            params["internships_min"] = criteria["internships_min"]
        if "enrollment_years" in criteria and criteria["enrollment_years"]:
            where_clauses.append("students.enrollment_year IN ({})".format(
                ",".join([str(int(y)) for y in criteria["enrollment_years"]])
            ))
        if "batch_names" in criteria and criteria["batch_names"]:
            batch_list = ",".join([f"'{b}'" for b in criteria["batch_names"]])
            where_clauses.append(f"students.course_batch IN ({batch_list})")
        if "city" in criteria and criteria["city"]:
            city_list = ",".join([f"'{c}'" for c in criteria["city"]])
            where_clauses.append(f"students.city IN ({city_list})")

        where = " AND ".join(where_clauses) if where_clauses else "1=1"

        sql = f"""
        SELECT
            students.student_id,
            students.name,
            students.age,
            students.gender,
            students.email,
            students.phone,
            students.enrollment_year,
            students.course_batch,
            students.city,
            students.graduation_year,
            p.language,
            p.problems_solved,
            p.assessments_completed,
            p.mini_projects,
            p.certifications_earned,
            p.latest_project_score,
            s.communication,
            s.teamwork,
            s.presentation,
            s.leadership,
            s.critical_thinking,
            s.interpersonal_skills,
            pl.mock_interview_score,
            pl.internships_completed,
            pl.placement_status,
            pl.company_name,
            pl.placement_package,
            pl.interview_rounds_cleared,
            pl.placement_date
        FROM students
        JOIN programming p ON students.student_id = p.student_id
        JOIN soft_skills s ON students.student_id = s.student_id
        JOIN placements pl ON students.student_id = pl.student_id
        WHERE {where}
        ORDER BY students.student_id
        LIMIT 1000
        """
        return self.fetch_df(sql, params)
