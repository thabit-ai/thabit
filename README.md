# Thabit

Evaluate multiple LLM models with the same data to determine which one is better for your use case.

## How to run

## Test

```shell
pytest tests
```

## Build

```shell
pip3 install build
```

## Contribute

## Docs

## TODO:

- Add logs.
- Validate the input dataset.
- Move source to files to simplify the codebase.
  - Move evaluators to their own files. Example: Similarity, Exact, Regex, HasWords, DoNotHaveWords.
  - Unit test for all evaluators.
  - Util folder for Validating Dataset, versioning datasets.
- Visualise adding a dataset (using UI to populate).
- Visulaise Output (using UI).
