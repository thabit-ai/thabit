# Thabit

Evaluate multiple LLM models with the same data to determine which one is better for your use case.

## How to run

```shell
pip3 install thabit
```

## Test

```shell
pytest tests
```

## Build

```shell
pip3 install -e .
```

## Contribute

## Docs

## TODO:

- Validate the input dataset.
- UI for adding/editing config.
- Visulaise Output (using UI).
- Run eval per dataset (add folders for dataset and for evals).
  This is to simplify visualising results later using the UI.

  ```
  root
  ├── datasets
  │ └── a
  └── evals
    └── a
  ```
