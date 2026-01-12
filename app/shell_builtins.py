import sys
import os
from app import executor
from app.main import version
from typing import List

class Builtins:
    def __init__(self):
        self.builtins = {
            "exit": self.exit,
            "echo": self.echo,
            "type": self.type,
            "pwd": self.pwd,
            "about": self.about,
            "export": self.export,
            "cd": self.cd
        }
    
    def get_builtins(self) -> dict:
        return self.builtins
    
    def run_builtin(self, command:str, args:List[str]) -> bool:
        return_value = self.builtins[command](args)
        return return_value

    def exit(self, args:List[str]) -> bool:
        return False
    
    def echo(self, args:List[str]) -> bool:
        executor.write_stdout(" ".join(args) + '\n')
        return True
    
    def type(self, args:List[str]) -> bool:
        try:
            cmdtest = args[0]
            for cmdlet in args:
                if cmdlet in self.builtins:
                    executor.write_stdout(f"{cmdlet} is a shell builtin\n")
                else:
                    exec_path = executor.find_exec(cmdlet)
                    if exec_path:
                        executor.write_stdout(f"{cmdlet} is {exec_path}\n")
                    else:
                        executor.write_stdout(f"{cmdlet}: not found\n")
            return True
        except:
            executor.write_stdout(f"Empty argument\n")
            return True
    
    def pwd(self, args:List[str]) -> bool:
        current_directory = os.getcwd()
        executor.write_stdout(current_directory)
        return True
    
    def about(self, args:List[str]) -> bool:
        executor.write_stdout(f"mkshell {version}\n")
        executor.write_stdout("Developed by Marcus Kotsu\n")
        executor.write_stdout("Based on Codecrafters\n")
        executor.write_stdout("Follow on Bluesky: @kotsu.red\n")
        executor.write_stdout("Follow on GitHub: @Kotsucoder\n")
        return True
    
    def export(self, args:List[str]) -> bool:
        for var_setter in args:
            var_setter = var_setter.split("=", 1)
            var_name = var_setter[0]
            var_content = var_setter[1]
            os.environ[var_name] = var_content
        return True
    
    def cd(self, args:List[str]) -> bool:
        path = args[0]
        if os.path.isdir(path):
            os.chdir(path)
        else:
            executor.write_stdout(f"cd: {path}: No such file or directory\n")
        return True