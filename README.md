<div align="center">
  <img src="./docs/assets/img/thabit-logo.png" width="30%" alt=Thabit" />
</div>

<div align="center" style="line-height: 1;">
  <a href="https://docs.thabit.ai" target="_blank" style="margin: 2px;">
    Docs
  </a>
  &nbsp; | &nbsp;
  <a href="https://discord.gg/5XQgnjXQ" target="_blank" style="margin: 2px;">
    Discord
  </a>
</div>

# Thabit

Open source platform to evaluate multiple LLM models with custom datasets.

## Demo
![demo](https://github.com/user-attachments/assets/cd34047c-d193-4e85-8a2d-77d6bf92a104)


## Installation

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

## Docs

Visit [https://docs.thabit.ai](https://docs.thabit.ai)

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
