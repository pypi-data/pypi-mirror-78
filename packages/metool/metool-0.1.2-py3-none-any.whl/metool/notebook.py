import uuid
import click
import datetime
import random
import importlib.resources

@click.group()
def main():
    pass

def gen_ukey():
    return uuid.uuid4()

@main.command()
def ukey():
    click.echo(gen_ukey())

def random_month():
    return random.randint(1, 12)

def random_day():
    return random.randint(1, 29)

def notebook_date(date):
    l = len(date)
    today = datetime.date.today()
    if l < 4:
        d = today
    elif l < 6:
        d = datetime.date(int(date[0:4]), random_month(), random_day())
    else:
        d = datetime.date(int(date[0:4]), int(l[4:6]), int(l[6:8]))
    return d.strftime('%Y-%m-%d')

@main.command()
@click.argument('title')
@click.option('--layout', default='article')
@click.option('--date', default='')
@click.option('--out', default='.')
def create(title, layout, date, out):
    date = notebook_date(date)
    filename = date + ' ' + title + '.md'
    ukey = gen_ukey()
    with open('notebook_tpl.md', 'r') as r:
        tpl = r.read()
    content = str.format(tpl, title=title, layout=layout, ukey=ukey)
    with open(out + '/' + filename, 'w') as w:
        w.write(content)
    click.echo('Successfully create ' + filename)
