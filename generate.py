import os

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(CURRENT_DIR, 'config')
TEMPLATE_DIR = os.path.join(CURRENT_DIR, 'templates')
GENERATED_DIR = os.path.join(CURRENT_DIR, 'accounts')


def validate(accounts: list, groups: dict):
    for key in ('alias', 'id'):
        values = [account[key] for account in accounts]
        for value in sorted(set(values)):
            if values.count(value) > 1:
                raise ValueError(f'Duplicate "{key}" in accounts.yaml: "{value}"')

    for account in accounts:
        for group in account.get('groups', []):
            if group not in groups:
                raise ValueError(f'Unknown group "{group}" for account "{account["alias"]}" in accounts.yaml')

    for group, config in groups.items():
        if not isinstance(config, dict) or not isinstance(config.get('services'), list):
            raise ValueError(f'Missing "services" list for group "{group}" in groups.yaml')  # noqa: TRY004
        for service in config['services']:
            if not isinstance(service, str) or not os.path.isdir(os.path.join(TEMPLATE_DIR, service)):
                raise ValueError(f'Missing directory "templates/{service}" for group "{group}" in groups.yaml')


def generate(account: dict, service: str, context: dict):
    template_dir = os.path.join(TEMPLATE_DIR, service)
    tf_output_dir = os.path.join(GENERATED_DIR, account['env'], account['alias'], account['region'], service)

    os.makedirs(tf_output_dir, exist_ok=True)

    env = Environment(loader=FileSystemLoader(template_dir), undefined=StrictUndefined)
    for template_file in sorted(os.listdir(template_dir)):
        if not template_file.endswith('.j2'):
            continue

        rendered = env.get_template(template_file).render(account=account, service=service, **context)

        filename = template_file.replace('.j2', '.tf')
        with open(os.path.join(tf_output_dir, filename), 'w', encoding='utf-8') as f:
            f.write(rendered)


def main():
    with open(os.path.join(CONFIG_DIR, 'accounts.yaml'), 'r', encoding='utf-8') as f:
        accounts = yaml.safe_load(f)['accounts']
    with open(os.path.join(CONFIG_DIR, 'groups.yaml'), 'r', encoding='utf-8') as f:
        groups = yaml.safe_load(f)['groups']

    validate(accounts=accounts, groups=groups)

    # `alias_safe` keeps hyphens(-) out of terraform identifiers
    for account in accounts:
        account['alias_safe'] = account['alias'].replace('-', '_')

    context = {'accounts': accounts}
    for account in accounts:
        for group in account.get('groups', []):
            for service in groups[group]['services']:
                generate(account=account, service=service, context=context)


if __name__ == '__main__':
    main()
