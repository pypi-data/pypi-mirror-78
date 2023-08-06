
import click
from functools import wraps
from . import protocol_parser
from .protocol_parser import Protocol

from pathlib import Path

def hrprotoparser_cmd(*args, **kwargs):
  def decorator(fun):
    @click.option('--proto', '-p', type=click.Path(exists=True, dir_okay=False, readable=True), required=True, help='Protocol file')
    @click.option('--info', is_flag=True, help='Print info on the protocol file (check its syntax in the process)')
    @click.option('--prefix', '-P', type=str, help='Prefix before all built-in structures', default='', required=False)
    @click.command()
    def main(proto, info, prefix, **kwargs_):
      p = Protocol(*args, **kwargs)
      with open(proto, 'r') as f :
        p.parse(f, proto)
      if info :
        click.echo(repr(p), err=True)
        return
      fun(
        proto=p,
        Constant = protocol_parser.Constant,
        IntConstant = protocol_parser.IntConstant,
        Type = protocol_parser.Type,
        Builtin = protocol_parser.Builtin,
        Array = protocol_parser.Array,
        Enum = protocol_parser.Enum,
        Field = protocol_parser.Field,
        Struct = protocol_parser.Struct,
        Packet = protocol_parser.Packet,
        Alias = protocol_parser.Alias,
        prefix = prefix,
        **kwargs_)
    return main
  return decorator
    

