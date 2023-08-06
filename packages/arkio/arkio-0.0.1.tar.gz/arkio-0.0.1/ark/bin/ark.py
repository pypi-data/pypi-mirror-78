# -*- coding: utf-8 -*-

import click


@click.command()
@click.option('--x', default=1)
@click.option('--y', default=1)
def div(x, y):
        click.echo('{}/{}={}'.format(x, y, x/y))


def main():
    div()
