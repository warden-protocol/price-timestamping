{ pkgs ? import <nixpkgs> {} }:

with pkgs;
let
    py = import ./src/py.nix {requirementsFile=./src/requirements.txt;};

in
mkShell {
        name = "pg-shell";
        buildInputs = [
        py
        #pg
        #haskellPackages.submark
        #graphviz
        ];
        #shellHook =''
        #. ${./utils/sh/shell-hook.sh} ${py}
        #trap end EXIT
        #'';
      }

