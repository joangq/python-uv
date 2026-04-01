from argbuilder import Command, Field
from typing import override
import os
import shutil
from pathlib import Path
from . import display

class CommandBase(Command):
    @override
    def run(
        self,
        *,
        text: bool = False,
        verbose: bool = False,
        pretty: bool = False,
        **kwargs: object
    ):
        env = kwargs.get('env', os.environ)
        env['PYTHONUTF8'] = '1'

        # if verbose:
        #     print(' '.join(self.build()))

        result = super().run(text=text, verbose=verbose, pretty=pretty, **kwargs)

        if not verbose:
            return result

        if result.returncode != 0:
            display.rich_dict(
                title='Error',
                data=dict(
                    stderr=result.stderr.decode('utf-8'),
                    stdout=result.stdout.decode('utf-8'),
                ),
                accent_colorizer=lambda _,__: 'red', # constant red
                value_colorizer=lambda _,__: 'red', # constant blue
            )
        else:
            display.rich_dict(
                title='Success',
                data=dict(
                    stderr=result.stderr.decode('utf-8'),
                    stdout=result.stdout.decode('utf-8'),
                ),
                accent_colorizer=lambda _,__: 'green', # constant green
                value_colorizer=lambda _,__: 'gray0', # constant blue
            )

        return result

class Uv(CommandBase):
    VIRTUAL_ENV_STACK = list()
    
    def arg0(self) -> str:
        return shutil.which('uv') or 'uv'

    class init(CommandBase):
        python_version: str = Field(['--python', '{value}'])
        package: bool = Field('--package')
        no_workspace: bool = Field('--no-workspace')
        bare: bool = Field('--bare')
        verbose: bool = Field('--verbose')

        @override
        def run(
            self, 
            *, 
            text: bool = False, 
            verbose: bool = False, 
            pretty: bool = False, 
            **kwargs: object
        ):
            result = super().run(text=text, verbose=verbose, pretty=pretty, **kwargs)

            if verbose:
                cwd = kwargs.get('cwd', '.')
                _cwd = Path(cwd)

                title = f'📁 {_cwd.name}/'
                data = dict()
                for file in _cwd.iterdir():
                    name = 2*' '
                    name += '📁' if file.is_dir() else '📄'
                    name += 1*' '
                    name += file.name
                    name += '/' if file.is_dir() else ''
                    data[name] = f'{file.stat().st_size} bytes'

                display.rich_dict(
                    title=title, 
                    data=data,
                    value_colorizer=lambda _,__: 'blue', # constant blue
                )
            return result

    class venv(CommandBase):
        no_project: bool = Field('--no-project')
        
        @override
        def run(
            self,
            *,
            text: bool = False,
            verbose: bool = False,
            pretty: bool = False,
            **kwargs: object
        ):
            cwd = kwargs.get('cwd', '.')
            _cwd = Path(cwd)

            if os.environ.get('VIRTUAL_ENV') is not None:
                Uv.VIRTUAL_ENV_STACK.append(os.environ['VIRTUAL_ENV'])
            
            os.environ['VIRTUAL_ENV'] = str((_cwd / '.venv').resolve())
            
            result = super().run(text=text, verbose=verbose, pretty=pretty, **kwargs)
            return result

    def exit(self):
        if Uv.VIRTUAL_ENV_STACK:
            os.environ['VIRTUAL_ENV'] = Uv.VIRTUAL_ENV_STACK.pop()
        
        return self

    class run(CommandBase):
        module: Command = Field('{value}', lambda x: x.build())
        active: bool = Field('--active')
        verbose: bool = Field('--verbose')

    class add(CommandBase):
        modules: str|list[str] = Field('{value}', lambda x: [x] if isinstance(x, str) else x)
        active: bool = Field('--active')
        group: str = Field(['--group', '{value}'])
        verbose: bool = Field('--verbose')