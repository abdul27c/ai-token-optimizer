
"""Deterministic prompt optimization and instruction-preservation checks."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class OptimizationResult:
    original_prompt: str
    optimized_prompt: str
    original_words: int
    optimized_words: int
    removed_phrases: tuple[str, ...]

    @property
    def words_saved(self) -> int:
        return self.original_words - self.optimized_words

    @property
    def reduction_percent(self) -> float:
        if self.original_words == 0:
            return 0.0
        return round(self.words_saved / self.original_words * 100, 2)


# Conservative phrase substitutions. These are rules, not an AI model.
REPLACEMENTS = (
    (r"\bin order to\b", "to"),
    (r"\bdue to the fact that\b", "because"),
    (r"\bat this point in time\b", "now"),
    (r"\bfor the purpose of\b", "for"),
    (r"\bin the event that\b", "if"),
    (r"\bhas the ability to\b", "can"),
    (r"\bis able to\b", "can"),
    (r"\ba large number of\b", "many"),
    (r"\bthe majority of\b", "most"),
    (r"\bfor the reason that\b", "because"),
)


def word_count(text: str) -> int:
    """Count whitespace-separated words in a prompt."""
    return len(text.split())


def optimize_prompt(prompt: str) -> OptimizationResult:
    """Apply conservative wording rules and report what changed."""
    if not isinstance(prompt, str):
        raise TypeError("Prompt must be a string.")

    optimized = prompt
    removed_phrases: list[str] = []

    for pattern, replacement in REPLACEMENTS:
        updated, count = re.subn(
            pattern, replacement, optimized, flags=re.IGNORECASE
        )
        if count:
            removed_phrases.append(
                f"{pattern}: {count} replacement(s) with '{replacement}'"
            )
            optimized = updated

    # Normalize extra spaces created by substitutions without changing
    # punctuation, line breaks, or the actual task instructions.
    optimized = re.sub(r"[ \t]+", " ", optimized).strip()

    return OptimizationResult(
        original_prompt=prompt,
        optimized_prompt=optimized,
        original_words=word_count(prompt),
        optimized_words=word_count(optimized),
        removed_phrases=tuple(removed_phrases),
    )


def required_terms_preserved(
    original_prompt: str, optimized_prompt: str
) -> bool:
    """Check that important literal terms from the original remain present.

    This basic check is case-insensitive. It does not prove semantic
    equivalence or guarantee that a model will produce the same answer.
    """
    terms = re.findall(r"\b[A-Z][A-Z0-9_-]{1,}\b", original_prompt)
    optimized_lower = optimized_prompt.lower()
    return all(term.lower() in optimized_lower for term in terms)
