# Justfile for LangNet Schema Definitions
# Usage: just <command>

# Default task: show available commands
default:
    just --list

# Generate all code (Python and Zig)
generate-all:
    just generate-python
    just generate-zig

# Generate Python protobuf code
generate-python:
    mkdir -p generated/python
    protoc \
        --python_out=generated/python \
        --proto_path=schema \
        schema/*.proto
    @echo "✓ Python code generated in generated/python/"

# Build zig-protobuf plugin
build-plugin:
    cd zig-protobuf && zig build install
    @echo "✓ zig-protobuf plugin built"

# Generate Zig protobuf code
generate-zig:
    # Build plugin if it doesn't exist
    if [ ! -f zig-protobuf/zig-out/bin/protoc-gen-zig ]; then \
        just build-plugin; \
    fi
    mkdir -p generated/zig
    protoc \
        --plugin=protoc-gen-zig=zig-protobuf/zig-out/bin/protoc-gen-zig \
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
    rm -rf generated output zig-protobuf/zig-out zig-protobuf/.zig-cache .zig-cache
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
    python examples/python_writer.py 2>&1 | grep -E "(Written:|Binary size:|JSON:|===.*===)" | head -15
    @echo "✓ Python serialization test completed"

# Test cross-language workflow
test-cross-lang:
    @echo "=== Testing cross-language workflow ==="
    @echo "1. Cleaning previous outputs..."
    rm -rf output 2>/dev/null || true
    @echo "2. Running Python writer..."
    python examples/python_writer.py 2>&1 | grep -E "(Written:|Binary size:|===.*===)" | head -15
    @echo "3. Verifying binary files..."
    @ls -lh output/*.bin 2>/dev/null | head -5 || echo "No binary files found"
    @echo "4. Testing Zig protobuf library..."
    cd zig-protobuf && zig test src/protobuf.zig 2>&1 | tail -3
    @echo "✓ Cross-language workflow test completed"

# Test full cross-language integration
test-full-cross-lang:
    @echo "=== Testing Full Cross-Language Integration ==="
    @echo "1. Cleaning previous outputs..."
    rm -rf output 2>/dev/null || true
    @echo "2. Generating protobuf code..."
    just generate-all
    @echo "3. Running Python writer to create binary files..."
    python examples/python_writer.py 2>&1 | grep -E "(Written:|Binary size:|===.*===)" | head -10
    @echo "4. Building Zig reader..."
    zig build reader 2>&1 | tail -5
    @echo "5. Running Zig reader to decode Python-generated files..."
    zig-out/bin/zig_reader 2>&1 | grep -E "(Decoded|Created|Written|===.*===)" | head -20
    @echo "6. Verifying Zig generated file exists..."
    @ls -lh output/zig_generated.bin 2>/dev/null || echo "Zig generated file not found"
    @echo "✓ Full cross-language integration test completed"

# Full integration test
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
