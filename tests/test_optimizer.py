
import unittest

from src.optimizer import (
    optimize_prompt,
    required_terms_preserved,
    word_count,
)


class TestPromptOptimizer(unittest.TestCase):
    def test_replaces_wordy_phrases(self):
        result = optimize_prompt(
            "In order to use AWS, do this at this point in time."
        )
        self.assertEqual(result.optimized_prompt, "to use AWS, do this now.")
        self.assertGreater(result.words_saved, 0)

    def test_empty_prompt(self):
        result = optimize_prompt("")
        self.assertEqual(result.optimized_prompt, "")
        self.assertEqual(result.reduction_percent, 0.0)

    def test_simple_prompt_remains_unchanged(self):
        prompt = "Summarize this report in three bullet points."
        result = optimize_prompt(prompt)
        self.assertEqual(result.optimized_prompt, prompt)
        self.assertEqual(result.words_saved, 0)

    def test_rejects_non_string_input(self):
        with self.assertRaises(TypeError):
            optimize_prompt(None)

    def test_preserves_required_literal_terms(self):
        original = "Analyze AWS and API costs."
        optimized = "Analyze AWS and API costs."
        self.assertTrue(required_terms_preserved(original, optimized))

    def test_detects_missing_literal_term(self):
        original = "Analyze AWS and API costs."
        optimized = "Analyze cloud and API costs."
        self.assertFalse(required_terms_preserved(original, optimized))

    def test_word_count(self):
        self.assertEqual(word_count("one two three"), 3)
        self.assertEqual(word_count(""), 0)


if __name__ == "__main__":
    unittest.main()
