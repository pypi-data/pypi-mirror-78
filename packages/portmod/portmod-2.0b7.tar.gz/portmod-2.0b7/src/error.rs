// Copyright 2019-2020 Portmod Authors
// Distributed under the terms of the GNU General Public License v3

use derive_more::{Display, From};
use pyo3::{exceptions, PyErr};

#[derive(Debug, Display, From)]
pub enum Error {
    #[display(fmt = "{}: {}", _0, _1)]
    IOError(String, std::io::Error),
    #[display(fmt = "{}: {}", _0, _1)]
    YamlError(String, serde_yaml::Error),
    LanguageIdentifierError(unic_langid::LanguageIdentifierError),
    StdError(Box<dyn std::error::Error>),
}

impl std::convert::From<Error> for PyErr {
    fn from(err: Error) -> PyErr {
        exceptions::OSError::py_err(err.to_string())
    }
}
