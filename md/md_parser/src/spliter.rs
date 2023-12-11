use crate::{bytes::MdChars, expr::SplitBlock};

pub fn split(input: &str) -> Vec<SplitBlock> {
    let mut input = MdChars::from(input).into_iter();
    let mut blocks = Vec::new();

    loop {
        #[cfg(feature = "math")]
        {
            if input.check_str("$$") {
                input.next();
                input.next();
                if input.check(b'\n') {
                    input.next();
                }
                let math = input.slice_to_str("\n$$");
                blocks.push(SplitBlock::MathBlock(
                    std::str::from_utf8(math).unwrap().to_string(),
                ));
                if input.check(b'\n') {
                    input.next();
                }
                continue;
            }
        }
        if input.check_str("```") {
            input.next();
            input.next();
            input.next();
            let lang = std::str::from_utf8(input.slice_to_byte(b'\n'))
                .unwrap()
                .to_string();
            let lang = if lang.is_empty() { None } else { Some(lang) };
            let code = input.slice_to_str("\n```");
            blocks.push(SplitBlock::CodeBlock(
                lang,
                std::str::from_utf8(code).unwrap().to_string(),
            ));
            if input.check(b'\n') {
                input.next();
            }
            continue;
        }
        if input.check_str("---") {
            input.next();
            input.next();
            input.next();
            input.slice_to_byte(b'\n');
            blocks.push(SplitBlock::Line);
            continue;
        }
        let para = input.slice_to_byte(b'\n');
        blocks.push(SplitBlock::Paragraph(MdChars::new(para)));
        if input.is_end() {
            break;
        }
    }
    blocks
}

#[cfg(test)]
mod tests {
    use super::split;
    use std::fs::read_to_string;

    #[test]
    fn test_split() {
        let input = read_to_string("../test/test.md").unwrap();
        let result = split(&input);
        dbg!(result);
    }

    #[test]
    fn test_short() {
        let input = "";
        let result = split(&input);
        dbg!(result);
    }
}
