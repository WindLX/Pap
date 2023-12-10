use crate::{bytes::MdChars, err::MdError, expr::*, Result};

#[derive(Debug, Clone)]
pub struct Parser {
    is_bold_1: bool,
    is_bold_2: bool,
    is_italic_1: bool,
    is_italic_2: bool,
    #[cfg(feature = "extra")]
    is_strike: bool,
}

impl<'md> Parser {
    pub fn new() -> Self {
        Self {
            is_bold_1: false,
            is_bold_2: false,
            is_italic_1: false,
            is_italic_2: false,
            #[cfg(feature = "extra")]
            is_strike: false,
        }
    }

    pub fn process(&mut self, input: &'md SplitBlock) -> Result<Block<'md>> {
        match input {
            SplitBlock::CodeBlock(lb, cb) => Ok(Block::CodeBlock(
                lb.clone(),
                <MdChars as Into<&str>>::into(cb.clone()),
            )),
            SplitBlock::Paragraph(pa) => match pa.as_bytes().get(0) {
                Some(b'#') => Ok(Block::Title(self.parse_title(&pa.as_bytes())?)),
                Some(b'+' | b'0'..=b'9' | b'\t') => {
                    Ok(Block::ListItem(self.parse_list(&pa.as_bytes())?))
                }
                Some(b'-') => {
                    if matches!(pa.as_bytes().get(1), Some(b' '))
                        && matches!(pa.as_bytes().get(2), Some(b'['))
                        && matches!(pa.as_bytes().get(3), Some(b' ' | b'x'))
                        && matches!(pa.as_bytes().get(4), Some(b']'))
                    {
                        Ok(Block::TodoItem(self.parse_todo(&pa.as_bytes())?))
                    } else {
                        Ok(Block::ListItem(self.parse_list(&pa.as_bytes())?))
                    }
                }
                Some(b'>') => Ok(Block::Quote(self.parse_quote(&pa.as_bytes())?)),
                Some(b'!') => Ok(Block::Image(self.parse_image(&pa.as_bytes())?)),
                #[cfg(feature = "extra")]
                Some(b'[') => {
                    if matches!(pa.as_bytes().get(1), Some(b'^')) {
                        Ok(Block::Footer(self.parse_footer(&pa.as_bytes())?))
                    } else {
                        Ok(Block::Paragraph(self.parse_paragraph(&pa.as_bytes())?))
                    }
                }
                _ => Ok(Block::Paragraph(self.parse_paragraph(&pa.as_bytes())?)),
            },
            SplitBlock::Line => Ok(Block::Line),
            #[cfg(feature = "math")]
            SplitBlock::MathBlock(mb) => {
                Ok(Block::MathBlock(<MdChars as Into<&str>>::into(mb.clone())))
            }
        }
    }

    pub fn parse_title_only(&mut self, line: usize, input: &'md SplitBlock) -> Option<RawTitle> {
        match input {
            SplitBlock::Paragraph(pa) => match pa.as_bytes().get(0) {
                Some(b'#') => match self.parse_raw_title(line, &pa.as_bytes()) {
                    Ok(t) => Some(t),
                    Err(_) => None,
                },
                _ => None,
            },
            _ => None,
        }
    }

    pub fn parse_link_only(&mut self, input: &'md SplitBlock) -> Vec<RawLink> {
        match input {
            SplitBlock::Paragraph(pa) => match self.parse_paragraph(pa.as_bytes()) {
                Ok(p) => {
                    let ll =
                        p.0.iter()
                            .filter(|s| matches!(s, Sentence::Link(_)))
                            .map(|s| match s {
                                Sentence::Link(l) => RawLink::from(l.clone()),
                                _ => unreachable!(),
                            })
                            .collect();
                    return ll;
                }
                _ => return Vec::new(),
            },
            _ => Vec::new(),
        }
    }

    fn parse_title(&mut self, input: &'md [u8]) -> Result<Title<'md>> {
        let mut level = 1;
        let mut input = &input[1..];
        loop {
            match input.get(0) {
                Some(b'#') => {
                    if level >= 6 {
                        break;
                    }
                    level += 1;
                    input = &input[1..];
                }
                Some(b' ') => input = &input[1..],
                _ => break,
            }
        }
        let content = self.parse_paragraph(input)?;
        Ok(Title {
            level: TitleLevel::from(level),
            content,
        })
    }

    fn parse_raw_title(&mut self, line: usize, input: &'md [u8]) -> Result<RawTitle> {
        let mut level = 1;
        let mut input = &input[1..];
        loop {
            match input.get(0) {
                Some(b'#') => {
                    if level >= 6 {
                        break;
                    }
                    level += 1;
                    input = &input[1..];
                }
                Some(b' ') => input = &input[1..],
                _ => break,
            }
        }
        let content = String::from_utf8(input.to_vec()).unwrap();
        Ok(RawTitle {
            line,
            level: TitleLevel::from(level),
            content,
        })
    }

    fn parse_list(&mut self, input: &'md [u8]) -> Result<ListItem<'md>> {
        let mut input = input;
        let mut level = 0;
        loop {
            match input.get(0) {
                Some(b'\t') => {
                    level += 1;
                    input = &input[1..];
                }
                Some(b'-' | b'+' | b'0'..=b'9') => break,
                _ => {
                    return Err(MdError::ListError(String::from(
                        "expect 'Tab' or '-' or '+' or '0'..='9'",
                    )))
                }
            }
        }
        match input[0] {
            b'-' | b'+' => {
                input = &input[1..];
                if let Some(b' ') = input.get(0) {
                    Ok(ListItem {
                        level,
                        index: None,
                        content: self.parse_paragraph(&input[1..])?,
                    })
                } else {
                    Err(MdError::ListError(String::from("expect 'Space'")))
                }
            }
            b'0'..=b'9' => {
                let index = self.parse_number(input)?;
                let input = &input[index.0..];
                if let (Some(b'.'), Some(b' ')) = (input.get(0), input.get(1)) {
                    Ok(ListItem {
                        level,
                        index: Some(index.1.into()),
                        content: self.parse_paragraph(&input[2..])?,
                    })
                } else {
                    Err(MdError::ListError(String::from("expect '.' && 'Space'")))
                }
            }
            _ => unreachable!(),
        }
    }

    fn parse_quote(&mut self, input: &'md [u8]) -> Result<Paragraph<'md>> {
        let input = &input[1..];
        if matches!(input.get(0), Some(b' ')) {
            self.parse_paragraph(&input[1..])
        } else {
            Err(MdError::QuoteError(String::from("expect 'Space'")))
        }
    }

    fn parse_paragraph(&mut self, input: &'md [u8]) -> Result<Paragraph<'md>> {
        let mut content = Vec::new();
        let mut input = input;
        loop {
            match input.get(0) {
                Some(b'`') => {
                    let c = self.parse_special_plain(&input[1..], b'`');
                    input = &input[c.0 + 1..];
                    if let Some(b'`') = input.get(0) {
                        if c.0 != 0 {
                            content.push(Sentence::Code(&std::str::from_utf8(c.1).unwrap()));
                        }
                        input = &input[1..];
                    } else {
                        return Err(MdError::ParagraphError(String::from("expect '`'")));
                    }
                }
                Some(b'[') => {
                    if matches!(input.get(1), Some(b'^')) {
                        let c = self.parse_footer_index(&input[2..])?;
                        input = &input[c.0 + 2..];
                        content.push(Sentence::FooterIndex(c.1));
                        if matches!(input.get(0), Some(b']')) {
                            input = &input[1..];
                        } else {
                            return Err(MdError::ParagraphError(String::from("expect ']'")));
                        }
                    } else {
                        let c = self.parse_plain(&input[1..]);
                        input = &input[c.0 + 1..];
                        if matches!(input.get(0), Some(b']')) && matches!(input.get(1), Some(b'('))
                        {
                            input = &input[2..];
                            let href = self.parse_special_plain(input, b')');
                            input = &input[href.0..];
                            if matches!(input.get(0), Some(b')')) {
                                let href = if href.1.len() == 0 {
                                    None
                                } else {
                                    Some(std::str::from_utf8(href.1).unwrap())
                                };
                                input = &input[1..];
                                content.push(Sentence::Link(Link {
                                    content: String::from_utf8_lossy(&c.1).to_string(),
                                    href,
                                }))
                            } else {
                                return Err(MdError::LinkError(String::from("expect ')'")));
                            }
                        } else {
                            return Err(MdError::LinkError(String::from("expect ']' && '('")));
                        }
                    }
                }
                #[cfg(feature = "math")]
                Some(b'$') => {
                    let c = self.parse_special_plain(&input[1..], b'$');
                    input = &input[c.0 + 1..];
                    if let Some(b'$') = input.get(0) {
                        if c.0 != 0 {
                            content.push(Sentence::Math(&std::str::from_utf8(c.1).unwrap()));
                        }
                        input = &input[1..];
                    } else {
                        return Err(MdError::ParagraphError(String::from("expect '$'")));
                    }
                }
                #[cfg(feature = "extra")]
                Some(b':') => {
                    let c = self.parse_special_plain(&input[1..], b':');
                    input = &input[c.0 + 1..];
                    if let Some(b':') = input.get(0) {
                        if c.0 != 0 {
                            content.push(Sentence::Emoji(&std::str::from_utf8(c.1).unwrap()));
                        }
                        input = &input[1..];
                    } else {
                        return Err(MdError::ParagraphError(String::from("expect ':'")));
                    }
                }
                None => break,
                _ => {
                    let text = self.parse_text(input);
                    input = text.0;
                    if let Some(text) = text.1 {
                        content.push(Sentence::Text(text))
                    }
                }
            }
        }
        Ok(Paragraph(content))
    }

    fn parse_text(&mut self, input: &'md [u8]) -> (&'md [u8], Option<Text>) {
        let mut input = input;
        let content = match input.get(0) {
            Some(b'*') => {
                input = &input[1..];
                match input.get(0) {
                    Some(b'*') => {
                        self.is_bold_1 = !self.is_bold_1;
                        input = &input[1..];
                        self.parse_plain(input)
                    }
                    _ => {
                        self.is_italic_1 = !self.is_italic_1;
                        self.parse_plain(input)
                    }
                }
            }
            Some(b'_') => {
                input = &input[1..];
                match input.get(0) {
                    Some(b'_') => {
                        self.is_bold_2 = true;
                        input = &input[1..];
                        self.parse_plain(input)
                    }
                    _ => {
                        self.is_italic_2 = !self.is_italic_2;
                        self.parse_plain(input)
                    }
                }
            }
            #[cfg(feature = "extra")]
            Some(b'~') => {
                input = &input[1..];
                if let Some(b'~') = input.get(0) {
                    input = &input[1..];
                    self.is_strike = !self.is_strike;
                    self.parse_plain(input)
                } else {
                    self.parse_plain(input)
                }
            }
            _ => self.parse_plain(input),
        };
        if content.0 == 0 {
            (&input[content.0..], None)
        } else {
            (
                &input[content.0..],
                Some(Text {
                    content: String::from_utf8_lossy(&content.1).to_string(),
                    is_bold: self.is_bold_1 || self.is_bold_2,
                    is_italic: self.is_italic_1 || self.is_italic_2,
                    #[cfg(feature = "extra")]
                    is_strike: self.is_strike,
                }),
            )
        }
    }

    fn parse_image(&mut self, input: &'md [u8]) -> Result<Image<'md>> {
        let mut input = &input[1..];
        if matches!(input.get(0), Some(b'[')) {
            let title = self.parse_plain(&input[1..]);
            input = &input[title.0 + 1..];
            if matches!(input.get(0), Some(b']')) && matches!(input.get(1), Some(b'(')) {
                input = &input[2..];
                let src = self.parse_special_plain(input, b')');
                input = &input[src.0..];
                if matches!(input.get(0), Some(b')')) {
                    let title = if title.1.len() == 0 {
                        None
                    } else {
                        Some(String::from_utf8_lossy(&title.1.clone()).to_string())
                    };
                    let src = if src.1.len() == 0 {
                        None
                    } else {
                        Some(std::str::from_utf8(src.1).unwrap())
                    };
                    return Ok(Image { title, src });
                } else {
                    return Err(MdError::ImageError(String::from("expect ')'")));
                }
            } else {
                return Err(MdError::ImageError(String::from("expect ']' && '('")));
            }
        } else {
            return Err(MdError::ImageError(String::from("expect '['")));
        }
    }

    fn parse_plain(&mut self, input: &'md [u8]) -> (usize, Vec<u8>) {
        let mut offset = 0;
        let mut skips = vec![];
        while offset < input.len() {
            let byte = input[offset];
            match byte {
                b'`' | b'_' | b'*' | b'[' | b']' | b'(' | b')' => break,
                b'\\' => {
                    skips.push(offset);
                    offset += 2
                }
                #[cfg(feature = "math")]
                b'$' => break,
                #[cfg(feature = "extra")]
                b'~' | b'{' | b'}' | b':' => break,
                _ => offset += 1,
            }
        }
        let mut input = input[..offset].to_vec();
        for s in skips {
            input = [&input[..s], &input[s + 1..]].concat()
        }
        (offset, input)
    }

    fn parse_number(&mut self, input: &'md [u8]) -> Result<(usize, usize)> {
        let mut offset = 0;
        let mut n: usize = 0;
        while offset < input.len() {
            let byte = input[offset];
            match byte {
                i @ b'0'..=b'9' => {
                    offset += 1;
                    n = n * 10 + (i - b'0') as usize;
                }
                b'.' => break,
                _ => return Err(MdError::NumberError(String::from("expect 'Number' or '.'"))),
            }
        }
        Ok((offset, n))
    }

    fn parse_special_plain(&mut self, input: &'md [u8], end: u8) -> (usize, &'md [u8]) {
        let mut offset = 0;
        while offset < input.len() {
            let byte = input[offset];
            if end == byte {
                break;
            } else {
                offset += 1;
            }
        }
        (offset, &input[..offset])
    }

    #[cfg(feature = "extra")]
    fn parse_todo(&mut self, input: &'md [u8]) -> Result<TodoItem<'md>> {
        let mut input = &input[3..];
        if matches!(input.get(0), Some(b' ' | b'x')) && matches!(input.get(1), Some(b']')) {
            let is_finished = matches!(input.get(0), Some(b'x'));
            input = &input[2..];
            let content = self.parse_paragraph(input)?;
            Ok(TodoItem {
                is_finished,
                content,
            })
        } else {
            Err(MdError::TodoError(String::from(
                "expect 'Space' or 'x' and ']'",
            )))
        }
    }

    #[cfg(feature = "extra")]
    fn parse_footer_index(&mut self, input: &'md [u8]) -> Result<(usize, FooterIndex<'md>)> {
        let c = self.parse_special_plain(input, b']');
        Ok((c.0, FooterIndex(std::str::from_utf8(c.1).unwrap())))
    }

    #[cfg(feature = "extra")]
    fn parse_footer(&mut self, input: &'md [u8]) -> Result<Footer<'md>> {
        let mut input = &input[2..];
        let index = self.parse_footer_index(input)?;
        input = &input[index.0..];
        if matches!(input.get(0), Some(b']'))
            && matches!(input.get(1), Some(b':'))
            && matches!(input.get(2), Some(b' '))
        {
            input = &input[3..];
            let content = self.parse_paragraph(input)?;
            Ok(Footer {
                index: index.1,
                content,
            })
        } else {
            return Err(MdError::FooterError(String::from("expect ']: '")));
        }
    }
}

pub fn parse(sb: &SplitBlock) -> Result<Block> {
    let mut parser = crate::parser::Parser::new();
    parser.process(sb)
}

pub fn parse_title_only(line: usize, sb: &SplitBlock) -> Option<RawTitle> {
    let mut parser = crate::parser::Parser::new();
    parser.parse_title_only(line, sb)
}

pub fn parse_link_only(sb: &SplitBlock) -> Vec<RawLink> {
    let mut parser = crate::parser::Parser::new();
    parser.parse_link_only(sb)
}

#[cfg(test)]
mod tests {
    use super::Parser;
    use crate::{
        expr::{Block, Image, Link, ListItem, Paragraph, Sentence, Text, Title, TitleLevel},
        spliter::split,
        Result,
    };

    #[cfg(feature = "parallel")]
    use std::fs::read_to_string;

    #[test]
    fn test_code_block() {
        let input = String::from("```\nlet a = 10\n```");
        let mut parser = Parser::new();
        let b = split(&input);
        let result: Vec<Result<Block>> = b.iter().map(|r| parser.process(r)).collect();
        dbg!(&result);
        assert_eq!(result, vec![Ok(Block::CodeBlock(None, "let a = 10\n"))]);
    }

    #[test]
    fn test_img() {
        let input = String::from("![](/asset/pic.png)\n");
        let mut parser = Parser::new();
        let b = split(&input);
        let result: Vec<Result<Block>> = b.iter().map(|r| parser.process(r)).collect();
        dbg!(&result);
        assert_eq!(
            result,
            vec![Ok(Block::Image(Image {
                title: None,
                src: Some("/asset/pic.png")
            }))]
        );
    }

    #[test]
    fn test_title() {
        let input = String::from(
            "# Title 1\n## Title 2\n### Title 3\n#### Title 4\n##### Title 5\n###### Title 6\n",
        );
        let mut parser = Parser::new();
        let b = split(&input);
        let result: Vec<Result<Block>> = b.iter().map(|r| parser.process(r)).collect();
        dbg!(&result);
        assert_eq!(
            result,
            vec![
                Ok(Block::Title(Title {
                    level: TitleLevel::H1,
                    content: Paragraph(vec![Sentence::Text(Text {
                        content: String::from("Title 1"),
                        is_bold: false,
                        is_italic: false,
                        #[cfg(feature = "extra")]
                        is_strike: false
                    })]),
                })),
                Ok(Block::Title(Title {
                    level: TitleLevel::H2,
                    content: Paragraph(vec![Sentence::Text(Text {
                        content: String::from("Title 2"),
                        is_bold: false,
                        is_italic: false,
                        #[cfg(feature = "extra")]
                        is_strike: false
                    })]),
                })),
                Ok(Block::Title(Title {
                    level: TitleLevel::H3,
                    content: Paragraph(vec![Sentence::Text(Text {
                        content: String::from("Title 3"),
                        is_bold: false,
                        is_italic: false,
                        #[cfg(feature = "extra")]
                        is_strike: false
                    })]),
                })),
                Ok(Block::Title(Title {
                    level: TitleLevel::H4,
                    content: Paragraph(vec![Sentence::Text(Text {
                        content: String::from("Title 4"),
                        is_bold: false,
                        is_italic: false,
                        #[cfg(feature = "extra")]
                        is_strike: false
                    })]),
                })),
                Ok(Block::Title(Title {
                    level: TitleLevel::H5,
                    content: Paragraph(vec![Sentence::Text(Text {
                        content: String::from("Title 5"),
                        is_bold: false,
                        is_italic: false,
                        #[cfg(feature = "extra")]
                        is_strike: false
                    })]),
                })),
                Ok(Block::Title(Title {
                    level: TitleLevel::H6,
                    content: Paragraph(vec![Sentence::Text(Text {
                        content: String::from("Title 6"),
                        is_bold: false,
                        is_italic: false,
                        #[cfg(feature = "extra")]
                        is_strike: false
                    })]),
                }))
            ]
        );
    }

    #[test]
    fn test_line() {
        let input = String::from("---\n");
        let mut parser = Parser::new();
        let b = split(&input);
        let result: Vec<Result<Block>> = b.iter().map(|r| parser.process(r)).collect();
        dbg!(&result);
        assert_eq!(result, vec![Ok(Block::Line)]);
    }

    #[test]
    fn test_quote() {
        let input = String::from("> This is quote\n");
        let mut parser = Parser::new();
        let b = split(&input);
        let result: Vec<Result<Block>> = b.iter().map(|r| parser.process(r)).collect();
        dbg!(&result);
        assert_eq!(
            result,
            vec![Ok(Block::Quote(Paragraph(vec![Sentence::Text(Text {
                content: String::from("This is quote"),
                is_bold: false,
                is_italic: false,
                #[cfg(feature = "extra")]
                is_strike: false
            })])))]
        );
    }

    #[test]
    fn test_list() {
        let input = String::from("+ This is disorder list\n\t11. This is order list");
        let mut parser = Parser::new();
        let b = split(&input);
        let result: Vec<Result<Block>> = b.iter().map(|r| parser.process(r)).collect();
        dbg!(&result);
        assert_eq!(
            result,
            vec![
                Ok(Block::ListItem(ListItem {
                    level: 0,
                    index: None,
                    content: Paragraph(vec![Sentence::Text(Text {
                        content: "This is disorder list".to_string(),
                        is_bold: false,
                        is_italic: false,
                        is_strike: false
                    })])
                })),
                Ok(Block::ListItem(ListItem {
                    level: 1,
                    index: Some(11),
                    content: Paragraph(vec![Sentence::Text(Text {
                        content: "This is order list".to_string(),
                        is_bold: false,
                        is_italic: false,
                        is_strike: false
                    })])
                }))
            ]
        );
    }

    #[test]
    fn test_paragraph() {
        let input =
            String::from("This is **bold**, this is *italic*, this is ***bold and italic***\n");
        let mut parser = Parser::new();
        let b = split(&input);
        let result: Vec<Result<Block>> = b.iter().map(|r| parser.process(r)).collect();
        dbg!(&result);
        assert_eq!(
            result,
            vec![Ok(Block::Paragraph(Paragraph(vec![
                Sentence::Text(Text {
                    content: "This is ".to_string(),
                    is_bold: false,
                    is_italic: false,
                    #[cfg(feature = "extra")]
                    is_strike: false,
                }),
                Sentence::Text(Text {
                    content: "bold".to_string(),
                    is_bold: true,
                    is_italic: false,
                    #[cfg(feature = "extra")]
                    is_strike: false,
                }),
                Sentence::Text(Text {
                    content: ", this is ".to_string(),
                    is_bold: false,
                    is_italic: false,
                    #[cfg(feature = "extra")]
                    is_strike: false,
                }),
                Sentence::Text(Text {
                    content: "italic".to_string(),
                    is_bold: false,
                    is_italic: true,
                    #[cfg(feature = "extra")]
                    is_strike: false,
                }),
                Sentence::Text(Text {
                    content: ", this is ".to_string(),
                    is_bold: false,
                    is_italic: false,
                    #[cfg(feature = "extra")]
                    is_strike: false,
                }),
                Sentence::Text(Text {
                    content: "bold and italic".to_string(),
                    is_bold: true,
                    is_italic: true,
                    #[cfg(feature = "extra")]
                    is_strike: false,
                })
            ])))]
        );
    }

    #[test]
    fn test_paragraph_2() {
        let input = String::from("A **little *complex* sentence.**\n");
        let mut parser = Parser::new();
        let b = split(&input);
        let result: Vec<Result<Block>> = b.iter().map(|r| parser.process(r)).collect();
        dbg!(&result);
        assert_eq!(
            result,
            vec![Ok(Block::Paragraph(Paragraph(vec![
                Sentence::Text(Text {
                    content: "A ".to_string(),
                    is_bold: false,
                    is_italic: false,
                    #[cfg(feature = "extra")]
                    is_strike: false,
                }),
                Sentence::Text(Text {
                    content: "little ".to_string(),
                    is_bold: true,
                    is_italic: false,
                    #[cfg(feature = "extra")]
                    is_strike: false,
                }),
                Sentence::Text(Text {
                    content: "complex".to_string(),
                    is_bold: true,
                    is_italic: true,
                    #[cfg(feature = "extra")]
                    is_strike: false,
                }),
                Sentence::Text(Text {
                    content: " sentence.".to_string(),
                    is_bold: true,
                    is_italic: false,
                    #[cfg(feature = "extra")]
                    is_strike: false,
                }),
            ])))]
        );
    }

    #[test]
    fn test_paragraph_3() {
        let input = String::from(
            "`let x = 10` and [link](http://example.com) and $x_a = 10$ and :happy:\n",
        );
        let mut parser = Parser::new();
        let b = split(&input);
        let result: Vec<Result<Block>> = b.iter().map(|r| parser.process(r)).collect();
        dbg!(&result);
        assert_eq!(
            result,
            vec![Ok(Block::Paragraph(Paragraph(vec![
                Sentence::Code("let x = 10"),
                Sentence::Text(Text {
                    content: " and ".to_string(),
                    is_bold: false,
                    is_italic: false,
                    #[cfg(feature = "extra")]
                    is_strike: false,
                }),
                Sentence::Link(Link {
                    content: "link".to_string(),
                    href: Some("http://example.com")
                }),
                Sentence::Text(Text {
                    content: " and ".to_string(),
                    is_bold: false,
                    is_italic: false,
                    #[cfg(feature = "extra")]
                    is_strike: false,
                }),
                Sentence::Math("x_a = 10"),
                Sentence::Text(Text {
                    content: " and ".to_string(),
                    is_bold: false,
                    is_italic: false,
                    #[cfg(feature = "extra")]
                    is_strike: false,
                }),
                Sentence::Emoji("happy"),
            ])))]
        );
    }

    #[cfg(feature = "math")]
    #[test]
    fn test_math_block() {
        let input = String::from("$$\nx_i = 10\n$$");
        let mut parser = Parser::new();
        let b = split(&input);
        let result: Vec<Result<Block>> = b.iter().map(|r| parser.process(r)).collect();
        dbg!(&result);
        assert_eq!(result, vec![Ok(Block::MathBlock("x_i = 10\n"))]);
    }

    #[cfg(feature = "pap")]
    #[cfg(feature = "parallel")]
    #[test]
    fn test_parser() {
        use rayon::prelude::{IntoParallelRefIterator, ParallelIterator};

        let input = read_to_string("../test/test.md").unwrap();
        let result = split(&input);
        let result: Vec<Block> = result
            .par_iter()
            .map(|r| {
                let mut parser = Parser::new();
                parser.process(r).unwrap()
            })
            .collect();
        dbg!(&result);
    }
}
