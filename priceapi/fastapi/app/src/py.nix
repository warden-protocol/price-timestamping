{ requirementsFile
}:

let machnix =
      import (builtins.fetchGit {
        url = "https://github.com/DavHau/mach-nix/";
        ref = "refs/tags/3.5.0";
      }) {
        pypiDataRev = "f62d8906d4558ed593fd3115f788ebf902b466bf";
        pypiDataSha256 = "sha256:1fak43vqj589n4fgsbsqkh5sxn8rp1ghpapr8ii387931pcry29n";
      };
in
machnix.mkPython {
  python = "python39Full";
  requirements = builtins.readFile requirementsFile;
}
