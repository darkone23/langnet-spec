const std = @import("std");
const langnet_spec = @import("langnet_spec");

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    std.debug.print("=== Zig Reader Example ===\n\n", .{});

    // 1. Read and decode SearchRequest from binary file
    std.debug.print("1. Reading SearchRequest from binary file...\n", .{});
    const search_request_data = try std.fs.cwd().readFileAlloc(allocator, "output/search_request.bin", 1024);
    defer allocator.free(search_request_data);

    var reader: std.Io.Reader = .fixed(search_request_data);
    var search_request = try langnet_spec.SearchRequest.decode(&reader, allocator);
    defer search_request.deinit(allocator);

    std.debug.print("   Decoded SearchRequest:\n", .{});
    std.debug.print("     query: {s}\n", .{search_request.query});
    std.debug.print("     page_number: {d}\n", .{search_request.page_number});
    std.debug.print("     results_per_page: {d}\n", .{search_request.results_per_page});

    // 2. Read and decode User from binary file
    std.debug.print("\n2. Reading User from binary file...\n", .{});
    const user_data = try std.fs.cwd().readFileAlloc(allocator, "output/user.bin", 1024);
    defer allocator.free(user_data);

    var user_reader: std.Io.Reader = .fixed(user_data);
    var user = try langnet_spec.User.decode(&user_reader, allocator);
    defer user.deinit(allocator);

    std.debug.print("   Decoded User:\n", .{});
    std.debug.print("     id: {s}\n", .{user.id});
    std.debug.print("     username: {s}\n", .{user.username});
    std.debug.print("     email: {s}\n", .{user.email});
    std.debug.print("     roles: ", .{});
    for (user.roles.items) |role| {
        std.debug.print("{s} ", .{role});
    }
    std.debug.print("\n", .{});

    // 3. Read and decode SearchResponse from binary file
    std.debug.print("\n3. Reading SearchResponse from binary file...\n", .{});
    const search_response_data = try std.fs.cwd().readFileAlloc(allocator, "output/search_response.bin", 4096);
    defer allocator.free(search_response_data);

    var search_response_reader: std.Io.Reader = .fixed(search_response_data);
    var search_response = try langnet_spec.SearchResponse.decode(&search_response_reader, allocator);
    defer search_response.deinit(allocator);

    std.debug.print("   Decoded SearchResponse:\n", .{});
    std.debug.print("     total_results: {d}\n", .{search_response.total_results});
    std.debug.print("     page_number: {d}\n", .{search_response.page_number});
    std.debug.print("     results count: {d}\n", .{search_response.results.items.len});

    for (search_response.results.items, 0..) |result, i| {
        std.debug.print("     Result {d}:\n", .{i + 1});
        std.debug.print("       id: {s}\n", .{result.id});
        std.debug.print("       title: {s}\n", .{result.title});
        std.debug.print("       url: {s}\n", .{result.url});
        std.debug.print("       snippet: {s}\n", .{result.snippet});
        if (result.metadata.items.len > 0) {
            std.debug.print("       metadata:\n", .{});
            for (result.metadata.items) |entry| {
                std.debug.print("         {s}: {s}\n", .{ entry.key, entry.value });
            }
        }
    }

    // 4. Demonstrate JSON decoding (optional)
    std.debug.print("\n4. Reading SearchRequest from JSON file...\n", .{});
    const search_request_json = try std.fs.cwd().readFileAlloc(allocator, "output/search_request.json", 1024);
    defer allocator.free(search_request_json);

    var search_request_parsed = try langnet_spec.SearchRequest.jsonDecode(search_request_json, .{}, allocator);
    defer search_request_parsed.deinit();
    const search_request_from_json = search_request_parsed.value;

    std.debug.print("   Decoded from JSON:\n", .{});
    std.debug.print("     query: {s}\n", .{search_request_from_json.query});
    std.debug.print("     page_number: {d}\n", .{search_request_from_json.page_number});
    std.debug.print("     results_per_page: {d}\n", .{search_request_from_json.results_per_page});

    // 5. Create a new message and serialize it
    std.debug.print("\n5. Creating and serializing new SearchRequest...\n", .{});
    var new_request = langnet_spec.SearchRequest{
        .query = "zig protocol buffers test",
        .page_number = 42,
        .results_per_page = 100,
    };

    var w: std.Io.Writer.Allocating = .init(allocator);
    defer w.deinit();
    try new_request.encode(&w.writer, allocator);

    std.debug.print("   Created new SearchRequest:\n", .{});
    std.debug.print("     query: {s}\n", .{new_request.query});
    std.debug.print("     page_number: {d}\n", .{new_request.page_number});
    std.debug.print("     results_per_page: {d}\n", .{new_request.results_per_page});
    std.debug.print("   Serialized size: {d} bytes\n", .{w.written().len});

    // Write the new binary file
    try std.fs.cwd().writeFile(.{ .sub_path = "output/zig_generated.bin", .data = w.written() });
    std.debug.print("   Written to: output/zig_generated.bin\n", .{});

    std.debug.print("\n=== Example Complete ===\n", .{});
    std.debug.print("\nCross-language verification:\n", .{});
    std.debug.print("- Python wrote binary files\n", .{});
    std.debug.print("- Zig successfully read them\n", .{});
    std.debug.print("- Zig created new binary file\n", .{});
    std.debug.print("- Python can read zig_generated.bin\n", .{});
}
