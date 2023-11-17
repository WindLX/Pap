#[derive(Debug, Clone, PartialEq)]
pub enum MdError {
    ImageError(String),
    NumberError(String),
    LinkError(String),
    ListError(String),
    QuoteError(String),
    ParagraphError(String),
    #[cfg(feature = "extra")]
    TitleError(String),
    #[cfg(feature = "extra")]
    TodoError(String),
    #[cfg(feature = "extra")]
    FooterError(String),
    #[cfg(feature = "table")]
    TableError(String),
}

unsafe impl Send for MdError {}

impl std::fmt::Display for MdError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            MdError::ImageError(s) => write!(f, "ImageError: {}", s),
            MdError::NumberError(s) => write!(f, "NumberError: {}", s),
            MdError::LinkError(s) => write!(f, "LinkError: {}", s),
            MdError::ListError(s) => write!(f, "ListError: {}", s),
            MdError::QuoteError(s) => write!(f, "QuoteError: {}", s),
            MdError::ParagraphError(s) => write!(f, "ParagraphError: {}", s),
            #[cfg(feature = "extra")]
            MdError::TitleError(s) => write!(f, "TitleError: {}", s),
            #[cfg(feature = "extra")]
            MdError::TodoError(s) => write!(f, "TodoError: {}", s),
            #[cfg(feature = "extra")]
            MdError::FooterError(s) => write!(f, "FooterError: {}", s),
            #[cfg(feature = "table")]
            MdError::TableError(s) => write!(f, "TableError: {}", s),
        }
    }
}
