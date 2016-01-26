import re


def addition(h):
    H = []
    for i in h:
        if i != '/':
            H.append(i)
     #sum(H)
    all_add = sum(map(int, H))
    return "<h1>Addition %s </h1>" % all_add


def subtraction(h):
    H = []
    return "<h1>Subtraction</h1>"


def multiplication():
    return "<h1>Multiplication</h1>"


def division():
    return "<h1>Division</h1>"


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


# def num_slash_checker(math_path):
#     num_slash = set('0123456789/')
#     if any((c in num_slash) for c in math_path):
#         print('Found')
#     else:
#         print('Not Found')


def math_list(math_path):
    num_list = math_path.replace('/', ' ').split(' ')
    #hh = H.split(' ')
    #for i in math_path:
    #    if i != '/':
    #        H.append(i)
     #sum(H)
    #all_add = sum(map(int, H))
    print(num_list)


def resolve_path(path):
    urls = [(r'^$', main_page),
            (r'^add/([0-9/]+)$', addition),
            (r'^subtraction/([0-9/]+)$', subtraction),
            (r'^multiplication/([0-9/]+)$', multiplication),
            (r'^division/([0-9/]+)$', division)
            ]
    math_path = path.lstrip('/')
    for regexp, func in urls:
        match = re.match(regexp, math_path)
        if match is None:
            continue
        args = match.groups([])
        return func, args
    # we get here if no url matches
    raise NameError


# if __name__ == '__main__':
#     from wsgiref.simple_server import make_server
#     srv = make_server('localhost', 8080, application)
#     srv.serve_forever()

math_list('91/0')