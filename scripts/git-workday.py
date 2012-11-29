#!/usr/bin/env python
import subprocess
import sys
import collections
import re
import functools
import datetime

Event = collections.namedtuple('Event', ('commit_hash', 'author_email', 'datetime', 'ticket', 'comment'))

PROJECTS = ['MTRANSLATE']


def compose_two(f, g):
    return lambda elem: f(g(elem))


def compose(*args):
    return reduce(lambda g, f: (lambda elem: f(g(elem))), reversed(args))


def identity(elem):
    return elem


def pretty_form(event):
    ticket = event.ticket if event.ticket else '<Unknown>'
    return '{} {} {}'.format(event.datetime, ticket, event.comment)


def event_from_gitlog(line):
    sp = line.strip().split(' ', 3)
    commit_hash = sp[0]
    timestamp = int(sp[1])
    author_email = sp[2]
    full_comment = sp[3]
    comment_sp = full_comment.split(' ', 1)
    dt = datetime.datetime.fromtimestamp(timestamp)
    ticket_pat = '^({})\-[0-9]+$'.format('|'.join(PROJECTS))
    ticket_re = re.compile(ticket_pat)
    if ticket_re.search(comment_sp[0]):
        ticket = comment_sp[0]
        if len(comment_sp) == 2:
            comment = comment_sp[1]
        else:
            comment = None
    else:
        ticket = None
        comment = full_comment
    return Event(commit_hash=commit_hash,
            datetime=dt,
            ticket=ticket, comment=comment,
            author_email=author_email)


def test_date(event, date):
    return event.datetime.date() == date


def test_email(event, email):
    return event.author_email == email


def ilimit(iterable, limit=100, offset=0):
    end_offset = offset + limit
    for i, elem in enumerate(iterable):
        if offset <= i and i < end_offset:
            yield elem
        elif end_offset <= i:
            return


def main(args):
    date_sp = args[1].split('-', 2)
    email = args[2]
    current_date = datetime.date(int(date_sp[0]), int(date_sp[1]),
                                    int(date_sp[2]))
    p = subprocess.Popen(['git', 'log', '--format=%H %at %ae %s'],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            close_fds=True)
    p_out = p.stdout
    process = compose(functools.partial(map, pretty_form),
                        functools.partial(filter, functools.partial(test_date, date=current_date)),
                        functools.partial(filter, functools.partial(test_email, email=email)),
                        functools.partial(ilimit, limit=1000),
                        functools.partial(map, event_from_gitlog))
    for result in process(p_out):
        print result
    p_out.close()

if __name__ == '__main__':
    main(sys.argv)
