# LangNet Schema Definitions

Shared Protocol Buffer schema definitions for Python and Zig interoperability.

## Overview

This repository contains Protocol Buffer (`.proto`) schema definitions that can be used to generate type-safe code for both Python and Zig projects. It's designed to be used as a Git submodule in both Python and Zig projects to ensure consistent data structures across language boundaries.

**Key Features:**
- Single source of truth for data schemas
- Generated code checked into repository
- `zig-protobuf` as a git submodule for Zig code generation
- Cross-language serialization/deserialization testing

## Project Structure

```
langnet-spec/
├── schema/           # Protocol Buffer definitions
│   ├── example.proto
│   └── langnet.proto
├── generated/        # Generated code (CHECKED IN)
│   ├── python/      # Python protobuf classes
│   └── zig/         # Zig protobuf structs
├── vendor/          # Git submodule for Zig code generation
├── examples/        # Cross-language examples
│   ├── python_writer.py
│   └── zig_reader.zig
├── justfile         # Task runner for code generation
└── README.md        # This file
```

## Quick Start

### 1. Clone and Initialize Submodules

```bash
git clone --recursive https://github.com/darkone23/langnet-spec
cd langnet-spec
```

If you already cloned without `--recursive`:
```bash
git submodule update --init --recursive
```

### 2. Generate All Code

```bash
just generate-all
```

This will:
1. Build the `zig-protobuf` plugin (if not already built)
2. Generate Python protobuf classes in `generated/python/`
3. Generate Zig protobuf structs in `generated/zig/`

### 3. Use as Git Submodule

**In your Python project:**
```bash
git submodule add https://github.com/darkone23/langnet-spec
# The generated code is already in the submodule, ready to use
```

**In your Zig project:**
```bash
# Generate Python code using betterproto2
just generate-python
```

Runs `protoc` with betterproto2 plugin to generate modern Python dataclasses in `generated/python/`. The old `generate-python` command is deprecated and now aliases to this.

### Generate Zig Code Only

```bash
just generate-zig
```

Checks if the `zig-protobuf` plugin is built (builds it if needed), then runs `protoc` with the plugin to generate Zig code in `generated/zig/`.

### Build Zig Protobuf Plugin

```bash
just build-plugin
```

Builds the `protoc-gen-zig` plugin from the `zig-protobuf` submodule. This is automatically run by `generate-zig` if needed.

### Clean Generated Files

```bash
just clean
```

Removes all generated files in `generated/`.

## Usage Examples

### Python Usage (betterproto2)

```python
import sys
sys.path.append('langnet-spec/generated/python')

from langnet import SearchRequest

# Create message
request = SearchRequest(
    query="test query",
    page_number=1,
    results_per_page=20
)

# Serialize to binary
data = bytes(request)

# Serialize to JSON
json_data = request.to_json(indent=2)

# Deserialize from binary
new_request = SearchRequest.from_bytes(data)

# Deserialize from JSON
from_json = SearchRequest.from_json(json_data)
```

### Zig Usage (Zig 0.15.x)

```zig
const std = @import("std");
const SearchRequest = @import("langnet-spec/generated/zig/example.pb.zig").SearchRequest;

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    // Create message
    var request = SearchRequest{
        .query = "test query",
        .page_number = 1,
        .results_per_page = 20,
    };

    // Serialize
    var w: std.Io.Writer.Allocating = .init(allocator);
    defer w.deinit();
    try request.encode(&w.writer, allocator);

    // Deserialize from binary
    var reader: std.Io.Reader = .fixed(w.written());
    var decoded = try SearchRequest.decode(&reader, allocator);
    defer decoded.deinit(allocator);

    // Deserialize from JSON
    const json_parsed = try SearchRequest.jsonDecode("{\"query\":\"test\"}", .{}, allocator);
    defer json_parsed.deinit();
    const from_json = json_parsed.value;
}
```

**Note:** This project uses Zig 0.15.x with "writergate" I/O changes. See `ZIG_0.15_NOTES.md` for detailed migration guidance from older Zig versions.

## Adding New Schema Definitions

1. Add your `.proto` file to `schema/` directory
2. Update the `justfile` if you need custom generation options
3. Run `just generate-all`
4. Commit both `.proto` files and generated code

Example `.proto` file structure:
```protobuf
syntax = "proto3";
package yourpackage;

message YourMessage {
  string field1 = 1;
  int32 field2 = 2;
}
```

## Cross-Language Testing

This repository includes examples and tests for cross-language interoperability:

### Running Cross-Language Tests

```bash
# Test full cross-language workflow: Python writes, Zig reads, Zig writes
just test-cross-lang

# Test basic cross-language workflow
just test-cross-lang

# Run just Python serialization test
just test-python

# Test Zig compilation
just test-zig-compile
```

### Example Workflow

The `examples/` directory contains working examples:

1. **Python writes (betterproto2)**: `python_writer_betterproto2.py` creates binary and JSON files using modern dataclasses
2. **Legacy Python writer**: `python_writer.py` (deprecated, uses standard protobuf)
3. **Zig reads**: `zig_reader.zig` reads Python-generated files, creates new binary
4. **Cross-verification**: Python can read Zig-generated files and vice versa

```bash
# Generate all code and run examples
just generate-all
python examples/python_writer_betterproto2.py
zig build reader
zig-out/bin/zig_reader
```

## Development Workflow

1. **Edit schema**: Modify `.proto` files in `schema/`
2. **Regenerate code**: Run `just generate-all`
3. **Test cross-language**: Run `just test-cross-lang`
4. **Test changes**: Use the generated code in your projects
5. **Commit changes**: Commit both `.proto` files and generated code

## Continuous Integration

Recommended CI steps:
1. Initialize submodules: `git submodule update --init --recursive`
2. Generate code from `.proto` files: `just generate-all`
3. Verify generated code is up-to-date: `just check-generated`
4. Run language-specific tests

## Dependencies

### Required Tools
- `protoc` (Protocol Buffer compiler) - installed via Nix
- `zig` (0.15.0 or later) - for Zig code generation
- `python` (3.8+ with `protobuf` package)

### Python Dependencies
```bash
pip install protobuf
```

## Troubleshooting

### Common Issues

**`protoc` not found**: Ensure you're in the Nix development shell with `direnv` or run `nix develop`.

**Python import errors**: Add `langnet-spec/generated/python` to your Python path.

 **Zig compilation errors**: Ensure you have the `zig-protobuf` dependency properly set up in your Zig project. Note that this project uses Zig 0.15.x with "writergate" I/O changes - see `ZIG_0.15_NOTES.md` for migration guidance. Note that this project uses Zig 0.15.x with "writergate" I/O changes - see `ZIG_0.15_NOTES.md` for migration guidance.

**Submodule not initialized**: Run `git submodule update --init --recursive`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `just generate-all`
5. Submit a pull request
