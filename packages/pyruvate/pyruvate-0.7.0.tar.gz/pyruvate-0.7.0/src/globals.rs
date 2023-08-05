use cpython::{PyErr, PyModule, Python};
use log::error;

pub struct WSGIGlobals<'a> {
    pub server_name: &'a str,
    pub server_port: &'a str,
    pub script_name: &'a str,
    pub io_module: PyModule,
    pub sys_module: PyModule,
    pub wsgi_module: Option<PyModule>,
}

impl<'a> WSGIGlobals<'a> {
    pub fn new(
        server_name: &'a str,
        server_port: &'a str,
        script_name: &'a str,
        py: Python,
    ) -> WSGIGlobals<'a> {
        // XXX work around not being able to import wsgi module from tests
        let wsgi_module = match py.import("pyruvate") {
            Ok(pyruvate) => Some(pyruvate),
            Err(_) => {
                error!("Could not import WSGI module, so no FileWrapper");
                PyErr::fetch(py);
                None
            }
        };
        WSGIGlobals {
            server_name,
            server_port,
            script_name,
            io_module: py.import("io").expect("Could not import module io"),
            sys_module: py.import("sys").expect("Could not import module sys"),
            wsgi_module,
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::globals::WSGIGlobals;
    use cpython::Python;
    use log::debug;

    #[test]
    fn test_creation() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let sn = "127.0.0.1";
        let sp = "7878";
        let script = "/foo";
        let pypath = py.import("sys").unwrap().get(py, "path").unwrap();
        debug!("sys.path: {:?}", pypath);
        let got = WSGIGlobals::new(sn, sp, script, py);
        assert!(got.server_name == sn);
        assert!(got.server_port == sp);
        assert!(got.script_name == script);
    }
}
