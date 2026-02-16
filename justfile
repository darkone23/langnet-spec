# Justfile for LangNet Schema Definitions
# Usage: just <command>

# Default task: show available commands
default:
    just --list

# Generate all code (Python and Zig)
generate-all:
    just generate-python
    just generate-zig
    just format-python
    just format-zig

# Generate Python protobuf code (standard protoc, strip _pb2 suffix)
generate-python:
    mkdir -p generated/python
    protoc \
        --python_out=generated/python \
        --proto_path=schema \
        schema/*.proto
    just fixup-python
    @echo "✓ Python protobuf code generated in generated/python/"

# Fixup generated python code: drop unused glue and rename modules
fixup-python:
    rm -f generated/python/__init__.py generated/python/message_pool.py 2>/dev/null || true
    for f in generated/python/*_pb2.py; do \
        mv "$f" "${f/_pb2.py/.py}"; \
    done
    @echo "✓ Python code fixup completed"
   
# Build zig-protobuf plugin
build-plugin:
    cd vendor/zig-protobuf && zig build install
    @echo "✓ zig-protobuf plugin built"

# Generate Zig protobuf code
generate-zig:
    # Build plugin if it doesn't exist
    if [ ! -f ./vendor/zig-protobuf/zig-out/bin/protoc-gen-zig ]; then \
        just build-plugin; \
    fi
    mkdir -p generated/zig
    protoc \
        --plugin=protoc-gen-zig=vendor/zig-protobuf/zig-out/bin/protoc-gen-zig \
        --zig_out=generated/zig \
        --proto_path=schema \
        schema/*.proto
    @echo "✓ Zig code generated in generated/zig/"

# Clean all generated files
clean:
    rm -rf generated
    @echo "✓ Cleaned generated files"

# Clean everything including test outputs and build artifacts
clean-all:
    rm -rf generated output vendor/zig-protobuf/zig-out vendor/zig-protobuf/.zig-cache .zig-cache
    @echo "✓ Cleaned all generated files and build artifacts"

# Test Zig compilation
test-zig-compile:
    zig build test --summary all
    @echo "✓ Zig compilation successful"

# Format Zig code
format-zig:
    zig fmt generated/zig/*.zig 2>/dev/null || true
    @echo "✓ Formatted Zig code"

# Format Python code
format-python:
    ruff format generated/python
    @echo "✓ Formatted Python code"



# Test Python serialization
test-python:
    python examples/python_writer.py
    @echo "✓ Python serialization test completed"

# test cross-language integration
test-cross-lang:
    @echo "=== Testing Full Cross-Language Integration ==="
    @echo "1. Cleaning previous outputs..."
    rm -rf output 2>/dev/null || true
    @echo "2. Generating protobuf code..."
    just generate-all
    @echo "3. Running Python writer to create binary files..."
    python examples/python_writer.py
    @echo "4. Building Zig reader..."
    zig build reader
    @echo "5. Running Zig reader to decode Python-generated files..."
    zig-out/bin/zig_reader
    @echo "6. Verifying Zig generated file exists..."
    @ls -lh output/zig_generated.bin
    @echo "✓ Full cross-language integration test completed"

# full integration test
test-integration:
    just clean-all
    just build-plugin
    just generate-all
    just test-cross-lang
    @echo "=== Integration test complete ==="
    @echo "All systems operational:"
    @echo "  • zig-protobuf plugin built"
    @echo "  • Python/Zig code generated"
    @echo "  • Python serialization works"
    @echo "  • Binary files created"
    @echo "  • Zig library functional"
    @echo "Ready for cross-language use!"

# Show schema files
list-schemas:
    @echo "Schema files:"
    @ls -la schema/*.proto
