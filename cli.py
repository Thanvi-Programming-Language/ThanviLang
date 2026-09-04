import argparse
from pathlib import Path
from runtime import Runtime
from tpl_web import compile_web
def main():
 p=argparse.ArgumentParser(prog='thanvi');p.add_argument('file');p.add_argument('--web',action='store_true');p.add_argument('-o','--output',default='website.html');a=p.parse_args();s=Path(a.file).read_text(encoding='utf-8')
 if a.web:Path(a.output).write_text(compile_web(s),encoding='utf-8');print('TPL Web generated:',a.output)
 else:
  o=Runtime().run(s)
  if o:print(o)
if __name__=='__main__':main()
