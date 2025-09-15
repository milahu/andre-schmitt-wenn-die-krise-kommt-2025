{
  pkgs ? import <nixpkgs> {},
}:

with pkgs;

mkShell {
  buildInputs = [
    sane-backends # scanimage
    gimp
    deskew
    tesseract
    imagemagick
    wget
    pdftk

    # not used by tesseract?
    # hunspellDicts.de-de
    # hunspellDicts.en-us

    # hocr editors
    # nur.repos.milahu.scribeocr
    # hocr-tools
    # nur.repos.milahu.archive-hocr-tools
    # gImageReader
    # gImageReader-qt

    # prettier

    (python3.withPackages (pp: with pp; [
      pillow
      numpy
      opencv4
      python-fontconfig
      reportlab
    ]))

    img2pdf

    # nur.repos.milahu.pdfjam
  ];
}
