import click
import uvicorn
import os

from app.controllers.cli import init as init_ingest
from app.controllers.cli import clear_all_command as clear_all
from app.controllers.cli import import_data_command as import_data
from server.web_ui import AgiUIInterface

agikb_interface = AgiUIInterface()
LaunchInterface = agikb_interface.launch_interface()
@click.group()
def cli():
    """Main command group for verba."""
    pass


@cli.command()
@click.option(
    "--model",
    default="gpt-3.5-turbo",
    help="Generative OpenAI model",
)
def start(model):
    """
    Run the FastAPI application.
    """
    os.environ["VERBA_MODEL"] = model
    uvicorn.run("server.api:app", host="0.0.0.0", port=6000, reload=True)


cli.add_command(init_ingest, name="init")
cli.add_command(import_data, name="import")
cli.add_command(LaunchInterface, name="webui")
cli.add_command(clear_all, name="clear")

if __name__ == "__main__":
    cli()
