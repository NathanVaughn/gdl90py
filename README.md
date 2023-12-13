# GDL90Py

This is a Python 3 encoder/decoder for Garmin DataLink (GDL) 90 messages.
Some 3rd party message formats (like ForeFlight) are also supported.

***Use at your own risk. This is provided as-is and is not intended for any
sort of safety-of-flight critical application.*** I made this for my own learning,
and use with flight simulators.

Inspired by [etdey/gdl90](https://github.com/etdey/gdl90).

## Usage

### Creating a message

Import the specific message class you want, initialize the class, and run `.serialize()`.
Example:

```python
>>> from gdl90py.messages.height_above_terrain import HeightAboveTerrainMessage
>>> hat = HeightAboveTerrainMessage(height_above_terrain=3000)
>>> hat.serialize()
b'~\x90\xd0\x1d\x89Y~'
```

With `.serialize()`, there is 1 option, which is whether or not to prepare the data
with the Least Significant Bit first (default is True).

GDL90 states that bytes should be sent with the Least Significant Bit first.
As an example, the number 234 is traditionally represented as `11101010` in binary.
The rightmost-digit is the least significant as it represents 1, and then the digit
to the left represents 2, etc. This is pretty common. With a Least Significant Bit
first structure, 234 would instead be sent over the wire as `01010111`.

This setting restructures the data to correctly send the Least Significant Bit first.
However, Python and most programs assume Most Significant Bit first so this can
create some confusion. 234 will instead be interpreted as 87 or its byte or hexadecimal
equivalent. Turn this setting off if you want to view data as Most Significant Bit
first bytes.

When a message is serialized some coercion is done. For example, if you provide
a latitude or longitude value that is outside the acceptable range, this will
automatically be converted to the standard invalid value. Other values like
a device name will be automatically cut down to the maximum allowable length.
A few values like a traffic ADS-B address are not silently ignored if the values
are incorrect as this likely would be due to a far more important issue.

Basically, just because you can instantiate the message class, does not mean
it will serialize without error!

### Parsing a message

For a stream of `bytes` data that could contain multiple messages, use
`gdl90py.parser.parse_messages`. If you only have the `bytes` for a single
message, you can use `gdl90py.parser.parse_message`. Example:

```python
>>> import pprint
>>> from gdl90py.parser import parse_messages
>>> msgs = parse_messages(b'~\t\x0b\xb8\x91\x9a~')
>>> pprint.pprint(msgs[0])
HeightAboveTerrainMessage(height_above_terrain=3000)
```

Both functions have 2 options. The first denotes whether the incoming
`bytes` data is structured with the Most Significant Bit first (default is True).
This is likely the case unless you're handling raw bits.

The second option is to ignore messages that are not recognized (default is False).
This will prevent an exception being raised if a message is encountered that
it doesn't know how to parse.

Malformed messages will always cause an exception.

No checks are done on the parsed data, so values exceeding limits on certain fields
may be parsed (for example, a time of reception exceeding 1 second)!

## FAQ

### Are you planning on adding support for X device?

No.

### Can this parse messages from a Sentry?

No. While I was able to get my hands on one and take a packet capture, it uses an
undocumented set of messages I have been unable to reverse-engineer.
