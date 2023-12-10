use crate::js_expr::*;
use md_parser::expr::*;
use md_parser::generator::{SingleGenerator, StatusGenerator};
use md_parser::Result as MResult;
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub struct JsGenerator;

#[wasm_bindgen]
impl JsGenerator {
    pub fn new() -> Self {
        Self
    }

    pub fn split(&self, input: String) -> Vec<String> {
        md_parser::spliter::split(&input)
            .iter()
            .map(|x| x.to_string())
            .collect()
    }

    pub fn serialize(&self, input: String) -> Result<JsValue, JsError> {
        let v = &self.process(input);
        match v {
            Ok(v) => Ok(serde_wasm_bindgen::to_value(&v).unwrap()),
            Err(e) => Err(e.clone()),
        }
    }

    pub fn deserialize(self, js_expr: JsValue) -> String {
        let block = serde_wasm_bindgen::from_value::<JsBlock>(js_expr).unwrap();
        block.to_string()
    }

    fn generate_title(&self, title: &Title) -> JsTitle {
        let t = JsTitle {
            level: match title.level {
                TitleLevel::H1 => JsTitleLevel::H1,
                TitleLevel::H2 => JsTitleLevel::H2,
                TitleLevel::H3 => JsTitleLevel::H3,
                TitleLevel::H4 => JsTitleLevel::H4,
                TitleLevel::H5 => JsTitleLevel::H5,
                TitleLevel::H6 => JsTitleLevel::H6,
            },
            content: self.generate_paragraph(&title.content),
        };
        t
    }

    fn generate_paragraph(&self, paragraph: &Paragraph) -> JsParagraph {
        let sentences = paragraph
            .0
            .iter()
            .map(|sentence| self.generate_sentence(sentence))
            .collect();
        JsParagraph(sentences)
    }

    fn generate_list_item(&self, list_item: &ListItem) -> JsListItem {
        JsListItem {
            level: list_item.level,
            index: match list_item.index {
                Some(i) => Some(i),
                None => None,
            },
            content: self.generate_paragraph(&list_item.content),
        }
    }

    fn generate_image(&self, image: &Image) -> JsImage {
        JsImage {
            title: match &image.title {
                Some(t) => Some(t.to_string()),
                None => None,
            },
            src: match image.src {
                Some(s) => Some(s.to_string()),
                None => None,
            },
        }
    }

    fn generate_todo_item(&self, todo_item: &TodoItem) -> JsTodoItem {
        JsTodoItem {
            is_finished: todo_item.is_finished,
            content: self.generate_paragraph(&todo_item.content),
        }
    }

    fn generate_footer(&self, footer: &Footer) -> JsFooter {
        JsFooter {
            index: self.generate_footer_index(&footer.index),
            content: self.generate_paragraph(&footer.content),
        }
    }

    fn generate_footer_index(&self, footer_index: &FooterIndex) -> JsFooterIndex {
        JsFooterIndex(footer_index.0.to_string())
    }

    fn generate_sentence(&self, sentence: &Sentence) -> JsSentence {
        match sentence {
            Sentence::Text(text) => JsSentence::Text(self.generate_text(text)),
            Sentence::Link(link) => JsSentence::Link(self.generate_link(link)),
            Sentence::Code(code) => JsSentence::Code(code.to_string()),
            Sentence::Math(math) => JsSentence::Math(math.to_string()),
            Sentence::Emoji(emoji) => JsSentence::Emoji(emoji.to_string()),
            Sentence::FooterIndex(index) => {
                JsSentence::FooterIndex(self.generate_footer_index(index))
            }
        }
    }

    fn generate_link(&self, link: &Link) -> JsLink {
        JsLink {
            content: link.content.to_string(),
            href: match link.href {
                Some(h) => Some(h.to_string()),
                None => None,
            },
        }
    }

    fn generate_text(&self, text: &Text) -> JsText {
        JsText {
            content: text.content.to_string(),
            is_bold: text.is_bold,
            is_italic: text.is_italic,
            is_strike: text.is_strike,
        }
    }
}

impl SingleGenerator<Result<JsBlock, JsError>> for JsGenerator {
    fn generate(&self, block: &MResult<Block>) -> Result<JsBlock, JsError> {
        let block = match block {
            Ok(block) => match block {
                Block::Title(title) => JsBlock::Title(self.generate_title(title)),
                Block::Paragraph(paragraph) => {
                    JsBlock::Paragraph(self.generate_paragraph(paragraph))
                }
                Block::Quote(paragraph) => JsBlock::Quote(self.generate_paragraph(paragraph)),
                Block::Image(image) => JsBlock::Image(self.generate_image(image)),
                Block::CodeBlock(lang, code) => JsBlock::CodeBlock(lang.clone(), code.to_string()),
                Block::MathBlock(math) => JsBlock::MathBlock(math.to_string()),
                Block::Line => JsBlock::Line,
                Block::Footer(footer) => JsBlock::Footer(self.generate_footer(footer)),
                Block::ListItem(list_item) => JsBlock::ListItem(self.generate_list_item(list_item)),
                Block::TodoItem(todo_item) => JsBlock::TodoItem(self.generate_todo_item(todo_item)),
            },
            Err(err) => return Err(JsError::new(&err.to_string())),
        };
        Ok(block)
    }
}

#[wasm_bindgen]
pub struct JsStatusGenerator;

#[wasm_bindgen]
impl JsStatusGenerator {
    pub fn new() -> Self {
        Self
    }

    pub fn get_js_titles(&self, input: String) -> Vec<JsValue> {
        self.get_titles(input)
            .iter()
            .map(|t| {
                let t = JsRawTitle {
                    line: t.line,
                    level: match t.level {
                        TitleLevel::H1 => JsTitleLevel::H1,
                        TitleLevel::H2 => JsTitleLevel::H2,
                        TitleLevel::H3 => JsTitleLevel::H3,
                        TitleLevel::H4 => JsTitleLevel::H4,
                        TitleLevel::H5 => JsTitleLevel::H5,
                        TitleLevel::H6 => JsTitleLevel::H6,
                    },
                    content: t.content.clone(),
                };
                serde_wasm_bindgen::to_value(&t).unwrap()
            })
            .collect()
    }
}

impl StatusGenerator for JsStatusGenerator {}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_serialize() {
        let g = JsGenerator::new();
        let _ = g.serialize(String::from(""));
        // assert!(false)
    }
}
