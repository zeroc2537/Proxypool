# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxy_pool
   Description :   proxy pool 启动入口
   Author :        JHao
   date：          2020/6/19
-------------------------------------------------
   Change Activity:
                   2020/6/19:
-------------------------------------------------
"""
__author__ = 'JHao'

import click

from helper.launcher import startServer, startScheduler
from setting import BANNER, VERSION

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=VERSION)
def cli():
    """ProxyPool cli工具"""


@cli.command(name="server")
def server():
    """ 启动api服务 """
    click.echo(BANNER)
    startServer()


@cli.command(name="schedule")
def schedule():
    """ 启动调度程序 """
    click.echo(BANNER)
    startScheduler("schedule")


@cli.command(name="check")
def schedule():
    """ 单独执行check """
    click.echo(BANNER)
    startScheduler("check")


@cli.command(name="craw")
def schedule():
    """ 单独执行craw """
    click.echo(BANNER)
    startScheduler("craw")


if __name__ == '__main__':
    cli()
