use cpython::{NoArgs, ObjectProtocol, PyDict, PyErr, PyObject, PyResult, Python};
pub use python3_sys::{PyGILState_Ensure, PyGILState_Release, PyGILState_STATE, Py_None};
use slog::{self, Drain, Level, OwnedKVList, Record};

pub fn with_gil<'a, F, R>(mut code: F) -> R
where
    F: FnMut(Python<'a>, PyGILState_STATE) -> R,
{
    let (gilstate, py) = unsafe { (PyGILState_Ensure(), Python::assume_gil_acquired()) };
    let result = code(py, gilstate);
    unsafe { PyGILState_Release(gilstate) };
    result
}

pub fn with_released_gil<F, R>(gilstate: PyGILState_STATE, mut code: F) -> R
where
    F: FnMut() -> R,
{
    unsafe { PyGILState_Release(gilstate) };
    let result = code();
    unsafe { PyGILState_Ensure() };
    result
}

pub fn close_pyobject(ob: &mut PyObject, py: Python) -> PyResult<()> {
    if ob.getattr(py, "close").is_ok() {
        ob.call_method(py, "close", NoArgs, None)?;
    }
    Ok(())
}

pub struct PythonLogger {
    logger: PyObject,
    critical: u8,
    debug: u8,
    error: u8,
    info: u8,
    warn: u8,
}

impl PythonLogger {
    pub fn new(py: Python, name: &str) -> PyResult<Self> {
        let locals = PyDict::new(py);
        let pylogging = py.import("logging")?;
        let critical = pylogging.get(py, "CRITICAL")?.extract(py)?;
        let debug = pylogging.get(py, "DEBUG")?.extract(py)?;
        let error = pylogging.get(py, "ERROR")?.extract(py)?;
        let info = pylogging.get(py, "INFO")?.extract(py)?;
        let warn = pylogging.get(py, "WARN")?.extract(py)?;
        locals.set_item(py, "logging", pylogging)?;
        let logger: PyObject = py
            .eval(
                &format!("logging.getLogger('{}')", name),
                None,
                Some(&locals),
            )?
            .extract(py)?;
        Ok(Self {
            logger,
            critical,
            debug,
            error,
            info,
            warn,
        })
    }

    fn python_level(&self, level: Level) -> u8 {
        match level {
            Level::Critical => self.critical,
            Level::Error => self.error,
            Level::Warning => self.warn,
            Level::Info => self.info,
            Level::Debug => self.debug,
            Level::Trace => self.debug,
        }
    }
}

impl Drain for PythonLogger {
    type Ok = ();
    type Err = PyErr;

    fn log(&self, record: &Record, _values: &OwnedKVList) -> Result<Self::Ok, Self::Err> {
        match with_gil(|py, _gs| {
            self.logger.call_method(
                py,
                "log",
                (
                    self.python_level(record.level()),
                    format!("{}", record.msg()),
                ),
                None,
            )
        }) {
            Ok(_) => Ok(()),
            Err(e) => Err(e),
        }
    }
}

#[cfg(test)]
mod tests {
    use cpython::{PyDict, Python};
    use slog::{crit, debug, error, info, trace, warn, Drain};
    use std::fs::{remove_file, File};
    use std::io::Read;

    use crate::pyutils::PythonLogger;

    #[test]
    fn test_logging() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"
import logging
from tempfile import mkstemp

_, logfilename = mkstemp()
logging.basicConfig(filename=logfilename, level=logging.DEBUG)"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => match PythonLogger::new(py, "foo") {
                Ok(drain) => {
                    let root = slog::Logger::root(drain.fuse(), slog_o!());
                    crit!(root, "critical foo");
                    debug!(root, "debug: foo");
                    error!(root, "Foo error encountered");
                    info!(root, "bar baz info");
                    trace!(root, "tracing foo ...");
                    warn!(root, "there's a foo!");
                    let logfilename: String = locals
                        .get_item(py, "logfilename")
                        .unwrap()
                        .extract(py)
                        .unwrap();
                    let mut logfile = File::open(&logfilename).unwrap();
                    let mut contents = String::new();
                    logfile.read_to_string(&mut contents).unwrap();
                    assert_eq!("CRITICAL:foo:critical foo\nDEBUG:foo:debug: foo\nERROR:foo:Foo error encountered\nINFO:foo:bar baz info\nDEBUG:foo:tracing foo ...\nWARNING:foo:there's a foo!\n", contents);
                    remove_file(logfilename).unwrap();
                }
                Err(_) => assert!(false),
            },
            Err(e) => {
                println!("Error: {:?}", e);
                assert!(false);
            }
        }
    }
}
