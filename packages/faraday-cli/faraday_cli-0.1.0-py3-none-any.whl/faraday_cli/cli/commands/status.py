import click
from faraday_cli.config import active_config
from tabulate import tabulate


@click.command(help="Show Cli status")
def status():
    click.secho("Faraday Cli - Status\n", fg="green")
    data = [
        {
            "faraday_url": active_config.faraday_url,
            "token": f"{active_config.token[:10]}..."
            if active_config.token
            else "NO TOKEN",
            "ssl_verify": active_config.ssl_verify,
        }
    ]
    click.secho(tabulate(data, headers="keys"), fg="green")
    click.echo("\n")
    data = [{"workspace": active_config.workspace}]
    click.secho(tabulate(data, headers="keys"), fg="green")
