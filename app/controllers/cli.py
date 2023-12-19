import click
from app.controllers.schema.init_schema import init_schema
from app.controllers.manager.ImportData import ImportData

@click.group()
def cli():
    """Main command group for FigAGI."""
    pass

@cli.command()
@click.option(
    "--model",
    default="gpt-3.5-turbo",
    help="OpenAI Model name to initialize. (default gpt-3.5-turbo)",
)
def init(model):
    """
    Initialize schemas
    """
    init_schema(model=model)

@cli.command()
@click.option(
    "--model",
    default="gpt-3.5-turbo",
    help="OpenAI Model name to initialize. (default gpt-3.5-turbo)",
)
def clear_all_command(model):
    init_schema(model=model)


@cli.command()
@click.option(
    "--path",
    default="./data",
    help="Path to data directory",
)
@click.option(
    "--model",
    default="gpt-3.5-turbo",
    help="OpenAI Model name to initialize. (default gpt-3.5-turbo)",
)
@click.option(
    "--clear",
    default=False,
    help="Remove all existing data before ingestion",
)
def import_data_command(path, model, clear):
    if clear:
        init_schema(model=model)
    ImportData(path, model)
