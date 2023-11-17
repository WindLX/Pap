extern crate md_parser;

use criterion::{black_box, criterion_group, criterion_main, Criterion};
use md_parser::{expr::Block, parser::Parser, spliter::split};
use rayon::prelude::{IntoParallelRefIterator, ParallelIterator};
use std::fs::read_to_string;

fn parse(path: &str) {
    let mut input = String::new();
    let text = read_to_string(path).unwrap();
    // 698_000
    for _ in 0..1000 {
        input.push_str(&text);
    }
    let result = split(&input);
    if result.len() < 1_000 {
        let _result: Vec<Block> = result
            .iter()
            .map(|r| {
                let mut parser = Parser::new();
                parser.process(r).unwrap()
            })
            .collect();
    } else {
        let _result: Vec<Block> = result
            .par_iter()
            .map(|r| {
                let mut parser = Parser::new();
                parser.process(r).unwrap()
            })
            .collect();
    }
    // dbg!(&result);
}

fn criterion_benchmark(c: &mut Criterion) {
    rayon::ThreadPoolBuilder::new()
        .num_threads(32)
        .build_global()
        .unwrap();
    c.bench_function("parse", |b| b.iter(|| parse(black_box("../test/test.md"))));
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
