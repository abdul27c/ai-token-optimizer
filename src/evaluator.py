
"""Measure prompt token counts and estimate API costs locally."""

from dataclasses import dataclass

import tiktoken


@dataclass(frozen=True)
class EvaluationResult:
    original_tokens: int
    optimized_tokens: int
    tokens_saved: int
    reduction_percent: float
    original_cost_usd: float
    optimized_cost_usd: float
    estimated_savings_usd: float


def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    """Count tokens with a specified tiktoken encoding."""
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")

    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))


def estimate_cost_usd(
    input_tokens: int,
    price_per_million_tokens: float,
) -> float:
    """Estimate input cost using a user-supplied price per million tokens."""
    if input_tokens < 0:
        raise ValueError("Token count cannot be negative.")
    if price_per_million_tokens < 0:
        raise ValueError("Token price cannot be negative.")

    return input_tokens * price_per_million_tokens / 1_000_000


def evaluate_prompts(
    original_prompt: str,
    optimized_prompt: str,
    input_price_per_million: float,
    encoding_name: str = "cl100k_base",
) -> EvaluationResult:
    """Compare token usage and estimated input costs for two prompts."""
    original_tokens = count_tokens(original_prompt, encoding_name)
    optimized_tokens = count_tokens(optimized_prompt, encoding_name)

    tokens_saved = original_tokens - optimized_tokens
    reduction_percent = (
        round(tokens_saved / original_tokens * 100, 2)
        if original_tokens
        else 0.0
    )

    original_cost = estimate_cost_usd(
        original_tokens, input_price_per_million
    )
    optimized_cost = estimate_cost_usd(
        optimized_tokens, input_price_per_million
    )

    return EvaluationResult(
        original_tokens=original_tokens,
        optimized_tokens=optimized_tokens,
        tokens_saved=tokens_saved,
        reduction_percent=reduction_percent,
        original_cost_usd=round(original_cost, 10),
        optimized_cost_usd=round(optimized_cost, 10),
        estimated_savings_usd=round(original_cost - optimized_cost, 10),
    )
