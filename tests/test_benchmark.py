
import json
import unittest
from pathlib import Path

from src.evaluator import evaluate_prompts
from src.optimizer import optimize_prompt


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "sample-data" / "benchmark_prompts.json"


class TestBenchmarkDataset(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with DATASET_PATH.open(encoding="utf-8") as file:
            cls.prompts = json.load(file)

    def test_dataset_has_five_prompts(self):
        self.assertEqual(len(self.prompts), 5)

    def test_each_prompt_has_required_fields(self):
        for item in self.prompts:
            with self.subTest(prompt_id=item.get("id")):
                self.assertTrue(item.get("id"))
                self.assertTrue(item.get("category"))
                self.assertIsInstance(item.get("prompt"), str)
                self.assertTrue(item["prompt"].strip())

    def test_benchmark_results_are_reproducible(self):
        for item in self.prompts:
            with self.subTest(prompt_id=item["id"]):
                first = optimize_prompt(item["prompt"])
                second = optimize_prompt(item["prompt"])
                self.assertEqual(first.optimized_prompt, second.optimized_prompt)

    def test_token_counts_match_optimized_prompts(self):
        for item in self.prompts:
            with self.subTest(prompt_id=item["id"]):
                optimized = optimize_prompt(item["prompt"])
                result = evaluate_prompts(
                    item["prompt"],
                    optimized.optimized_prompt,
                    input_price_per_million=2.0,
                )
                self.assertGreaterEqual(result.original_tokens, 0)
                self.assertGreaterEqual(result.optimized_tokens, 0)
                self.assertEqual(
                    result.tokens_saved,
                    result.original_tokens - result.optimized_tokens,
                )


if __name__ == "__main__":
    unittest.main()
