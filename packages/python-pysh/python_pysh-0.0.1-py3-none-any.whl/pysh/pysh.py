#! /usr/bin/env python3
import os
import random

def main():
    _bgr = random.randint(0, 255)
    _bgg = random.randint(0, 255)
    _bgb = random.randint(0, 255)
    _fgr = 255 - _bgr
    _fgg = 255 - _bgg
    _fgb = 255 - _bgb

    while True:
        prompt = ''
        cmd = ''
        pwd = os.getcwd()
        
        if pwd.startswith(os.getenv('HOME')):
            pwd = '~' + pwd[len(os.getenv('HOME')):]

        pwd = pwd.split('/')

        for it, dir_ in enumerate(pwd):
            bgr_ = random.randint(0, 255)
            bgg_ = random.randint(0, 255)
            bgb_ = random.randint(0, 255)
            fgr_ = 255 - bgr_
            fgg_ = 255 - bgg_
            fgb_ = 255 - bgb_

            if pwd != ['', '']:
                prompt += '\x1b[48;2;%s;%s;%sm\x1b[38;2;%s;%s;%sm %s ' % (_bgr, _bgg, _bgb, _fgr, _fgg, _fgb, dir_ if dir_ else '/')

                if it != len(pwd) - 1:
                    prompt += '\x1b[38;2;%s;%s;%sm\x1b[48;2;%s;%s;%sm\ue0b0\x1b[0m' % (_bgr, _bgg, _bgb, bgr_, bgg_, bgb_)
                else:
                    prompt += '\x1b[0m\x1b[38;2;%s;%s;%sm\ue0b0\x1b[0m' % (_bgr, _bgg, _bgb)
            else:
                prompt = '\x1b[48;2;%s;%s;%sm\x1b[38;2;%s;%s;%sm / \x1b[0m\x1b[38;2;%s;%s;%sm\ue0b0\x1b[0m' % (_bgr, _bgg, _bgb, _fgr, _fgg, _fgb, _bgr, _bgg, _bgb)

            _bgr = bgr_
            _bgg = bgg_
            _bgb = bgb_
            _fgr = fgr_
            _fgg = fgg_
            _fgb = fgb_
        prompt += ' '

        if prompt:
            try:
                cmd = input(prompt)
            except KeyboardInterrupt:
                print()
                continue
            except EOFError:
                print('exit')
                quit()
        
            if cmd.startswith('cd '):
                _dir = cmd[3:]

                if _dir == '~':
                    _dir = os.getenv('HOME')

                try:
                    os.chdir(_dir)
                except:
                    print('/bin/zsh:', _dir + ': No such file or directory')

                continue
            elif cmd == 'exit':
                quit()
            elif cmd == 'cd':
                os.chdir(os.getenv('HOME'))
                continue

            os.system('/bin/zsh -c "' + cmd.replace('"', '\\"') + '"')

if __name__ == '__main__':
    main()
