<div align="center">
  <img src="./docs/assets/img/thabit-logo.png" width="90%" alt=Thabit" />
</div>

<div align="center" style="line-height: 1;">
  <a href="https://thabit.ai" target="_blank" style="margin: 2px;">
    Home Page
  </a>
  &nbsp; | &nbsp;
  <a href="https://docs.thabit.ai" target="_blank" style="margin: 2px;">
    Docs
  </a>
  &nbsp; | &nbsp;
  <a href="https://discord.gg/5XQgnjXQ" target="_blank" style="margin: 2px;">
    Discord
  </a>
</div>

# Thabit

Evaluate multiple LLM models with custom datasets.

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
