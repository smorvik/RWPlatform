import unittest
from src.main import get_db_connection

class TestDatabaseFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = get_db_connection()
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_create_questionnaire(self):
        title = "Тестовая анкета"
        description = "Описание тестовой анкеты"
        self.cursor.execute("INSERT INTO Questionnaires (title, description) VALUES (?, ?)", title, description)
        self.conn.commit()

        self.cursor.execute("SELECT * FROM Questionnaires WHERE title = ?", title)
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result.title, title)
        self.assertEqual(result.description, description)

    def test_add_question(self):
        questionnaire_id = 1
        question_text = "Как вы оцениваете условия работы?"

        self.cursor.execute("INSERT INTO Questions (questionnaire_id, text) VALUES (?, ?)", questionnaire_id, question_text)
        self.conn.commit()

        self.cursor.execute("SELECT * FROM Questions WHERE text = ?", question_text)
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result.text, question_text)

    def test_add_answer(self):
        question_id = 1
        response_text = "Доволен"
        rating = 5

        self.cursor.execute("INSERT INTO Answers (question_id, response_text, rating) VALUES (?, ?, ?)", question_id, response_text, rating)
        self.conn.commit()

        self.cursor.execute("SELECT * FROM Answers WHERE response_text = ?", response_text)
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result.response_text, response_text)
        self.assertEqual(result.rating, rating)

if __name__ == "__main__":
    unittest.main()
