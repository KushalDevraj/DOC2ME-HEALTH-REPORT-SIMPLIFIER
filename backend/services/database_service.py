import mysql.connector as mysql
import uuid
import random
from utils import variables, relative_path
from utils.logger import Logger

logger = Logger()

class DatabaseService:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None # Initialize to avoid __del__ errors
        self.cursor = None
        self.mock_mode = False
        self.sqlite_mode = False
        self.data_store = {
            "input": {},
            "output": {},
            "feedback": {}
        }
        
        # PRIORITIZE SQLITE to avoid MySQL timeout latency
        try:
             # Skip MySQL logic intentionally for faster local startup
             raise Exception("Forcing SQLite for local dev performance")
             
             self.conn = mysql.connect(
                host=variables["database_host"],
                user=variables["database_user"],
                password=variables["database_password"],
                database=variables["database_name"]
            )
             self.cursor = self.conn.cursor()
             self.initialize_tables()
             logger.info("Connected to MySQL database successfully.")
        except Exception as e:
            # print(f"Failed to connect to MySQL database: {e}") 
            # logger.info(f"Failed to connect to MySQL database: {e}")
            logger.info("Using SQLite Database for persistence (Performance Mode).")
            import sqlite3
            self.sqlite_mode = True
            sqlite_db = relative_path(f"/data/{variables['database_name']}.sqlite")
            self.conn = sqlite3.connect(sqlite_db, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.initialize_sqlite_tables()
            logger.info(f"Connected to SQLite database at {sqlite_db}")

    def initialize_sqlite_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS input (
                uuid CHAR(36) PRIMARY KEY,
                prompt TEXT
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS output (
                uuid CHAR(36) PRIMARY KEY,
                output TEXT,
                output_type TEXT,
                input_uuid CHAR(36),
                FOREIGN KEY (input_uuid) REFERENCES input(uuid)
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                uuid CHAR(36) PRIMARY KEY,
                feedback TEXT,
                feedback_type TEXT,
                output_uuid CHAR(36),
                FOREIGN KEY (output_uuid) REFERENCES output(uuid)
            )
            """
        )
        self.conn.commit()

    def __del__(self):
        if getattr(self, 'conn', None):
            self.conn.close()
    
    def create_input_table(self):
        if self.mock_mode: return
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS input (
                uuid CHAR(36) PRIMARY KEY,
                prompt TEXT
            )
            """
        )
        self.conn.commit()
    
    def create_output_table(self):
        if self.mock_mode: return
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS output (
                uuid CHAR(36) PRIMARY KEY,
                output TEXT,
                output_type TEXT,
                input_uuid CHAR(36),
                FOREIGN KEY (input_uuid) REFERENCES input(uuid)
            )
            """
        )
        self.conn.commit()
    
    def create_feedback_table(self):
        if self.mock_mode: return
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                uuid CHAR(36) PRIMARY KEY,
                feedback TEXT,
                feedback_type TEXT,
                output_uuid CHAR(36),
                FOREIGN KEY (output_uuid) REFERENCES output(uuid)
            )
            """
        )
        self.conn.commit()
    
    def initialize_tables(self):
        if self.mock_mode: return
        try:
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()
            if not tables:
                self.create_input_table()
                self.create_output_table()
                self.create_feedback_table()
        except mysql.Error as err:
            logger.error(f"Error initializing tables: {err}")
    
    def generate_uuid(self):
        return str(uuid.uuid4())
    
    def insert_input(self, prompt):
        uuid_str = self.generate_uuid()
        if self.mock_mode:
            self.data_store["input"][uuid_str] = {"uuid": uuid_str, "prompt": prompt}
            return uuid_str
        
        placeholder = "?" if self.sqlite_mode else "%s"
        query = f"INSERT INTO input (uuid, prompt) VALUES ({placeholder}, {placeholder})"
        self.cursor.execute(query, (uuid_str, prompt))
        self.conn.commit()
        return uuid_str
    
    def insert_output(self, input_uuid, output, output_type):
        output_uuid = self.generate_uuid()
        if self.mock_mode:
            self.data_store["output"][output_uuid] = {
                "uuid": output_uuid,
                "output": output,
                "output_type": output_type,
                "input_uuid": input_uuid
            }
            return output_uuid
            
        placeholder = "?" if self.sqlite_mode else "%s"
        query = f"INSERT INTO output (uuid, output, output_type, input_uuid) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})"
        self.cursor.execute(query, (output_uuid, output, output_type, input_uuid))
        self.conn.commit()
        return output_uuid
    
    def insert_feedback(self, output_uuid, feedback, feedback_type):
        feedback_uuid = self.generate_uuid()
        if self.mock_mode:
            self.data_store["feedback"][feedback_uuid] = {
                "uuid": feedback_uuid,
                "feedback": feedback,
                "feedback_type": feedback_type,
                "output_uuid": output_uuid
            }
            return feedback_uuid

        placeholder = "?" if self.sqlite_mode else "%s"
        query = f"INSERT INTO feedback (uuid, feedback, feedback_type, output_uuid) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})"
        self.cursor.execute(query, (feedback_uuid, feedback, feedback_type, output_uuid))
        self.conn.commit()
        return feedback_uuid

    def get_output(self, output_uuid):
        if self.mock_mode:
            data = self.data_store["output"].get(output_uuid)
            return (data["output"],) if data else None

        placeholder = "?" if self.sqlite_mode else "%s"
        query = f"SELECT output FROM output WHERE uuid = {placeholder}"
        self.cursor.execute(query, (output_uuid,))
        return self.cursor.fetchone()
    
    def get_output_from_input(self, input_uuid):
        if self.mock_mode:
            for item in self.data_store["output"].values():
                if item["input_uuid"] == input_uuid:
                    # Return tuple matching SQL fetchone structure: (uuid, output, output_type, input_uuid)
                    return (item["uuid"], item["output"], item["output_type"], item["input_uuid"])
            return None

        placeholder = "?" if self.sqlite_mode else "%s"
        query = f"SELECT * FROM output WHERE input_uuid = {placeholder}"
        self.cursor.execute(query, (input_uuid,))
        return self.cursor.fetchone()
    
    def get_output_record(self, output_uuid):
        if self.mock_mode:
            return self.data_store["output"].get(output_uuid)
            
        placeholder = "?" if self.sqlite_mode else "%s"
        query = f"SELECT * FROM output WHERE uuid = {placeholder}"
        self.cursor.execute(query, (output_uuid,))
        return self.cursor.fetchone()

    def get_input(self, input_uuid):
        if self.mock_mode:
            data = self.data_store["input"].get(input_uuid)
            return (data["prompt"],) if data else None

        placeholder = "?" if self.sqlite_mode else "%s"
        query = f"SELECT prompt FROM input WHERE uuid = {placeholder}"
        self.cursor.execute(query, (input_uuid,))
        return self.cursor.fetchone()

    def get_random_input(self):
        if self.mock_mode:
            inputs = list(self.data_store["input"].values())
            if not inputs: return None
            item = random.choice(inputs)
            # Return tuple matching SQL fetchone structure: (uuid, prompt)
            return (item["uuid"], item["prompt"])

        order_by = "RANDOM()" if self.sqlite_mode else "RAND()"
        query = f"SELECT * FROM input ORDER BY {order_by} LIMIT 1"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_latest_input(self):
        if self.mock_mode:
            inputs = list(self.data_store["input"].values())
            if not inputs: return None
            # Return tuple matching SQL fetchone structure: (uuid, prompt)
            item = inputs[-1]
            return (item["uuid"], item["prompt"])

        if self.sqlite_mode:
            query = "SELECT * FROM input ORDER BY rowid DESC LIMIT 1"
        else:
            # Fallback for MySQL - since no timestamp, we just take one.
            query = "SELECT * FROM input LIMIT 1" 
        
        self.cursor.execute(query)
        return self.cursor.fetchone()
