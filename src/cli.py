
"""Command-line interface for the AI Token Optimizer."""

import argparse

from src.evaluator import evaluate_prompts
from src.optimizer import optimize_prompt


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Optimize prompt wording and estimate token savings."
    )
    parser.add_argument(
        "--price",
        type=float,
        default=2.0,
        help="Assumed input price in USD per million tokens (default: 2.0).",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="Prompt to optimize. If omitted, you'll be prompted to enter one.",
    )
    args = parser.parse_args()

    prompt = args.prompt
    if prompt is None:
        prompt = input("Enter your prompt: ")

    result = optimize_prompt(prompt)
    evaluation = evaluate_prompts(
        original_prompt=prompt,
        optimized_prompt=result.optimized_prompt,
        input_price_per_million=args.price,
    )

    print("\n=== AI TOKEN OPTIMIZER ===")
    print("\nOriginal prompt:")
    print(prompt)
    print("\nOptimized prompt:")
    print(result.optimized_prompt)

    print("\n=== RESULTS ===")
    print(f"Original words: {result.original_words}")
    print(f"Optimized words: {result.optimized_words}")
    print(f"Original tokens: {evaluation.original_tokens}")
    print(f"Optimized tokens: {evaluation.optimized_tokens}")
    print(f"Tokens saved: {evaluation.tokens_saved}")
    print(f"Token reduction: {evaluation.reduction_percent}%")
    print(f"Estimated original input cost: ${evaluation.original_cost_usd:.8f}")
    print(f"Estimated optimized input cost: ${evaluation.optimized_cost_usd:.8f}")
    print(f"Estimated input savings: ${evaluation.estimated_savings_usd:.8f}")

    if result.removed_phrases:
        print("\nRules applied:")
        for phrase in result.removed_phrases:
            print(f"- {phrase}")
    else:
        print("\nNo optimization rules were triggered.")

    print(
        "\nNote: This baseline uses deterministic wording rules. "
        "Cost estimates use your assumed price and exclude output tokens."
    )


if __name__ == "__main__":
    main()
