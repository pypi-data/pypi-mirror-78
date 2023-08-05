import os
import click
import webtree.template

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('Provide scrape Command')
    elif ctx.invoked_subcommand == 'scrape':
        click.echo('Invoked %s' % ctx.invoked_subcommand)
    elif ctx.invoked_subcommand == 'clean':
        click.echo('Invoked %s' % ctx.invoked_subcommand)

@cli.command()
@click.option('--site', default='https://www.google.com', help='Enter URL to scrape')
def scrape(site):
  out = webtree.template.base_template
  out = out + """
if __name__ == '__main__':
    init_global_variables("""+'\''+site+'\''+""")
    app.run_server(debug=True)
  """
  with open('app.py','w') as f:
    f.write("newline = '\\n'\n")
    f.write(out.strip('\n'))

  os.system('python app.py')

@cli.command()
def clean():
  os.system('rm app.py')

if __name__ == '__main__':
    cli()