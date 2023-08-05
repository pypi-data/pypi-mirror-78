from .pyruvate import serve, FileWrapper  # noqa: F401


def serve_paste(app, global_conf, **kw):
    write_blocking = kw.get('write_blocking', False)
    num_headers = kw.get('max_number_headers', 24)
    serve(
        app,
        kw.get('socket'),
        int(kw['workers']),
        write_blocking=bool(write_blocking),
        max_number_headers=int(num_headers))
    return 0
