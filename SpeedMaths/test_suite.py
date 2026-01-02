import unittest
from main import MathEngine

class TestMathEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MathEngine()

    def test_addition_generation(self):
        """Test if addition questions are generated correctly within range"""
        # Level 1
        q = self.engine.generate_question('addition')
        self.assertIn('+', q['question'])
        self.assertTrue(q['answer'].isdigit())
        
        # Test logic
        parts = q['question'].split('+')
        a, b = int(parts[0]), int(parts[1])
        self.assertEqual(int(q['answer']), a + b)

    def test_multiplication_generation(self):
        """Test multiplication logic"""
        q = self.engine.generate_question('multiplication')
        self.assertIn('×', q['question'])
        
        parts = q['question'].split('×')
        a, b = int(parts[0]), int(parts[1])
        self.assertEqual(int(q['answer']), a * b)

    def test_adaptive_difficulty(self):
        """Test if difficulty level changes based on performance"""
        initial_level = self.engine.difficulty_configs['addition']['level']
        
        # Simulate correct answer
        self.engine.update_difficulty('addition', True)
        self.assertEqual(self.engine.difficulty_configs['addition']['level'], initial_level + 1)
        
        # Simulate wrong answer
        self.engine.update_difficulty('addition', False)
        self.assertEqual(self.engine.difficulty_configs['addition']['level'], initial_level)

    def test_percentage_generation(self):
        """Test percentage question formatting"""
        q = self.engine.generate_question('percentages')
        # Should be fraction or percentage question
        is_fraction = "/" in q['answer']
        is_val = q['answer'].replace('.', '', 1).isdigit()
        self.assertTrue(is_fraction or is_val)

    def test_blitz_mode_logic(self):
        """Blitz mode just uses standard generation but unlimited, verifies engine supports this"""
        # Ensure repeated calls work
        for _ in range(100):
            q = self.engine.generate_question('subtraction')
            self.assertIsNotNone(q)

if __name__ == '__main__':
    unittest.main()
