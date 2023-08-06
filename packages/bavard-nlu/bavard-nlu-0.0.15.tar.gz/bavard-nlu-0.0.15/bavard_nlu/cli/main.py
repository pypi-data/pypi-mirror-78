import click

from bavard_nlu.cli.predict import predict
from bavard_nlu.cli.train import train
from bavard_nlu.cli.agent_data_to_tfrec import agent_data_to_tfrecord


@click.group()
def cli():
    pass


cli.add_command(agent_data_to_tfrecord)
cli.add_command(train)
cli.add_command(predict)


def main():
    cli()


if __name__ == '__main__':
    main()
