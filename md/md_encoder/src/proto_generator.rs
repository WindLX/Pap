use md_parser::expr::*;
use md_parser::generator::Generator;
use md_parser::Result as MResult;
use prost::Message;

pub mod proto {
    include!("../generated/pap_proto.rs");
}

pub struct ProtoGenerator {
    parallel_threshold: usize,
}

impl ProtoGenerator {
    pub fn new(parallel_threshold: usize) -> Self {
        Self { parallel_threshold }
    }

    pub fn serialize(&self, input: String) -> Vec<Vec<u8>> {
        let mut bufs = Vec::new();
        self.process(input).iter().for_each(|b| {
            let mut buf = Vec::new();
            b.encode(&mut buf).unwrap();
            bufs.push(buf);
        });
        bufs
    }

    pub fn get_threshold(&self) -> usize {
        self.parallel_threshold
    }

    pub fn set_threshold(&mut self, parallel_threshold: usize) {
        self.parallel_threshold = parallel_threshold;
    }

    fn generate_title(&self, title: &Title) -> proto::Title {
        let t = proto::Title {
            level: match title.level {
                TitleLevel::H1 => 0,
                TitleLevel::H2 => 1,
                TitleLevel::H3 => 2,
                TitleLevel::H4 => 3,
                TitleLevel::H5 => 4,
                TitleLevel::H6 => 5,
            },
            content: Some(self.generate_paragraph(&title.content)),
        };
        t
    }

    fn generate_paragraph(&self, paragraph: &Paragraph) -> proto::Paragraph {
        let sentences = paragraph
            .0
            .iter()
            .map(|sentence| self.generate_sentence(sentence))
            .collect();
        proto::Paragraph { sentences }
    }

    fn generate_quote(&self, quote: &Paragraph) -> proto::Quote {
        let sentences = quote
            .0
            .iter()
            .map(|sentence| self.generate_sentence(sentence))
            .collect();
        proto::Quote { sentences }
    }

    fn generate_code_block(&self, language: Option<String>, code: &str) -> proto::CodeBlock {
        proto::CodeBlock {
            language,
            code: code.to_string(),
        }
    }

    fn generate_list_item(&self, list_item: &ListItem) -> proto::ListItem {
        proto::ListItem {
            level: list_item.level as u32,
            index: match list_item.index {
                Some(i) => Some(i as u32),
                None => None,
            },
            content: Some(self.generate_paragraph(&list_item.content)),
        }
    }

    fn generate_image(&self, image: &Image) -> proto::Image {
        proto::Image {
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

    fn generate_math_block(&self, math_block: &str) -> proto::MathBlock {
        proto::MathBlock {
            math: math_block.to_string(),
        }
    }

    fn generate_table_block(&self, _table_block: Option<()>) -> proto::TableBlock {
        proto::TableBlock {}
    }

    fn generate_todo_item(&self, todo_item: &TodoItem) -> proto::TodoItem {
        proto::TodoItem {
            is_finished: todo_item.is_finished,
            content: Some(self.generate_paragraph(&todo_item.content)),
        }
    }

    fn generate_footer(&self, footer: &Footer) -> proto::Footer {
        proto::Footer {
            index: Some(self.generate_footer_index(&footer.index)),
            content: Some(self.generate_paragraph(&footer.content)),
        }
    }

    fn generate_footer_index(&self, footer_index: &FooterIndex) -> proto::FooterIndex {
        proto::FooterIndex {
            index: footer_index.0.to_string(),
        }
    }

    fn generate_sentence(&self, sentence: &Sentence) -> proto::Sentence {
        proto::Sentence {
            sentence: Some(match sentence {
                Sentence::Text(text) => proto::sentence::Sentence::Text(self.generate_text(text)),
                Sentence::Link(link) => proto::sentence::Sentence::Link(self.generate_link(link)),
                Sentence::Code(code) => proto::sentence::Sentence::Code(code.to_string()),
                Sentence::Math(math) => proto::sentence::Sentence::Math(math.to_string()),
                Sentence::Emoji(emoji) => proto::sentence::Sentence::Emoji(emoji.to_string()),
                Sentence::FooterIndex(index) => {
                    proto::sentence::Sentence::FooterIndex(self.generate_footer_index(index))
                }
            }),
        }
    }

    fn generate_link(&self, link: &Link) -> proto::Link {
        proto::Link {
            content: link.content.to_string(),
            href: match link.href {
                Some(h) => Some(h.to_string()),
                None => None,
            },
        }
    }

    fn generate_text(&self, text: &Text) -> proto::Text {
        proto::Text {
            content: text.content.to_string(),
            is_bold: text.is_bold,
            is_italic: text.is_italic,
            is_strike: text.is_strike,
        }
    }
}

impl Generator<proto::Block> for ProtoGenerator {
    fn parallel_threshold(&self) -> usize {
        self.parallel_threshold
    }

    fn generate(&self, block: &MResult<Block>) -> proto::Block {
        let block = match block {
            Ok(block) => match block {
                Block::Title(title) => proto::block::Block::Title(self.generate_title(title)),
                Block::Paragraph(paragraph) => {
                    proto::block::Block::Paragraph(self.generate_paragraph(paragraph))
                }
                Block::Quote(paragraph) => {
                    proto::block::Block::Quote(self.generate_quote(paragraph))
                }
                Block::Image(image) => proto::block::Block::Image(self.generate_image(image)),
                Block::CodeBlock(lang, code) => {
                    proto::block::Block::CodeBlock(self.generate_code_block(lang.clone(), code))
                }
                Block::MathBlock(math) => {
                    proto::block::Block::MathBlock(self.generate_math_block(math))
                }
                Block::Line => proto::block::Block::Line(proto::Line {}),
                Block::Footer(footer) => proto::block::Block::Footer(self.generate_footer(footer)),
                Block::ListItem(list_item) => {
                    proto::block::Block::ListItem(self.generate_list_item(list_item))
                }
                Block::TodoItem(todo_item) => {
                    proto::block::Block::TodoItem(self.generate_todo_item(todo_item))
                }
                Block::TableBlock => {
                    proto::block::Block::TableBlock(self.generate_table_block(Some(())))
                }
            },
            Err(err) => panic!("{:?}", err),
        };
        proto::Block { block: Some(block) }
    }
}

#[cfg(test)]
mod proto_tests {
    use super::ProtoGenerator;
    use std::fs::read_to_string;

    #[test]
    fn test_proto_generator() {
        let input = read_to_string("../test/test.md").unwrap();
        let proto_generator = ProtoGenerator::new(1000);
        let _result = proto_generator.serialize(input);
        dbg!(&_result);
    }
}
