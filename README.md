# tf-generator
A starter kit for managing resources across multiple AWS accounts with Terraform, generated from Jinja2 templates.

## How it works
`generate.py` reads two files in `config/`, then renders the templates in `templates/` once per account into `accounts/`.

### Inputs
`config/accounts.yaml` lists the accounts. Each account names the groups it belongs to:

```yaml
accounts:
  - alias: example-security
    id: "333333333333"
    email: example+security@example.com
    env: security
    region: ap-northeast-2
    groups: [baseline, security]
```

`alias`, `id` and `email` must be identical to the account's name, ID and email in AWS Organizations. The script does not check this.

`config/groups.yaml` maps each group to its `services`. A service is a directory path under `templates/`:

```yaml
groups:
  baseline:
    services:
      - cloudtrail/data
      - firehose

  security:
    services:
      - cloudtrail/management
      - guardduty
```

An account gets every service of every group it belongs to, so `example-security` above gets all four services.

### Rendering
Run the script with [uv](https://docs.astral.sh/uv/), which installs the dependencies on first run:

```bash
uv run generate.py
```

Without uv, install `jinja2` and `pyyaml` and run `python generate.py`.

For each account and each of its services, every `.j2` file directly inside `templates/<service>/` is rendered and written as a `.tf` file with the same name:

```
templates/<service>/<name>.j2  ->  accounts/<env>/<alias>/<region>/<service>/<name>.tf
```

Each `accounts/<env>/<alias>/<region>/<service>/` directory is a standalone Terraform root module with its own backend and state, so you run `terraform` inside it.

Existing files are overwritten on every run. Files are never deleted, so after removing a template, a service or an account, delete its generated output by hand.

## Usage

### Authentication
Terraform does not use per-account credentials. Each generated configuration assumes an IAM role in the target account, so you only need credentials that are allowed to assume that role.

This requires a role to exist in every account listed in `config/accounts.yaml` beforehand. The templates assume it has the same name in every account, so only the account `id` changes in the role ARN:

```hcl
provider "aws" {
  region = "ap-northeast-2"

  assume_role {
    role_arn = "arn:aws:iam::<account-id>:role/SampleAccountProvisioningRole"
  }
}
```

### Role configuration
`SampleAccountProvisioningRole` needs two things in every account.

#### Trust policy
The role must trust the principal you run Terraform as:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "AWS": "<principal-arn>" },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

#### Permissions
Grant only what the generated Terraform files manage in that account.

### Backend permissions
State for every account is stored in a single S3 bucket in the account you manage Terraform from. The `backend "s3"` block does not assume `SampleAccountProvisioningRole`, so these permissions go on the principal you run Terraform as, not on the role.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::<tfstate-bucket>"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::<tfstate-bucket>/*/terraform.tfstate"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::<tfstate-bucket>/*/terraform.tfstate.tflock"
    }
  ]
}
```

Each service of each account has its own state key, so `*` stands for the path between the bucket and the state file, which is `aws/<env>/<alias>/<region>/<service>` (for example `aws/prod/example-prod/ap-northeast-2/cloudtrail/data`).

The permissions on the `.tflock` object are only needed when state locking is enabled with `use_lockfile = true`. See the [S3 backend documentation](https://developer.hashicorp.com/terraform/language/backend/s3) for details.
