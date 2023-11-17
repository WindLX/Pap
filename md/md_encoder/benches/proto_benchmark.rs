extern crate mdencoder;

use criterion::{black_box, criterion_group, criterion_main, Criterion};
use mdencoder::proto_generator::ProtoGenerator;
use std::fs::read_to_string;

fn parse_proto(path: &str) {
    let mut input = String::new();
    let text = read_to_string(path).unwrap();
    // 698_000
    for _ in 0..1000 {
        input.push_str(&text);
    }
    let proto_generator = ProtoGenerator::new(1000);
    let _result = proto_generator.serialize(input);
}

fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("proto", |b| {
        b.iter(|| parse_proto(black_box("../test/test.md")))
    });
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
