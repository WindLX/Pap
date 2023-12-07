use crate::expr::*;
use crate::Result;

pub trait Generator<T>
where
    T: Sized,
{
    fn generate(&self, block: &Result<Block>) -> T;
    fn process(&self, input: String) -> Vec<T> {
        let split_blocks = crate::spliter::split(&input);
        let bs: Vec<Result<Block>> = split_blocks
            .iter()
            .map(|sb| crate::parser::parse(sb))
            .collect();
        bs.iter().map(|b| self.generate(b)).collect()
    }
}

#[cfg(feature = "parallel")]
use rayon::prelude::{IntoParallelRefIterator, ParallelIterator};

#[cfg(feature = "parallel")]
pub trait ParaGenerator<T>
where
    T: Sized + Send,
    Self: Sync,
{
    fn parallel_threshold(&self) -> usize;
    fn generate(&self, block: &Result<Block>) -> T;
    fn process(&self, input: String) -> Vec<T> {
        let split_blocks = crate::spliter::split(&input);
        if split_blocks.len() < self.parallel_threshold() {
            let bs: Vec<Result<Block>> = split_blocks
                .iter()
                .map(|sb| crate::parser::parse(sb))
                .collect();
            bs.iter().map(|b| self.generate(b)).collect()
        } else {
            let bs: Vec<Result<Block>> = split_blocks
                .par_iter()
                .map(|sb| crate::parser::parse(sb))
                .collect();
            bs.par_iter().map(|b| self.generate(b)).collect()
        }
    }
}

pub trait SingleGenerator<T>
where
    T: Sized,
{
    fn generate(&self, block: &Result<Block>) -> T;
    fn process(&self, input: String) -> T {
        let split_block = crate::spliter::split(&input);
        let b = match &split_block.get(0) {
            Some(sb) => crate::parser::parse(sb),
            None => Ok(Block::Paragraph(Paragraph(vec![Sentence::Text(
                Text::default(),
            )]))),
        };
        self.generate(&b)
    }
}

pub trait StatusGenerator {
    fn get_titles(&self, input: String) -> Vec<RawTitle> {
        let split_blocks = crate::spliter::split(&input);
        let mut bs = Vec::new();
        for sb in split_blocks.iter().enumerate() {
            let t = crate::parser::parse_title_only(sb.0, &sb.1);
            if let Some(t) = t {
                bs.push(t);
            }
        }
        bs
    }
}

pub trait NetGenerator {
    fn get_refs(&self, input: String) -> Vec<RawLink> {
        let split_blocks = crate::spliter::split(&input);
        let mut bs = Vec::new();
        for sb in split_blocks {
            let l = crate::parser::parse_link_only(&sb);
            bs.extend(l)
        }
        bs
    }
}
