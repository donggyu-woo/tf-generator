---
name: add-account
description: Add a new AWS account to config/accounts.yaml and regenerate the Terraform files with generate.py. Use when the user asks to add an account, onboard an account, or register a new account.
argument-hint: <alias> <account-id> <email> <env> [groups...]
disable-model-invocation: true
---

# Add a new account

Input: $ARGUMENTS

## 1. Collect the information

The required fields are listed below. Do not guess a value that is missing from the input; ask the user for it.

| Field | Description | Example |
| --- | --- | --- |
| alias | Account alias | example-dev |
| id | 12-digit AWS account ID | "444444444444" |
| email | Root email of the account | example+dev@example.com |
| env | Environment | dev |
| region | Default region (ap-northeast-2 if omitted) | ap-northeast-2 |
| groups | Groups defined in config/groups.yaml | [baseline] |

## 2. Check AWS Organizations

The new account's information must be identical to what is registered in AWS Organizations. Depending on the service, the generated Terraform may not work if the account information is wrong.

First ask the user whether the values were already checked against AWS Organizations. If they were, skip the rest of this step.

Otherwise, give the user the command below with the given id filled in, and ask them to run it and confirm the result. Never run this command yourself, even if the user cannot run it.

Leave `<profile-name>` as is for the user to replace with a profile of the Organizations management account or a delegated administrator account. They can drop `--profile <profile-name>` if their default credentials are already for that account.

```sh
aws --profile <profile-name> organizations describe-account --account-id <account-id>
```

- The account exists in Organizations and its status is ACTIVE.
- The alias, id and email exactly match the Name, Id and Email returned.

If the user reports a difference, do not fix it on your own. Confirm with the user which value to use.

## 3. Validate

If any check fails, do not modify any file and tell the user.

- The id is a 12-digit number.
- The alias and id do not already exist in config/accounts.yaml.
- Every value in groups is defined in config/groups.yaml.

## 4. Edit

Append the account to the end of the `accounts` list in config/accounts.yaml, in the same format as the existing entries.

- Always write the id as a quoted string.
- Leave one blank line between entries.
- Do not touch the existing entries.

## 5. Generate

```sh
uv run generate.py
```

If it fails, report the error as is and stop. Do not modify templates or other configuration to work around the error.

## 6. Report

Summarize the changed and generated files with `git status` and `git diff --stat`.

Do not run terraform plan/apply or git commit/push.

## Examples

Invocation:

```
/add-account example-dev 444444444444 example+dev@example.com dev baseline
```

Entry added to config/accounts.yaml:

```yaml
  - alias: example-dev
    id: "444444444444"
    email: example+dev@example.com
    env: dev
    region: ap-northeast-2
    groups: [baseline]
```

With more than one group:

```
/add-account example-audit 555555555555 example+audit@example.com audit baseline security
```

```yaml
  - alias: example-audit
    id: "555555555555"
    email: example+audit@example.com
    env: audit
    region: ap-northeast-2
    groups: [baseline, security]
```
