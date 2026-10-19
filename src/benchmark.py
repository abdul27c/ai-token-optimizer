
"""Run repeatable benchmarks against a local prompt dataset."""

import json
from pathlib import Path

from src.evaluator import evaluate_prompts
from src.optimizer import optimize_prompt


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    dataset_path = project_root / "sample-data" / "benchmark_prompts.json"

    with dataset_path.open(encoding="utf-8") as file:
        prompts = json.load(file)

    if not isinstance(prompts, list):
        raise ValueError("Benchmark dataset must be a JSON list.")

    results = []
    total_original_tokens = 0
    total_optimized_tokens = 0
    total_saved = 0

    print("AI TOKEN OPTIMIZER — BENCHMARK")
    print("-" * 76)

    for item in prompts:
        if not isinstance(item, dict) or not isinstance(item.get("prompt"), str):
            raise ValueError("Every benchmark item must contain a string prompt.")

        original = item["prompt"]
        optimized = optimize_prompt(original)
        evaluation = evaluate_prompts(
            original_prompt=original,
            optimized_prompt=optimized.optimized_prompt,
            input_price_per_million=2.0,
        )

        total_original_tokens += evaluation.original_tokens
        total_optimized_tokens += evaluation.optimized_tokens
        total_saved += evaluation.tokens_saved

        results.append({
            "id": item.get("id", "unknown"),
            "category": item.get("category", "uncategorized"),
            "original_tokens": evaluation.original_tokens,
            "optimized_tokens": evaluation.optimized_tokens,
            "tokens_saved": evaluation.tokens_saved,
            "reduction_percent": evaluation.reduction_percent,
            "rules_applied": list(optimized.removed_phrases),
        })

        print(
            f"{item.get('id', 'unknown'):12} "
            f"{evaluation.original_tokens:4} -> "
            f"{evaluation.optimized_tokens:4} tokens | "
            f"saved {evaluation.tokens_saved:4} | "
            f"{evaluation.reduction_percent:6.2f}%"
        )

    overall_reduction = (
        total_saved / total_original_tokens * 100
        if total_original_tokens
        else 0.0
    )

    print("-" * 76)
    print(f"Prompts evaluated: {len(results)}")
    print(f"Original tokens: {total_original_tokens}")
    print(f"Optimized tokens: {total_optimized_tokens}")
    print(f"Tokens saved: {total_saved}")
    print(f"Overall token reduction: {overall_reduction:.2f}%")
    print("Note: This benchmark measures token counts, not output quality.")

    output_path = project_root / "sample-data" / "benchmark_results.json"
    output_path.write_text(
        json.dumps({
            "prompts_evaluated": len(results),
            "original_tokens": total_original_tokens,
            "optimized_tokens": total_optimized_tokens,
            "tokens_saved": total_saved,
            "overall_reduction_percent": round(overall_reduction, 2),
            "results": results,
        }, indent=2),
        encoding="utf-8",
    )
    print(f"Detailed results saved to: {output_path}")


if __name__ == "__main__":
    main()
