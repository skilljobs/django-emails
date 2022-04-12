"""
Convert HTML email to TEXT alternative version

- Preserve text and URLs
- For each link clearly delimit the URL on a new line
- Render nice headings
- Remove unnecessary whitespace
- Wrap and justify text but do not wrap URLs
- Reposition HTML email #header into a signature,
  so text body starts with a salutation

Test usage:
    email_body = open('email.html').read()
    print render_as_text(email_body)

Inspired by HTML to markdown.
"""

from textwrap import wrap
from lxml.html import fromstring


WRAP = 55


def ascii_emoji(s):
    """ASCII emojis or everything"""
    try:
        import emoji
        return emoji.demojize(s)
    except ImportError:
        import unicodedata
        return unicodedata.normalize('NFKD', str(s)).encode('ASCII', 'ignore')


def strip_whitespace(s):
    s = s.replace('\n', ' ')
    while '  ' in s:
        s = s.replace('  ', ' ')
    return s


def justify_str(s, width):
    right, w = s, width
    items = right.split()
    for i in range(len(items) - 1):
        items[i] += ' '
    left_count = w - sum([len(x) for x in items])
    while left_count > 0 and len(items) > 1:
        for i in range(len(items) - 1):
            items[i] += ' '
            left_count -= 1
            if left_count < 1:
                break
    return ''.join(items)


def justify_p(para, width):
    splitted = wrap(para, width)
    wrapped = []
    for line in splitted:
        aligned = line
        if line is not splitted[-1]:
            aligned = justify_str(line, width)
        wrapped.append(aligned)
    return '\n'.join(wrapped)


def render_as_text(html):
    html = ascii_emoji(strip_whitespace(html.strip()))
    dom = fromstring(html)
    txt, lines = '', []
    for ID in ('content', 'header', 'footer'):
        div = dom.cssselect('#'+ID)[0]
        s = ''
        for e in div.iter():
            if e.tag in ('p', 'div', 'h3', 'td'):
                s += '\n'
            if e.tag == 'li':
                s += '\n * '
            if e.tag == 'h3' or 'Thank you for' in e.text_content():
                s += '\n'
            if e.text_content() and not list(e):
                s += e.text_content()
            elif e.text:
                s += e.text
            if e.tail:
                s += e.tail
            if e.tag == 'a' and e.attrib.get('class', '') != 'noalt':
                href = e.attrib['href']
                if 'Confirm' in e.text_content():
                    href = ''  # don't show email confirmation link twice
                else:  # don't show tracking query strings in text
                    href = href.split('?')[0]
                s += '\n' + href + '\n'
            if e.tag == 'h3':
                s += '\n' + '-' * len(e.text) + '\n'
            if e.tag == 'u':
                s += ': '
        txt += s
        if ID != 'footer':
            txt += '\n' + '=' * WRAP + '\n'
    for line in txt.split('\n'):
        line = line.strip()
        if ' ' in line and len(line) > WRAP:
            line = justify_p(line, WRAP)
        lines.append(line)
    return '\n'.join(lines)
