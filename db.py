import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_equipment(self):
        sql = """
        CREATE TABLE Equipment (
            name string NOT NULL,
            serial_number str NOT NULL,
            type str,
            date str,
            location str,
            condition str,
            description str,
            PRIMARY KEY (serial_number)
            );
"""
        self.execute(sql, commit=True)

    def create_table_work_log(self):
        sql = """
        CREATE TABLE WorkLog (
            id int NOT NULL,
            date str NOT NULL,
            type str,
            description str,
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    def create_table_locations(self):
        sql = """
        CREATE TABLE Locations (
            City     STRING,
            Object   STRING,
            Building STRING,
            Room     STRING
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_equipment(self, name: str, serial_number: str, type: str,
                      date: str, location: str, condition: str, description: str):
        sql = """
        INSERT INTO Equipment(name, serial_number, type, date, 
        location, condition, description) VALUES(?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(name, serial_number, type, date,
                                      location, condition, description), commit=True)

    def select_all_equipment(self):
        sql = """
        SELECT * FROM Equipment
        """
        return self.execute(sql, fetchall=True)

    def select_equipment(self, **kwargs):
        sql = "SELECT * FROM Equipment WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def update_equipment(self, serial_number, date, location, condition, description):
        sql = f"""
        UPDATE Equipment SET date=?, location=?, condition=?, description=? WHERE serial_number=?
        """
        return self.execute(sql, parameters=(date, location, condition,
                                             description, serial_number), commit=True)

    def delete_equipment(self, serial_number):
        sql = f"DELETE FROM Equipment WHERE serial_number=?"
        return self.execute(sql, parameters=(serial_number,), commit=True)

    def clear_all_equipment(self):
        sql = f"DELETE FROM Equipment"
        return self.execute(sql, commit=True)


    def add_work_log(self, id: int, name: str, type: str = None, description: str = None):
        sql = """
        INSERT INTO WorkLog(id, date, type, description) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, type, description), commit=True)

    def select_all_work_log(self):
        sql = """
        SELECT * FROM WorkLog
        """
        return self.execute(sql, fetchall=True)

    def select_work_log(self, **kwargs):
        sql = "SELECT * FROM WorkLog WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def update_work_log_description(self, id, description):
        sql = f"""
        UPDATE WorkLog SET description=? WHERE id=?
        """
        return self.execute(sql, parameters=(description, id), commit=True)

    def delete_work_log(self, id):
        sql = f"DELETE FROM WorkLog WHERE id=?"
        return self.execute(sql, parameters=(id,), commit=True)

    def clear_all_work_log(self):
        sql = f"DELETE FROM WorkLog"
        return self.execute(sql, commit=True)

    def select_help_dev(self, text):
        words = {"Тип": "Type", "Место": "Location", "Статус": "condition"}
        sql = f"""
        SELECT {words[text]} FROM Equipment
        """
        return self.execute(sql, fetchall=True)

    def select_help_log(self, text):
        words = {"Дата": "Date", "Место": "Location", "Статус": "condition"}
        sql = f"""
        SELECT {words[text]} FROM WorkLog
        """
        return self.execute(sql, fetchall=True)

    def select_locations(self):
        sql = f"""
                SELECT * FROM Locations
                """
        return self.execute(sql, fetchall=True)

    def add_location(self, city: str, object: str, building: str, room: str):
        locations = [str(i[0]) for i in self.execute("""SELECT * FROM Locations""", fetchall=True)]
        adding_adress = " ".join([city, object, building, room])
        if adding_adress not in locations:
            sql = """
            INSERT INTO Locations(city, object, building, room) VALUES(?, ?, ?, ?)
            """
            self.execute(sql, parameters=(city, object, building, room), commit=True)
            return True
        else:
            return False

    def delete_location(self, city, object, building, room):
        sql = f"DELETE FROM Locations WHERE city=? AND object=? AND building=? AND room=?"
        return self.execute(sql, parameters=(city, object, building, room), commit=True)

    def select_help_location(self):
        sql = f"""
        SELECT * FROM Locations
        """
        return self.execute(sql, fetchall=True)

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
