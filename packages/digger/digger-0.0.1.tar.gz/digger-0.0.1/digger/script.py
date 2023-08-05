import click


@click.group()
def main():
    pass


@click.command(help='run a web server.')
@click.option('--host')
@click.option('--port', type=int)
@click.option('--debug', is_flag=True)
def webserver(host, port, debug):
    from digger.web import app
    app.run(host=host, port=port, debug=debug)


main.add_command(webserver)

if __name__ == '__main__':
    main()
