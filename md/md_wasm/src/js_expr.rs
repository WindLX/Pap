use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(tag = "tag", content = "content")]
pub enum JsBlock {
    Title(JsTitle),
    Paragraph(JsParagraph),
    Quote(JsParagraph),
    ListItem(JsListItem),
    CodeBlock(Option<String>, String),
    Image(JsImage),
    Line,
    MathBlock(String),
    TodoItem(JsTodoItem),
    Footer(JsFooter),
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct JsTitle {
    pub level: JsTitleLevel,
    pub content: JsParagraph,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct JsRawTitle {
    pub line: usize,
    pub level: JsTitleLevel,
    pub content: String,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum JsTitleLevel {
    H1,
    H2,
    H3,
    H4,
    H5,
    H6,
}

impl From<usize> for JsTitleLevel {
    fn from(value: usize) -> Self {
        match value {
            1 => JsTitleLevel::H1,
            2 => JsTitleLevel::H2,
            3 => JsTitleLevel::H3,
            4 => JsTitleLevel::H4,
            5 => JsTitleLevel::H5,
            6 => JsTitleLevel::H6,
            _ => panic!("Invalid title level"),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct JsParagraph(pub Vec<JsSentence>);

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(tag = "tag", content = "content")]
pub enum JsSentence {
    Text(JsText),
    Link(JsLink),
    Code(String),
    Math(String),
    Emoji(String),
    FooterIndex(JsFooterIndex),
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct JsText {
    pub content: String,
    pub is_bold: bool,
    pub is_italic: bool,
    pub is_strike: bool,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct JsLink {
    pub content: String,
    pub href: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct JsImage {
    pub title: Option<String>,
    pub src: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct JsListItem {
    pub level: usize,
    pub index: Option<usize>,
    pub content: JsParagraph,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct JsTodoItem {
    pub is_finished: bool,
    pub content: JsParagraph,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct JsFooterIndex(pub String);

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct JsFooter {
    pub index: JsFooterIndex,
    pub content: JsParagraph,
}

impl ToString for JsBlock {
    fn to_string(&self) -> String {
        match self {
            JsBlock::Title(title) => title.to_string(),
            JsBlock::Paragraph(paragraph) => paragraph.to_string(),
            JsBlock::ListItem(list_item) => list_item.to_string(),
            JsBlock::TodoItem(todo_item) => todo_item.to_string(),
            JsBlock::Footer(footer) => footer.to_string(),
            JsBlock::Quote(quote) => format!("> {}", quote.to_string()),
            JsBlock::CodeBlock(lang, code) => {
                if code.ends_with('\n') {
                    format!("```{}\n{}```", lang.clone().unwrap_or_default(), code)
                } else {
                    format!("```{}\n{}\n```", lang.clone().unwrap_or_default(), code)
                }
            }
            JsBlock::Image(image) => image.to_string(),
            JsBlock::MathBlock(math) => {
                if math.ends_with('\n') {
                    format!("$$\n{}$$", math)
                } else {
                    format!("$$\n{}\n$$", math)
                }
            }
            JsBlock::Line => String::from("---"),
        }
    }
}

impl ToString for JsTitle {
    fn to_string(&self) -> String {
        let level = match self.level {
            JsTitleLevel::H1 => "#",
            JsTitleLevel::H2 => "##",
            JsTitleLevel::H3 => "###",
            JsTitleLevel::H4 => "####",
            JsTitleLevel::H5 => "#####",
            JsTitleLevel::H6 => "######",
        };
        format!("{} {}", level, self.content.to_string())
    }
}

impl ToString for JsParagraph {
    fn to_string(&self) -> String {
        let v: Vec<String> = self.0.iter().map(|vv| vv.to_string()).collect();
        v.join("")
    }
}

impl ToString for JsListItem {
    fn to_string(&self) -> String {
        let prefix: String = std::iter::repeat("\t").take(self.level).collect();
        let index = match self.index {
            Some(i) => format!("{}. ", i),
            None => String::from("+ "),
        };
        format!("{}{}{}", prefix, index, self.content.to_string())
    }
}

impl ToString for JsTodoItem {
    fn to_string(&self) -> String {
        let state = if self.is_finished { "x" } else { " " };
        format!("- [{}] {}", state, self.content.to_string())
    }
}

impl ToString for JsFooter {
    fn to_string(&self) -> String {
        format!("{}: {}", self.index.to_string(), self.content.to_string())
    }
}

impl ToString for JsFooterIndex {
    fn to_string(&self) -> String {
        format!("[^{}]", self.0)
    }
}

impl ToString for JsSentence {
    fn to_string(&self) -> String {
        match self {
            JsSentence::Text(text) => text.to_string(),
            JsSentence::Link(link) => link.to_string(),
            JsSentence::Code(code) => format!("`{}`", code),
            JsSentence::Math(math) => format!("${}$", math),
            JsSentence::Emoji(emoji) => format!(":{}:", emoji),
            JsSentence::FooterIndex(index) => index.to_string(),
        }
    }
}

impl ToString for JsText {
    fn to_string(&self) -> String {
        let mut s = self.content.clone();
        if self.is_bold {
            s = format!("**{}**", s)
        }
        if self.is_italic {
            s = format!("*{}*", s)
        }
        if self.is_strike {
            s = format!("~~{}~~", s)
        }
        s
    }
}

impl ToString for JsLink {
    fn to_string(&self) -> String {
        format!(
            "[{}]({})",
            self.content.to_string(),
            self.href.clone().unwrap_or_default()
        )
    }
}

impl ToString for JsImage {
    fn to_string(&self) -> String {
        format!(
            "![{}]({})",
            self.title.clone().unwrap_or_default(),
            self.src.clone().unwrap_or_default()
        )
    }
}
