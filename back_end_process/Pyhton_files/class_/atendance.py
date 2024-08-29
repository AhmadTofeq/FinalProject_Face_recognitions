import json
from sqlalchemy import text
from app import db
from flask_sqlalchemy import SQLAlchemy
class atendance :

    def send_json_to_db(self,file_path):
        # Read JSON data from the file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Convert JSON object to a JSON string
        json_data = json.dumps(data)

        # Define the SQL for calling the stored procedure
        sql = "CALL insert_attendances_batch(:jsonData)"

        # Execute the stored procedure with JSON data
        try:
            db.session.execute(
                text(sql),
                {'jsonData': json_data}
            )
            db.session.commit()  # Commit the transaction
            print(f"Inserted {len(data)} records successfully.")
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            print(f"An error occurred: {e}")

    def delete_attendance_by_staff(self,staff_id):
        # Define the SQL for calling the stored procedure
        sql = "CALL delete_attendance_by_staff(:staffId)"

        try:
            # Execute the stored procedure with the staff_id parameter
            db.session.execute(
                text(sql),
                {'staffId': staff_id}
            )
            db.session.commit()  # Commit the transaction
            print(f"Attendance records for staff ID {staff_id} deleted successfully.")
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            print(f"An error occurred: {e}")

    def insert_attendance(self,date_time_atendance, id_staff, id_presntation, case_atendance):
        # Define the SQL for calling the stored procedure
        sql = """
        CALL insert_attendance(:p_date_time_atendance, :p_id_staff, :p_id_presntation, :p_case_atendance)
        """

        try:
            # Execute the stored procedure with the parameters
            db.session.execute(
                text(sql),
                {
                    'p_date_time_atendance': date_time_atendance,
                    'p_id_staff': id_staff,
                    'p_id_presntation': id_presntation,
                    'p_case_atendance': case_atendance
                }
            )
            db.session.commit()  # Commit the transaction
            print("Attendance record inserted successfully.")
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            print(f"An error occurred: {e}")
#
# if __name__ == '__main__':
#     atendance1=atendance()
#     atendance1.send_json_to_db(r"F:\final_project\main\FinalProject_Face_recognitions_fork\json_files\Presentation_14.json")