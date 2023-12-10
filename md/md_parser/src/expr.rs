use crate::bytes::MdChars;

#[derive(Debug)]
pub enum SplitBlock {
    Paragraph(MdChars),
    CodeBlock(Option<String>, MdChars),
    Line,
    #[cfg(feature = "math")]
    MathBlock(MdChars),
}

impl ToString for SplitBlock {
    fn to_string(&self) -> String {
        match self {
            SplitBlock::Paragraph(s) => s.to_string(),
            SplitBlock::CodeBlock(l, s) => {
                format!(
                    "```{}\n{}\n```",
                    l.clone().unwrap_or_default(),
                    s.to_string()
                )
            }
            SplitBlock::Line => "---".to_string(),
            #[cfg(feature = "math")]
            SplitBlock::MathBlock(s) => format!("$$\n{}\n$$", s.to_string()),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub enum Block<'md> {
    Title(Title<'md>),
    Paragraph(Paragraph<'md>),
    Quote(Paragraph<'md>),
    ListItem(ListItem<'md>),
    CodeBlock(Option<String>, &'md str),
    Image(Image<'md>),
    Line,
    #[cfg(feature = "math")]
    MathBlock(&'md str),
    #[cfg(feature = "extra")]
    TodoItem(TodoItem<'md>),
    #[cfg(feature = "extra")]
    Footer(Footer<'md>),
}

#[derive(Debug, Clone, PartialEq)]
pub struct Title<'md> {
    pub level: TitleLevel,
    pub content: Paragraph<'md>,
}

#[derive(Debug, Clone, PartialEq)]
pub struct RawTitle {
    pub line: usize,
    pub level: TitleLevel,
    pub content: String,
}

#[derive(Debug, Clone, PartialEq)]
pub enum TitleLevel {
    H1,
    H2,
    H3,
    H4,
    H5,
    H6,
}

impl From<usize> for TitleLevel {
    fn from(value: usize) -> Self {
        match value {
            1 => TitleLevel::H1,
            2 => TitleLevel::H2,
            3 => TitleLevel::H3,
            4 => TitleLevel::H4,
            5 => TitleLevel::H5,
            6 => TitleLevel::H6,
            _ => panic!("Invalid title level"),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Paragraph<'md>(pub Vec<Sentence<'md>>);

#[derive(Debug, Clone, PartialEq)]
pub enum Sentence<'md> {
    Text(Text),
    Link(Link<'md>),
    Code(&'md str),
    #[cfg(feature = "math")]
    Math(&'md str),
    #[cfg(feature = "extra")]
    Emoji(&'md str),
    #[cfg(feature = "extra")]
    FooterIndex(FooterIndex<'md>),
}

#[derive(Debug, Clone, PartialEq)]
pub struct Text {
    pub content: String,
    pub is_bold: bool,
    pub is_italic: bool,
    #[cfg(feature = "extra")]
    pub is_strike: bool,
}

impl Default for Text {
    fn default() -> Self {
        Text {
            content: String::new(),
            is_bold: false,
            is_italic: false,
            is_strike: false,
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Link<'md> {
    pub content: String,
    pub href: Option<&'md str>,
}

#[derive(Debug, Clone, PartialEq)]
pub struct RawLink {
    pub content: String,
    pub href: Option<String>,
    pub is_md: bool,
}

impl<'md> From<Link<'md>> for RawLink {
    fn from(value: Link<'md>) -> Self {
        RawLink {
            content: value.content,
            href: match value.href {
                Some(href) => Some(href.to_string()),
                None => None,
            },
            is_md: value
                .href
                .map(|href| href.starts_with("md://"))
                .unwrap_or_default(),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Image<'md> {
    pub title: Option<String>,
    pub src: Option<&'md str>,
}

#[derive(Debug, Clone, PartialEq)]
pub struct ListItem<'md> {
    pub level: usize,
    pub index: Option<usize>,
    pub content: Paragraph<'md>,
}

#[cfg(feature = "extra")]
#[derive(Debug, Clone, PartialEq)]
pub struct TodoItem<'md> {
    pub is_finished: bool,
    pub content: Paragraph<'md>,
}

#[cfg(feature = "extra")]
#[derive(Debug, Clone, PartialEq)]
pub struct FooterIndex<'md>(pub &'md str);

#[cfg(feature = "extra")]
#[derive(Debug, Clone, PartialEq)]
pub struct Footer<'md> {
    pub index: FooterIndex<'md>,
    pub content: Paragraph<'md>,
}
