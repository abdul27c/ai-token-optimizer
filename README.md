# AI Token Optimizer

A Python-based prompt optimization and evaluation tool that reduces unnecessary wording, measures token usage, and estimates input-token cost differences.

## Overview

The AI Token Optimizer applies deterministic text-reduction rules to prompts and evaluates the resulting token counts using `tiktoken`. It includes a command-line interface, configurable input-cost estimates, a repeatable benchmark dataset, and automated tests.

The initial implementation focuses on a transparent, testable baseline before introducing model-powered optimization.

## Features

- Rule-based prompt optimization using conservative phrase substitutions
- Token counting with `tiktoken`
- Estimated input-token cost comparison using a configurable price
- Word-count and token-reduction reporting
- Repeatable benchmark runner with JSON results
- Automated unit tests for optimization, cost calculations, and benchmark consistency
- No API key required for the current baseline

## Technology Stack

- Python
- `tiktoken`
- `unittest`
- JSON
- Git and GitHub

## Project Structure

```text
ai-token-optimizer/
├── src/
│   ├── optimizer.py
│   ├── evaluator.py
│   ├── cli.py
│   └── benchmark.py
├── tests/
│   ├── test_optimizer.py
│   ├── test_evaluator.py
│   └── test_benchmark.py
├── sample-data/
│   └── benchmark_prompts.json
├── docs/
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### Requirements

- Python 3
- pip

### Install

```bash
git clone https://github.com/abdul27c/ai-token-optimizer.git
cd ai-token-optimizer

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Optimize a prompt

```bash
python -m src.cli --prompt "In order to analyze AWS costs, I am able to review a large number of records at this point in time." --price 2.0
```

The command displays the original and optimized prompts, word counts, token counts, reduction percentage, and estimated input-cost differences.

The `--price` argument is an assumed input-token price in USD per million tokens. Update it to the applicable model's current price when making a real estimate.

### Run the benchmark

```bash
python -m src.benchmark
```

The benchmark evaluates the sample dataset and writes a detailed report to `sample-data/benchmark_results.json`.

### Run tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Initial Benchmark

The initial five-prompt sample produced these results:

| Metric | Result |
|---|---:|
| Prompts evaluated | 5 |
| Original tokens | 102 |
| Optimized tokens | 76 |
| Tokens saved | 26 |
| Overall token reduction | 25.49% |

These figures describe the included sample dataset only. They are not a production benchmark or a guarantee of savings on other prompts.

## How It Works

1. The optimizer applies a fixed set of phrase substitutions.
2. The evaluator counts tokens before and after optimization.
3. A configurable price is used to estimate input-token cost.
4. The benchmark runs the same optimization against a fixed JSON dataset.
5. Automated tests check core behavior and benchmark consistency.

## Limitations

- Optimization is deterministic and rule-based; it does not currently call an LLM.
- Token counts use the selected `tiktoken` encoding, which may not match every model's tokenizer.
- Cost estimates cover input tokens only and use a user-supplied price.
- The current benchmark measures token reduction, not response quality, semantic equivalence, latency, or actual API spending.
- Literal-term preservation checks do not prove that the original intent has been preserved.

## Roadmap

- Add model-powered prompt optimization behind an optional API integration.
- Evaluate output quality against defined tasks and expected results.
- Compare token usage, estimated cost, latency, and quality across prompt versions.
- Expand the benchmark dataset with more prompt types and edge cases.
- Add continuous integration through GitHub Actions.

## Author

Built as a portfolio project exploring prompt engineering, tokenization, software testing, and cost-aware AI application development.
