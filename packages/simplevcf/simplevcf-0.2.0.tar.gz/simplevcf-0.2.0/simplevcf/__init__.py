#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simple Pure Python VCF Parser
"""

import argparse
import collections
import typing
from typing import Sequence
import re
import gzip
import simplevcf.header

BAD_INFO_CHAR = re.compile(r'[;=,\s]')
BAD_FORMAT_CHAR = re.compile(r'[:,\s]')


class Record(typing.NamedTuple):
    """VCF Record

    Use `parse` method to parse VCF line
    """

    CHROM: str
    """Chromosome name
    """

    POS: int
    """VCF entry position
    """

    ID: typing.Optional[str]
    """VCF entry ID
    """

    REF: str
    """Reference sequence
    """

    ALT: typing.List[str]
    """Alternative sequences
    """

    QUAL: typing.Optional[str]
    """Quality score
    """

    FILTER: typing.Optional[str]
    """VCF entry Filter
    """

    INFO: typing.Dict[str, typing.Any]
    """Parsed VCF INFO record
    """

    FORMAT: typing.List[str]
    """Parsed VCF FORMAT record
    """

    CALL: typing.Dict[str, typing.Dict[str, typing.Any]]
    """Called genotype
    """
    @staticmethod
    def parse(line: str, samples: typing.Iterable[str]) -> 'Record':
        """Parse VCF line and convert to Record object

           Args:
               line: A VCF line
               samples: A list of sample names
        """
        elements = line.strip().split('\t')
        CHROM = elements[0]
        POS = int(elements[1])
        ID = _value_or_empty(elements[2])
        REF = elements[3]
        ALT = elements[4].split(',') if elements[4] != '.' else []
        QUAL = _value_or_empty(elements[5])  # QUAL
        FILTER = _value_or_empty(elements[6])  # FILTER

        if len(elements) >= 8:
            INFO: typing.Dict[str, typing.Any] = {
                y[0]: y[1].split(',') if len(y) > 1 else True
                for y in [x.split('=', 1) for x in elements[7].split(';')]
            }  # INFO
        else:
            INFO = {}

        if len(elements) >= 9:
            FORMAT = elements[8].split(':') if elements[8] != '.' else [
            ]  # FORMAT
        else:
            FORMAT = []

        CALL = {}
        if samples:
            for x, y in zip(samples, elements[9:]):
                one_call = dict()
                for k, v in zip(FORMAT, y.split(':')):
                    one_call[k] = v.split(',')
                CALL[x] = one_call

        return Record(CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO, FORMAT,
                      CALL)

    def to_line(self, samples: typing.List[str]) -> str:
        """Convert to VCF line

           Args:
               samples: Sample names
        """
        columns = [
            self.CHROM,
            str(self.POS),
            _dot_for_none(self.ID),
            _dot_for_none(self.REF), ','.join(self.ALT) if self.ALT else '.',
            _dot_for_none(self.QUAL),
            _dot_for_none(self.FILTER), ';'.join([
                x[0] if x[1] == True else x[0] + '=' + ','.join(x[1])
                for x in self.INFO.items()
            ])
        ]

        if samples:
            columns += [':'.join(self.FORMAT)] + [
                ':'.join([
                    ','.join(self.CALL[x][y]) if y in self.CALL[x] else '.'
                    for y in self.FORMAT
                ]) for x in samples
            ]

        return '\t'.join(columns)


class Reader:
    """VCF Reader

       Args:
           stream: file-like object
    """
    def __init__(self, stream: typing.IO[typing.Any]):
        header_lines = []

        for i, line in enumerate(stream):
            if line.startswith('##'):
                header_lines.append(line)
            elif line.startswith('#'):
                header_lines.append(line)
                break
            else:
                break
        self.header = simplevcf.header.Header.parse_header(header_lines)
        self.stream = stream

    def __iter__(self):
        return self

    def __next__(self) -> Record:
        return Record.parse(self.stream.__next__(), self.header.samples)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.close()

    def get_samples(self) -> typing.List[str]:
        """Get sample name list
        """
        return self.header.get_samples()

    def get_header(self) -> simplevcf.header.Header:
        """Get header
        """
        return self.header


class Writer:
    """VCF Writer

       Args:
           stream: file-like object
           headers: A sequence of header lines
           samples: A list of sample names    
    """
    def __init__(self, stream: typing.IO[typing.Any],
                 header: simplevcf.header.Header):
        self.samples = header.get_samples()
        self.stream = stream

        for line in header.get_header_lines():
            print(line.line.strip(), file=self.stream)
        if self.samples:
            print('\t'.join([
                '#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO',
                'FORMAT'
            ] + self.samples),
                  file=self.stream)
        else:
            print('\t'.join([
                '#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO'
            ]),
                  file=self.stream)

    def write_record(self, record: Record):
        """Write VCF record

           Args:
                record: VCF record
        """
        print(record.to_line(self.samples), file=self.stream)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.close()


def _value_or_empty(value: str) -> typing.Optional[str]:
    if value == '.':
        return None
    return value


def _dot_for_none(value: typing.Optional[str]) -> str:
    if value:
        return value
    return '.'


def vcfopen(filename: str) -> Reader:
    """Open VCF file

       Args:
           filename: A VCF file name
    """
    if filename.endswith('.gz'):
        return Reader(gzip.open(filename, 'rt', encoding='utf-8'))
    else:
        return Reader(open(filename, 'r', encoding='utf-8'))
