import uuid
import click

@click.group()
def main():
    pass

@main.command()
def key():
    click.echo(uuid.uuid4())
