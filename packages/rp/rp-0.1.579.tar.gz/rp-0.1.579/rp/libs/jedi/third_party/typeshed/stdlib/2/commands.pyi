from typing import overload, AnyStr, Text, Tuple

def getstatus(file: Text) -> str: ...
def getoutput(cmd: Text) -> str: ...
def getstatusoutput(cmd: Text) -> Tuple[int, str]: ...

@overload
def mk2arg(head: bytes, x: bytes) -> bytes: ...
@overload
def mk2arg(head: Text, x: Text) -> Text: ...

def mkarg(x: AnyStr) -> AnyStr: ...
