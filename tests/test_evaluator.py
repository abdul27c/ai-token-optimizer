
import unittest

from src.evaluator import (
    count_tokens,
    estimate_cost_usd,
    evaluate_prompts,
)


class TestEvaluator(unittest.TestCase):
    def test_count_tokens(self):
        self.assertGreater(count_tokens("Hello, world!"), 0)

    def test_estimate_cost(self):
        self.assertAlmostEqual(
            estimate_cost_usd(1000, 2.0),
            0.002,
        )

    def test_rejects_negative_token_count(self):
        with self.assertRaises(ValueError):
            estimate_cost_usd(-1, 2.0)

    def test_rejects_negative_price(self):
        with self.assertRaises(ValueError):
            estimate_cost_usd(100, -2.0)

    def test_evaluation_reports_reduction(self):
        result = evaluate_prompts(
            "In order to complete this task, summarize the report.",
            "To complete this task, summarize the report.",
            input_price_per_million=2.0,
        )
        self.assertGreater(result.tokens_saved, 0)
        self.assertGreater(result.reduction_percent, 0)
        self.assertGreater(result.estimated_savings_usd, 0)

    def test_empty_prompts(self):
        result = evaluate_prompts(
            "", "", input_price_per_million=2.0
        )
        self.assertEqual(result.original_tokens, 0)
        self.assertEqual(result.optimized_tokens, 0)
        self.assertEqual(result.reduction_percent, 0.0)
        self.assertEqual(result.estimated_savings_usd, 0.0)


if __name__ == "__main__":
    unittest.main()
