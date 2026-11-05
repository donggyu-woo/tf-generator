---
name: remove-account
description: Remove an AWS account from config/accounts.yaml, delete its generated Terraform files and regenerate with generate.py. Use when the user asks to remove an account, offboard an account, or unregister an account.
argument-hint: <alias-or-account-id>
disable-model-invocation: true
---

# Remove an account

Input: $ARGUMENTS

## 1. Identify the account

The input is the alias or the 12-digit id of the account. If it is missing, ask the user for it. Do not guess.

Find the entry in config/accounts.yaml whose alias or id matches the input exactly. If none matches, do not modify any file and tell the user.

Show the user the matching entry and the directory generated for it:

```
accounts/<env>/<alias>/
```

## 2. Check the Terraform resources

Removing the account from this repository does not destroy the resources Terraform created in it, and does not delete their state in the S3 backend. Once the generated files are deleted, those resources can no longer be managed from this repository.

List every service directory under `accounts/<env>/<alias>/<region>/` that contains a `backend.tf`, and ask the user whether the resources of each one were already destroyed, or are meant to be kept.

If they were not, give the user the commands below with the directory filled in, and ask them to run them and confirm the result. Never run `terraform destroy` or any other `terraform` command yourself, even if the user cannot run it.

```sh
cd accounts/<env>/<alias>/<region>/<service>
terraform init
terraform destroy
```

If the user does not confirm for every service directory, stop here without modifying any file.

## 3. Confirm

Before changing anything, ask the user to confirm that the entry and the directory shown in step 1 should be removed. Do not proceed without an explicit yes.

## 4. Edit

Remove the entry from the `accounts` list in config/accounts.yaml.

- Remove only that entry and one of the blank lines next to it, so one blank line remains between the other entries.
- Do not touch the other entries.

## 5. Delete the generated files

```sh
rm -rf accounts/<env>/<alias>
```

If `accounts/<env>/` is empty afterwards, remove it as well. Do not delete anything else under `accounts/`.

## 6. Generate

```sh
uv run generate.py
```

If it fails, report the error as is and stop. Do not modify templates or other configuration to work around the error.

## 7. Report

Summarize the changed and deleted files with `git status` and `git diff --stat`.

Remind the user of what this skill leaves to them:

- The state objects under `aws/<env>/<alias>/` in the S3 backend bucket, if they should be deleted.
- The account itself in AWS Organizations, if it should be closed or removed.

Do not delete the state objects, run any `aws` command, or run git commit/push.

## Examples

Invocation by alias:

```
/remove-account example-beta
```

Invocation by id:

```
/remove-account 111111111111
```

Entry removed from config/accounts.yaml:

```yaml
  - alias: example-beta
    id: "111111111111"
    email: example+beta@example.com
    env: beta
    region: ap-northeast-2
    groups: [baseline]
```

Directory deleted:

```
accounts/beta/example-beta/
```
