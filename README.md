# Cimple Compiler — P4

> 4th semester project @ **Aalborg University**  
> Course: *Design, Definition and Implementation of Programming Languages*

![Python](https://img.shields.io/badge/Python-99%25-blue?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![AAU](https://img.shields.io/badge/AAU-P4%20Project-blue)

---

## What is this?

Welcome to the **Cimple Compiler** — a fully featured compiler for a custom-built programming language called **Cimple**, built from scratch as part of our 4th semester project at Aalborg University.

We designed the language, wrote the grammar, and built the entire compiler pipeline in **Python**:

```
Source Code -> Lexer -> Parser -> AST -> Type Checker -> Code Generation
```

---

## Language Features

Cimple is a simple, statically typed language that supports:

| Feature | Details |
|---|---|
| **Types** | `integer`, `doubleFloatingPoint`, `string`, `boolean`, `void` |
| **Variables & Arrays** | Declaration and assignment |
| **Functions** | With parameters and return values |
| **Control Flow** | `if/else`, `while`, `skip` |
| **Arithmetic** | `+`, `-`, `*`, `/`, `MOD` |
| **Comparisons** | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| **Logic** | `AND`, `OR`, `!` |
| **Function Calls** | With expression-based arguments |
| **Format Strings** | String formatting support |

---

## Project Structure

```
P4/
├── src/                  # Compiler source code
├── tests/                # Test suite
├── documentation/        # Project documentation
├── .github/workflows/    # CI/CD pipelines
├── .devcontainer/        # Dev container config
├── concreteSyntax.txt    # Formal grammar for Cimple
├── Dockerfile            # Docker image definition
├── docker-compose.yaml   # Docker Compose services
├── pyproject.toml        # Python project config
└── requirements.txt      # Python dependencies
```

---

## Getting Started

No local Python setup needed — just **Docker**!

### Prerequisites

- [Docker](https://www.docker.com/) installed and running

### Build & Setup

```
docker compose up
```

### Run the Compiler

```
docker compose up app
```

### Run Tests

```
docker compose up test
```

---

## Grammar (Sneak Peek)

The full concrete syntax is defined in [`concreteSyntax.txt`](concreteSyntax.txt). Here's a taste:

```
Prog     -> FuncDef
FuncDef  -> TYPE IDF (Param,...,Param) { Stm return Exp; } FuncDef | ε
Stm      -> TYPE Def | IDF = Exp | if(Exp){Stm}else{Stm} | while(Exp){Stm} | skip
Exp      -> ExpAnd | ExpOr | ExpAdd | ...
TYPE     -> integer | double | string | boolean | void
```

---

## CI/CD

Every push and pull request is automatically tested and built using **GitHub Actions**. Workflows live in `.github/workflows/`.

---

## Contributors

See all contributors [here](https://github.com/bruun12/P4/graphs/contributors).

---

## License

This project was built for educational purposes at Aalborg University and has not been released under an explicit open source license.
