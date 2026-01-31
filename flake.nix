{
  description = "A flake for Slides Slicer";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
  in {
    devShells.${system}.default =
      pkgs.mkShell
      {
        buildInputs = [
          pkgs.uv
          pkgs.python313
          (with pkgs.python313Packages; [
            python-lsp-server
            python-lsp-ruff
          ])
          pkgs.qpdf
        ];

        shellHook = ''
          echo "This is development for Slicer"
        '';
      };
  };
}
