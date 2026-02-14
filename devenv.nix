{ pkgs, lib, config, inputs, ... }:

{
  # https://devenv.sh/basics/
  env.name = "langnet-spec";

  env.SESSION_NAME = "langnet-spec";
  # env.UV_PROJECT = "${config.devenv.root}/backend";
  env.UV_PROJECT_ENVIRONMENT = "${config.devenv.root}/.devenv/state/venv";

  # https://devenv.sh/packages/
  packages = [
    pkgs.git
    pkgs.protobuf
    pkgs.just
    # pkgs.zig
    pkgs.python3Packages.ruff
  ];

  # https://devenv.sh/languages/
  # languages.rust.enable = true;
  languages.python.enable = true;
  languages.python.uv.enable = true;
  languages.python.uv.sync.enable = true;
  languages.python.venv.enable = true;
  languages.zig.enable = true;

  # https://devenv.sh/processes/
  # processes.dev.exec = "${lib.getExe pkgs.watchexec} -n -- ls -la";

  # https://devenv.sh/services/
  # services.postgres.enable = true;

  # https://devenv.sh/scripts/
  # scripts.hello.exec = ''
  #   echo hello from $GREET
  # '';

  # https://devenv.sh/basics/
  enterShell = ''
    # hello         # Run scripts directly
    # git --version # Use packages
    # 
    source $DEVENV_STATE/venv/bin/activate
    export VIRTUAL_ENV_PROMPT="$SESSION_NAME"
  '';

  # https://devenv.sh/tasks/
  # tasks = {
  #   "myproj:setup".exec = "mytool build";
  #   "devenv:enterShell".after = [ "myproj:setup" ];
  # };

  # https://devenv.sh/tests/
  enterTest = ''
    # echo "Running tests"
    # git --version | grep --color=auto "${pkgs.git.version}"
  '';

  # https://devenv.sh/git-hooks/
  # git-hooks.hooks.shellcheck.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}
