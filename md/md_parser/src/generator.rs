use crate::expr::*;
use crate::Result;

#[cfg(feature = "parallel")]
use rayon::prelude::{IntoParallelRefIterator, ParallelIterator};

#[cfg(feature = "parallel")]
pub trait Generator<T>
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
