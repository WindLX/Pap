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
                let math = input.slice_to_str("$$");
                blocks.push(SplitBlock::MathBlock(MdChars::new(math)));
                continue;
            }
        }
        #[cfg(feature = "table")]
        {
            if input.check_str(":::table") {
                for _ in 0..9 {
                    input.next();
                }
                let table = input.slice_to_str(":::");
                blocks.push(SplitBlock::TableBlock(MdChars::new(table)));
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
            let code = input.slice_to_str("```");
            blocks.push(SplitBlock::CodeBlock(lang, MdChars::new(code)));
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
        if para.len() > 0 {
            blocks.push(SplitBlock::Paragraph(MdChars::new(para)));
        }
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
    fn test_table() {
        let input =
            ":::table\n| 表头1 | 表头2 |\n| ----- | ----- |\n| 内容1 | 内容2 |\n| 内容3 | 内容4 |:::";
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
