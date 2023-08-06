[![Build Status](https://dev.azure.com/asottile/asottile/_apis/build/status/asottile.yesqa?branchName=master)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=53&branchName=master)
[![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/asottile/asottile/53/master.svg)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=53&branchName=master)

yesqa
=====

A tool (and pre-commit hook) to automatically remove unnecessary `# noqa`
comments, for example: a check that's no longer applicable (say you increased your
max line length), a mistake (`# noqa` added to a line that wasn't failing),
or other code in the file caused it to no longer need a `# noqa` (such as an unused import).

## Installation

`pip install yesqa`


## As a pre-commit hook

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/asottile/yesqa
    rev: v1.2.2
    hooks:
    -   id: yesqa
```

If you need to select a specific version of flake8 and/or run with specific
flake8 plugins, add them to [`additional_dependencies`][0].

[0]: http://pre-commit.com/#pre-commit-configyaml---hooks
