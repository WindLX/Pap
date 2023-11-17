pub mod bytes;
pub mod err;
pub mod expr;
pub mod generator;
pub mod parser;
pub mod spliter;

pub type Result<T> = std::result::Result<T, err::MdError>;
