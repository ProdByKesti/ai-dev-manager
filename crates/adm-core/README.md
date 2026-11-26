# Core foundation

This workspace contains one independent Rust core package, with a library and a
minimal executable. The library is the boundary for core and future domain
code; domain objects are deferred to M01-03. This avoids an empty domain crate.
The executable only prints a baseline message and exits; background operation,
persistence and IPC are not implemented.

The baseline requires Python 3.11 or later for the diagnostic and stable Rust
and Cargo 1.100.0 or later. Edition 2021 is sufficient for this minimal code;
1.100.0 is the minimum selected because it is the toolchain actually tested,
not a claim that older versions cannot compile it. Other versions and platforms
have not been verified. No external Rust dependencies are used.

From the repository root, using already installed tools without downloads or
toolchain changes:

```text
python -B scripts/check_rust_toolchain.py
cargo check --workspace --offline --locked
cargo build --workspace --offline --locked
cargo test --workspace --offline --locked
cargo build --workspace --release --offline --locked
cargo run --package adm-core --offline --locked
python -B -m unittest discover -s tests -p test_rust_toolchain.py
```

The diagnostic checks executable availability and reported stable versions; it
does not certify a working compiler, linker or the full future application stack.
Run the builds to validate the actual local environment. Configure an already
installed compatible toolchain if a check fails; the diagnostic does not install
or switch tools.
