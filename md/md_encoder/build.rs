use std::io::Result;

fn main() -> Result<()> {
    let mut config = prost_build::Config::new();
    config
        .protoc_arg("--proto_path")
        .protoc_arg("../proto")
        .out_dir("generated")
        .compile_protos(&["../proto/pap_block.proto"], &["src/"])?;
    Ok(())
}
