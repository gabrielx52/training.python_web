import socket
import sys
import mimetypes
import os
import pathlib


def response_ok(body=b"this is a pretty minimal response", mimetype=b"text/plain"):
    """returns a basic HTTP response"""
    resp = []
    resp.append(b"HTTP/1.1 200 OK")
    resp.append(b" ".join([b"Content-Type: ", mimetype]))
    resp.append(b"")
    resp.append(body)
    return b"\r\n".join(resp)


def response_method_not_allowed():
    """returns a 405 Method Not Allowed response"""
    resp = []
    resp.append("HTTP/1.1 405 Method Not Allowed")
    resp.append("")
    return "\r\n".join(resp).encode('utf8')


def response_not_found():
    """returns a 404 Not Found response"""
    return b"HTTP/1.1 404 Not Found\r\n\r\n"


def parse_request(request):
    first_line = request.split("\r\n", 1)[0]
    method, uri, protocol = first_line.split()
    if method != "GET":
        raise NotImplementedError("We only accept GET")
    return uri

def resolve_uri(uri):
    """This method should return appropriate content and a mime type"""
    homedir = pathlib.Path.cwd()
    print('\nHomedir: {}\n'.format(homedir))
    subdirs = [x for x in homedir.glob('**/*')]
    print('\nSubdirs: {}\n'.format(subdirs))
    return b"still broken", b'text/plain'

# def resolve_uri(uri):
#     """This method should return appropriate content and a mime type"""
#     '''
# It should map the pathname represented by the URI to a filesystem location.
# It should have a ‘home directory’, and look only in that location.
# If the URI is a directory, it should return a plain-text listing of the directory contents and the mimetype text/plain.
# If the URI is a file, it should return the contents of that file and its correct mimetype.
# If the URI does not map to a real location, it should raise an exception that the server can catch to return a 404 response.'''
#     uri = pathlib.Path(uri)
#     homedir = pathlib.Path.cwd().joinpath('webroot')
#     fullpath = homedir.joinpath(uri)
#     if not fullpath.exists():
#         raise NameError
#     elif fullpath.is_dir():
#         mimetype = 'text/plain'
#         content = list(fullpath.glob('**'))
#     else:
#         mimetype = mimetypes.guess_type(uri)[0]
#         content = open(fullpath, 'rb')
#     #print(fullpath)
#     print(homedir.joinpath(uri))
#     #print(uri)
#     return content, mimetype.encode()

# def resolve_uri(uri):
#     mimetype = mimetypes.guess_type(uri)[0]
#     homedir = os.getcwd() + '/webroot'
#     for i in os.listdir(homedir):
#         print(i)
#     uri = homedir + uri
#     print(uri,'\n','#'*25)
#     content = ''
#     if not os.path.exists(uri):
#         raise NameError
#     if mimetype is None:
#         mimetype = 'text/plain'
#         for i in os.listdir(uri):
#             content += i + ' '
#         #content.encode('utf8')
#     """This method should return appropriate content and a mime type"""
    return content.encode('utf8'), mimetype.encode('utf8')


def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                request = ''
                while True:
                    data = conn.recv(1024)
                    request += data.decode('utf8')
                    if len(data) < 1024:
                        break

                try:
                    uri = parse_request(request)
                except NotImplementedError:
                    response = response_method_not_allowed()
                else:
                    try:
                        content, mime_type = resolve_uri(uri)
                    except NameError:
                        response = response_not_found()
                    else:
                        response = response_ok(content, mime_type)

                print('sending response', file=log_buffer)
                conn.sendall(response)
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return


if __name__ == '__main__':
    server()
    sys.exit(0)
