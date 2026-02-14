const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Create shared protobuf module
    const zig_protobuf_module = b.addModule("protobuf", .{
        .root_source_file = b.path("vendor/zig-protobuf/src/protobuf.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Add zig_reader executable for cross-language testing
    const zig_reader_exe = b.addExecutable(.{
        .name = "zig_reader",
        .root_module = b.createModule(.{
            .root_source_file = b.path("examples/zig_reader.zig"),
            .target = target,
            .optimize = optimize,
            .imports = &.{
                .{ .name = "protobuf", .module = zig_protobuf_module },
                .{ .name = "generated_example", .module = b.addModule("generated_example", .{
                    .root_source_file = b.path("generated/zig/example.pb.zig"),
                    .target = target,
                    .optimize = optimize,
                    .imports = &.{
                        .{ .name = "protobuf", .module = zig_protobuf_module },
                    },
                }) },
                .{ .name = "generated_langnet", .module = b.addModule("generated_langnet", .{
                    .root_source_file = b.path("generated/zig/langnet.pb.zig"),
                    .target = target,
                    .optimize = optimize,
                    .imports = &.{
                        .{ .name = "protobuf", .module = zig_protobuf_module },
                    },
                }) },
            },
        }),
    });

    // Install the zig_reader executable
    b.installArtifact(zig_reader_exe);

    // Create a run step for zig_reader
    const zig_reader_run_step = b.step("reader", "Run the zig_reader example");
    const zig_reader_run_cmd = b.addRunArtifact(zig_reader_exe);
    zig_reader_run_step.dependOn(&zig_reader_run_cmd.step);
    zig_reader_run_cmd.step.dependOn(b.getInstallStep());
}
