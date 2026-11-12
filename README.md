# llm-response-checker

A small Python command line tool that checks an LLM response against a rubric of simple, rule-based checks. It is a demo project showing how structured output and instruction-following can be verified automatically, with tests, a Dockerfile and a CI workflow.

## Features

- `valid_json` - the response must parse as JSON (errors report line and column)
- `required_keys` - the JSON object must contain the listed keys
- `max_words` - the response must stay under a word limit
- `must_include` - listed phrases must appear (case-insensitive)
- `must_not_include` - listed phrases must not appear (case-insensitive)
- Score = share of checks passed; exit code `0` if all pass, `1` otherwise
- No external dependencies (Python 3.10+)

## Usage

```bash
python -m checker.cli --rubric examples/rubric.json --response examples/response_good.json
python -m checker.cli --rubric examples/rubric.json --response examples/response_bad.json
python -m checker.cli --rubric examples/rubric.json --response examples/response_bad.json --json
```

Example output for the bad response:

```
Rubric: Product summary task
  [PASS] valid_json
  [FAIL] required_keys - Missing keys: tags
  [PASS] max_words - 17 words
  [FAIL] must_include - Missing phrases: battery
  [FAIL] must_not_include - Forbidden phrases found: as an ai language model
Score: 0.40 (FAILED)
```

## Rubric format

```json
{
  "name": "Product summary task",
  "checks": {
    "valid_json": true,
    "required_keys": ["title", "summary", "tags"],
    "max_words": 60,
    "must_include": ["battery"],
    "must_not_include": ["as an ai language model"]
  }
}
```

## Run the tests

```bash
python -m unittest discover -v
```

## Run with Docker

```bash
docker build -t llm-response-checker .
docker run --rm llm-response-checker --rubric examples/rubric.json --response examples/response_good.json
```

## Project structure

```
checker/
  checks.py     individual checks
  evaluate.py   runs a rubric and computes the score
  cli.py        command line interface
examples/       sample rubric and responses
tests/          unit tests
.github/workflows/ci.yml   runs the tests on every push
```

## Ideas for extending

- Add a `max_chars` or `regex_match` check
- Support checking a folder of responses and printing a summary table
- Add a weighted score

## License

MIT
