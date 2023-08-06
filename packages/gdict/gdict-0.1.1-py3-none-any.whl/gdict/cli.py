from enum import auto, Enum
import urllib
from lxml import etree

import requests
import click


class Opt(Enum):
    default = auto()
    version = auto()
    author = auto()


def __search(word):
    request = __query(word)
    html = etree.HTML(request.text)
    result_content = html.xpath('//div[@id="results-contents"]')[0]
    name = result_content.xpath('//h2[@class="wordbook-js"]/span[@class="keyword"]')[0].text
    zh_means = [i.text for i in result_content.xpath('//div[@class="trans-container"]/ul/li') if i.text != '\n\t\t']
    en_means = [i.text for i in html.xpath('//*[@id="tEETrans"]/div/ul/li//span[@class="def"]')]
    return name, zh_means, en_means


def __query(word):
    youdao_url = 'http://dict.youdao.com/search?q=%GDWORD%&ue=utf8'
    url = youdao_url.replace('%GDWORD%', urllib.parse.quote(word))
    request = requests.get(url)
    return request


@click.command()
@click.argument('word', required=False)
@click.option('-v', '--version', 'opt', flag_value=Opt.version)
@click.option('-a', '--author', 'opt', flag_value=Opt.author)
def entry(word, opt):
    if opt is not None:
        if opt == Opt.version:
            click.echo('v0.1.1')
        elif opt == Opt.author:
            click.echo('email: guojian_k@qq.com')
        return
    if not word:
        return
    name, zh_means, en_means = __search(word)
    click.secho(name, bold=True, blink=True, fg='cyan')
    click.secho('\n网络释义', fg='yellow')
    for zh_mean in zh_means:
        click.secho(zh_mean)
    click.secho('\n英英释义', fg='yellow')
    for cn_mean in en_means:
        click.secho(cn_mean)
    click.echo('\n')
