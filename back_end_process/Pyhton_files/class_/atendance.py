import json
import os
from back_end_process.Pyhton_files.class_.paths import paths1
from sqlalchemy import text
from app import db

from flask_sqlalchemy import SQLAlchemy
class atendance :
    def send_json_to_db(self,file_path):
        # Read JSON data from the file
        self.data_preproccesing(file_path)
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

    def load_json(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
        else:
            data = []
        return data
    def data_preproccesing(self,path_file):
        clean_data = []
        dec_atendas_info = []
        json_data=self.load_json(path_file)
        for staf in json_data:
            id_staff = int(staf['id_staff'])
            # Find the matching item in dec_atendas_info or set it to a default 'NEW' case
            found_item = {}
            for item in dec_atendas_info:
                id_staff = int(staf['id_staff'])
                if item['id_staff'] == id_staff:
                    found_item = item
                    break
            else:
                if len(found_item) == 0:
                    found_item = {"id_staff": "", "case": "NEW"}
            # Check the case of the found item and determine actions
            if staf["case"] == "IN" and found_item["case"] == "OUT":
                # Update case from 'OUT' to 'IN' and append to clean_data
                clean_data.append(staf)
                for i, item in enumerate(dec_atendas_info):
                    if item['id_staff'] == id_staff:
                        dec_atendas_info[i]['case'] = "IN"
                        print(i, item)
                        break
            elif staf["case"] == "OUT" and found_item["case"] == "IN":
                # Update case from 'IN' to 'OUT' and append to clean_data
                clean_data.append(staf)
                for i, item in enumerate(dec_atendas_info):
                    if item['id_staff'] == id_staff:
                        dec_atendas_info[i]['case'] = "OUT"
                        break
            elif found_item["case"] == "NEW":
                # Handle new staff entries, set their case and append to both lists
                clean_data.append(staf)
                dec_atendas_info.append(staf.copy())
        # Save the clean_data to the specified path as JSON
        with open(path_file, 'w') as file:
            json.dump(clean_data, file, indent=4)
#
# if __name__ == '__main__':
#     atendance1=atendance()
#     atendance1.data_preproccesing(r"F:\final_project\main\FinalProject_Face_recognitions_fork\json_files\Presentation_19.json")