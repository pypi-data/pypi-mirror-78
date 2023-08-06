
# HRPROTOPARSER

hrprotoparser stands for "Human Readable PROTOcol PARSER"

This is the core library to produce a network abstraction layer for communication.


# Why not procol buffers or flat buffers or zmq ?

This library aims to provide a trivially simple protocol, suited for embedded applications.

  * ZMQ is more like a socket abstraction, and even if it support request / reply, there is no such thing as "protocol" (but you can use hrp over zmq !)
  * Protocol buffers is interesting, but is not "that simple", and needs unpacking the data. It is the way to go in the general case, since it is widely used. HRP offers an even simpler protocol, eaiser to parse, and more oriented RPC.
  * Flat buffers : This one is a tough opponent since it is the official alternative to protocol buffers for performence oriented. It is However high-level oriented. HRP is low-level and mostly C-oriented, and its binary format is quite simpler than flat buffers.

Another benefit form HRPP is how it is architectured : one core library parsing the protocol file, and generated codes are simple skbs templates. This way, you can customize every aspect of the generated code with a trivial synthax.

# Installation

First install the packet with pip:

    pip install hrprotoparser

(Or `pip install .` if cloned from git).


Then you have to clone the skbs templates to generate protocols :

If you have cloned this repository from git, you only have to get the submodules with :

    git submodule update --init --recursive

Or if you installed from pypi, then clone the template repository only in some folder :

    git clone https://github.com/hl037/hrprotoparser-skbs-templates skbs-template

Then go to the directory

    cd skbs-template

and run :

    for i in hrpp*; do skbs install --symlink $i; done
    
...To install the templates.

Now, you can start using hrpp.


# Usage

To use one of the provided template, do the following :

    skbs gen @hrpp_C <dest> -- -p protocol.hrp

where `@hrpp_C` can be replaced by any hrpp template, and `<dest>` is the destination directory.

To get help, simply do :

    skbs gen @hrpp_C <dest> -- --help
  
You can also simply print the protocol content with :

    skbs gen @hrpp_C <dest> -- --info

# Synthax

The protocol sythax is close to the C/C++/Java family.

The protocol definition is entirely parseable using only regular expressions.

There are 5 statement types : Flag, Constant, Structure, Enumeration, and Packets.

Any text that doesn't match a statement is comment. (No // or # everywhere, you can document the protocol directly inside the definition).

## Flags

**Pattern : `F <FlagName> = <ConstantValue>`**

A flag is some kind of configuration. There are standard flags changing the binary format of the protocol encoding. See the "Standard Flags" section for more details.

## Constants

**Pattern : `C <Type> <ConstantName> = <ConstantValue> // Optionnal documentation comment`**

A constant can be used as an array size or a packet type.

## Enumerations

**Pattern : `E <EnumName> : <Type> {`**

**Pattern of an enum constant : `<ConstantName> = <ConstantValue> // Optionnal documentation comment`**

**Pattern of the block end : `}`**

An enumeration groups constants under a same specialized type. This is only pure semantic and the binary format of the protocol doesn't care if a value is an enum, or an integer / float.

## Struct

**Pattern : `S <Struct>  {`**

**Pattern of a struct field : `<Type> <FieldName> // Optionnal docummentation comment`**

**Pattern of the block end : `}`**

A structure groups reusable fields for packets. They can be nested at will.

## Packet

**Pattern : `<Direction> <PacketName> (<PacketType>) {`**

**Pattern of the fields and of the end of packet are the same as struct**

The `PacketType` is either directly an integer, or a constant name.

The Direction may be one of : 

  * `>`  "client to server"
  * `<`  "server to client"
  * `<>` "any direction"
  * [NOT IMPLEMENTED YET] `PeerA > PeerB` "PeerA to PeerB"
  * [NOT IMPLEMENTED YET] `PeerB < PeerA` "PeerB to PeerA" (a response)


# Datatypes

## Base datatype

  * `int8`/`char`, `uint8`/`byte` : signed and unsigned integer of 8 bits
  * `int16`, `uint16` : signed and unsigned integer of 16 bits
  * `int32`, `uint32` : signed and unsigned integer of 32 bits
  * `int64`, `uint64` : signed and unsigned integer of 64 bits
  * `float32` : floating point number using 32 bits
  * `float64` : floating point number using 64 bits

## Array types

Array are constructed recursively as `<Type>[<ItemCount>]`

**Note** : Multidimensionnal indice order is reversed compared to the C one : the first dimension is the right-most.

Any Base type, struct and array can be "arrayed".

Variable length arrays are only supported as last, optionnally nested, struct field. This is the same rule as the C programming language.
To make an array variable length, simply leave the <ItemCount> empty.

# Standard flags

## Flag `PSIZE`

Size of the header field specifying the packet size :

  * `-1` : Variable size of packet size : the packet size is a packed variable int. One should concatenate the 7 least signifient bits as long as the most significant bit is 1. The bytes are sent LSB first.
  * `0` : Deduced packet size : The packet size is deduced from the packet type. In this mode, use of variable length array is forbidden.
  * `n` with `n > 0` : Fixed size of packet size : The packet size field occupies n bytes

## Flag `TSIZE`

Size of header field specifying the packet type :

  * `-1` : Variable size of packet type : the pacjet type is packed as a variable int, with the same binary format as previously
  * `n` with `n > 0` : Fixed packet type size : The packet type field occupies n bytes.

# Binary format

The binary format of the protocol is very simple : 
It is the concatenation of the packet size (if one), the packet type, and the C binary representation of the structure on a little endian machine with an alignment of 1.

# Disclaimer

Some part of the code base is quite old (2014). It works but may not be the most beautiful code I've ever done... May be some day I will rewrite it from scratch...

# License

Copyright © 2014-2020 Léo Flaventin Hauchecorne

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

