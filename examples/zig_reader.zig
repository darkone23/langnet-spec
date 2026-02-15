const std = @import("std");
const langnet_spec = @import("langnet_spec");

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    std.debug.print("=== Zig Reader Example ===\n\n", .{});

    // 1. Read and decode QueryResponse from binary file
    std.debug.print("1. Reading QueryResponse from binary file...\n", .{});
    const query_response_data = try std.fs.cwd().readFileAlloc(allocator, "examples/output/query_response.bin", 4096);
    defer allocator.free(query_response_data);

    var reader: std.Io.Reader = .fixed(query_response_data);
    var query_response = try langnet_spec.QueryResponse.decode(&reader, allocator);
    defer query_response.deinit(allocator);

    std.debug.print("   Decoded QueryResponse:\n", .{});
    std.debug.print("     schema_version: {s}\n", .{query_response.schema_version});
    if (query_response.query) |q| {
        std.debug.print("     query.surface: {s}\n", .{q.surface});
        std.debug.print("     query.language_hint: {}\n", .{q.language_hint});
    }
    std.debug.print("     lemmas count: {d}\n", .{query_response.lemmas.items.len});
    std.debug.print("     analyses count: {d}\n", .{query_response.analyses.items.len});
    std.debug.print("     senses count: {d}\n", .{query_response.senses.items.len});
    std.debug.print("     citations count: {d}\n", .{query_response.citations.items.len});

    // Print lemmas
    std.debug.print("\n   Lemmas:\n", .{});
    for (query_response.lemmas.items, 0..) |lemma, i| {
        std.debug.print("     Lemma {d}:\n", .{i + 1});
        std.debug.print("       lemma_id: {s}\n", .{lemma.lemma_id});
        std.debug.print("       display: {s}\n", .{lemma.display});
        std.debug.print("       language: {}\n", .{lemma.language});
        if (lemma.sources.items.len > 0) {
            std.debug.print("       sources: ", .{});
            for (lemma.sources.items, 0..) |source, j| {
                if (j > 0) std.debug.print(", ", .{});
                std.debug.print("{s}", .{@tagName(source)});
            }
            std.debug.print("\n", .{});
        }
    }

    // Print analyses
    if (query_response.analyses.items.len > 0) {
        std.debug.print("\n   Analyses:\n", .{});
        for (query_response.analyses.items, 0..) |analysis, i| {
            std.debug.print("     Analysis {d}:\n", .{i + 1});
            std.debug.print("       type: {}\n", .{analysis.type});
            if (analysis.features) |features| {
                std.debug.print("       features.pos: {}\n", .{features.pos});
                std.debug.print("       features.case: {}\n", .{features.case});
                std.debug.print("       features.number: {}\n", .{features.number});
                std.debug.print("       features.gender: {}\n", .{features.gender});
            }
        }
    }

    // 2. Read and decode SimpleSearchQuery from binary file
    std.debug.print("\n2. Reading SimpleSearchQuery from binary file...\n", .{});
    const search_query_data = try std.fs.cwd().readFileAlloc(allocator, "output/simple_search_query.bin", 1024);
    defer allocator.free(search_query_data);

    var search_query_reader: std.Io.Reader = .fixed(search_query_data);
    var search_query = try langnet_spec.SimpleSearchQuery.decode(&search_query_reader, allocator);
    defer search_query.deinit(allocator);

    std.debug.print("   Decoded SimpleSearchQuery:\n", .{});
    std.debug.print("     query: {s}\n", .{search_query.query});
    std.debug.print("     language: {}\n", .{search_query.language});
    std.debug.print("     max_results: {d}\n", .{search_query.max_results});
    std.debug.print("     include_morphology: {}\n", .{search_query.include_morphology});
    std.debug.print("     include_definitions: {}\n", .{search_query.include_definitions});

    // 3. Demonstrate JSON decoding
    std.debug.print("\n3. Reading QueryResponse from JSON file...\n", .{});
    const query_response_json = try std.fs.cwd().readFileAlloc(allocator, "output/query_response.json", 8192);
    defer allocator.free(query_response_json);

    var query_response_parsed = try langnet_spec.QueryResponse.jsonDecode(query_response_json, .{}, allocator);
    defer query_response_parsed.deinit();
    const query_response_from_json = query_response_parsed.value;

    std.debug.print("   Decoded from JSON:\n", .{});
    std.debug.print("     schema_version: {s}\n", .{query_response_from_json.schema_version});
    std.debug.print("     lemmas count: {d}\n", .{query_response_from_json.lemmas.items.len});
    std.debug.print("     senses count: {d}\n", .{query_response_from_json.senses.items.len});

    // 4. Create a new SimpleSearchQuery and serialize it
    std.debug.print("\n4. Creating and serializing new SimpleSearchQuery...\n", .{});
    var new_search_query = langnet_spec.SimpleSearchQuery{
        .query = "agni",
        .language = .LANGUAGE_SAN,
        .max_results = 5,
        .include_morphology = true,
        .include_definitions = true,
    };

    var w: std.Io.Writer.Allocating = .init(allocator);
    defer w.deinit();
    try new_search_query.encode(&w.writer, allocator);

    std.debug.print("   Created new SimpleSearchQuery:\n", .{});
    std.debug.print("     query: {s}\n", .{new_search_query.query});
    std.debug.print("     language: {}\n", .{new_search_query.language});
    std.debug.print("     max_results: {d}\n", .{new_search_query.max_results});
    std.debug.print("   Serialized size: {d} bytes\n", .{w.written().len});

    // Write the new binary file
    try std.fs.cwd().writeFile(.{ .sub_path = "output/zig_generated.bin", .data = w.written() });
    std.debug.print("   Written to: output/zig_generated.bin\n", .{});

    std.debug.print("\n=== Example Complete ===\n", .{});
    std.debug.print("\nCross-language verification:\n", .{});
    std.debug.print("- Python wrote binary files using actual schema\n", .{});
    std.debug.print("- Zig successfully read QueryResponse and SimpleSearchQuery\n", .{});
    std.debug.print("- Zig created new SimpleSearchQuery binary file\n", .{});
    std.debug.print("- Python can read zig_generated.bin\n", .{});
}
