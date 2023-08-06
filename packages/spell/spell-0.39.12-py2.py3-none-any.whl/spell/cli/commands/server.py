import click

from spell.cli.utils import HiddenOption

from spell.cli.commands.model_servers import (
    describe,
    logs,
    remove,
    start,
    stop,
    update_custom,
    serve,
    predict,
    healthcheck,
    list_model_servers,
)


@click.group(
    name="server",
    short_help="Manage model servers",
    help="""Manage model servers

             With no subcommand, displays all of your model servers""",
    invoke_without_command=True,
)
@click.option(
    "--raw", help="display output in raw format", is_flag=True, default=False, cls=HiddenOption
)
@click.pass_context
def server(ctx, raw):
    if not ctx.invoked_subcommand:
        client = ctx.obj["client"]
        list_model_servers(client, raw)


server.add_command(describe)
server.add_command(logs)
server.add_command(remove)
server.add_command(start)
server.add_command(stop)
server.add_command(update_custom, name="update")
server.add_command(serve)
server.add_command(predict)
server.add_command(healthcheck)
