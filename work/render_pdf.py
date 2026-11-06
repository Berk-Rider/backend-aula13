from pdf2image import convert_from_path
from pathlib import Path
pdf=Path('work/rendered/qa_review.pdf').resolve()
out=Path('work/rendered/png').resolve(); out.mkdir(parents=True,exist_ok=True)
pages=convert_from_path(str(pdf),dpi=120,fmt='png',output_folder=str(out),poppler_path=r'C:/Users/Berk_/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin',paths_only=True)
print('PAGES',len(pages))
for p in pages: print(p)
