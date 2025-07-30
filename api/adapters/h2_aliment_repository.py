from domain.aliment_repository import AlimentRepository
from domain.aliment import Aliment
import jpype
import jaydebeapi
import os
import logging

logger = logging.getLogger(__name__)

class H2AlimentRepository(AlimentRepository):
    '''
    Repository that handles the communication with H2 database.
    '''

    def __init__(self, jar_path="h2-2.2.224.jar"):
        H2_JAR_PATH = os.environ.get("H2_JAR_PATH", "/app/lib/h2.jar")
        logger.debug(f'H2_JAR_PATH:{H2_JAR_PATH}')
        if not jpype.isJVMStarted():
            logger.debug('Starting JVM')
            jpype.startJVM(
                jpype.getDefaultJVMPath(),
                f"-Djava.class.path={H2_JAR_PATH}"
            )
        else:
            logger.debug('JVM already started')
        self.conn = jaydebeapi.connect(
            'org.h2.Driver',
            'jdbc:h2:mem:testdb',
            ['', ''],
            jar_path
        )
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS aliment (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                status BOOLEAN NOT NULL
            )
        """)
        self.conn.commit()

    def get_all(self):
        self.cursor.execute("SELECT id, name, description, status FROM aliment")
        rows = self.cursor.fetchall()
        return [Aliment(*row) for row in rows]

    def get_by_id(self,
                  aliment_id: int) -> Aliment:
        self.cursor.execute('SELECT id, name, description, status FROM aliment where ID = ?',
                            [aliment_id])
        row = self.cursor.fetchone()
        if not row:
            return None
        return Aliment(*row)

    def insert(self,
               aliment: Aliment):
        self.cursor.execute(
            'INSERT INTO aliment (name, description, status) VALUES (?, ?, ?)',
            [aliment.name, aliment.description, aliment.status]
        )
        self.conn.commit()
        self.cursor.execute('SELECT MAX(id) FROM aliment')
        return self.cursor.fetchone()[0]

    def update(self,
               aliment: Aliment):
        self.cursor.execute(
            'UPDATE aliment SET name=?, description=?, status=? WHERE id=?',
            [aliment.name, aliment.description, aliment.status, aliment.id]
        )
        self.conn.commit()

    def delete(self, aliment_id: int):
        self.cursor.execute('DELETE FROM aliment WHERE id=?', [aliment_id])
        self.conn.commit()

    def exists(self, aliment_id):
        self.cursor.execute('SELECT ID FROM aliment WHERE id=?', [aliment_id])
        return self.cursor.fetchone() is not None