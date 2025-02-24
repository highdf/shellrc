# ~/.latexmkrc
$pdf_mode = 1;                   # 强制 PDF 模式
$pdflatex = 'xelatex -synctex=1 -interaction=nonstopmode %O %S';  # ✅ 关键修正
$dvi_mode = 0;                   # 关闭 DVI 模式
$postscript_mode = 0;            # 关闭 PS 模式
$biber = 'biber %O %S';
$clean_ext = "aux bbl blg log";
$out_dir = "build";
$pdf_previewer = 'zathura';
