#!/usr/bin/env python3

import re


def addition(num_str):
    if num_str.endswith('/'):
        num_str = num_str.rstrip('/')
    num_str = num_str.replace('/', '+')
    after_math = eval(num_str)
    return "<h1>Addition %s = %s </h1>" % (num_str, after_math)


def subtraction(num_str):
    if num_str.endswith('/'):
        num_str = num_str.rstrip('/')
    num_str = num_str.replace('/', '-')
    after_math = eval(num_str)
    return "<h1>Subtraction %s = %s </h1>" % (num_str, after_math)


def multiplication(num_str):
    if num_str.endswith('/'):
        num_str = num_str.rstrip('/')
    num_str = num_str.replace('/', '*')
    after_math = eval(num_str)
    return "<h1>Multiplication %s = %s </h1>" % (num_str, after_math)


def division(num_str):
    if num_str.endswith('/'):
        num_str = num_str.rstrip('/')
    try:
        after_math = eval(num_str)
        return "<h1>Division %s = %s </h1>" % (num_str, after_math)
    except ZeroDivisionError:
        return '<h1>Zero Division Error</h1>'


def main_page():
    return "<h1>Math things happen</h1>"


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


def resolve_path(path):
    urls = [(r'^$', main_page),
            (r'^add/([0-9/]+)$', addition),
            (r'^subtraction/([0-9/]+)$', subtraction),
            (r'^multiplication/([0-9/]+)$', multiplication),
            (r'^division/([0-9/]+)$', division)
            ]
    math_path = path.lstrip('/')
    print('math path: ',math_path)
    for regexp, func in urls:
        match = re.match(regexp, math_path)
        if match is None:
            continue
        args = match.groups([])
        return func, args
    # we get here if no url matches
    raise NameError


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
