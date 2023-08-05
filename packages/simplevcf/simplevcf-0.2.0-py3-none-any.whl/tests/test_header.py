#!/usr/bin/env python3

import unittest
import simplevcf
import simplevcf.header
import os.path
import io


class TestHeader(unittest.TestCase):
    def test_parse(self):
        result = simplevcf.header._parse_content(
            '<ID=MLEAF,Number=A,Type=Float,Description="Maximum likelihood expectation (MLE) for the allele frequency (not necessarily the same as the AF), for each ALT allele, in the same order as listed">'
        )
        self.assertEqual(
            result, {
                'ID':
                'MLEAF',
                'Number':
                'A',
                'Type':
                'Float',
                'Description':
                'Maximum likelihood expectation (MLE) for the allele frequency (not necessarily the same as the AF), for each ALT allele, in the same order as listed'
            })

        result = simplevcf.header._parse_content('VCFv4.2')
        self.assertEqual(result, {'value': 'VCFv4.2'})

    def test_parse_header_all(self):
        test_file = os.path.join(os.path.dirname(__file__), "NA12878.vcf")

        with simplevcf.vcfopen(test_file) as reader:
            self.assertEqual(
                reader.get_header().get_info('AC'),
                simplevcf.header.HeaderLine(
                    '##INFO=<ID=AC,Number=A,Type=Integer,Description="Allele count in genotypes, for each ALT allele, in the same order as listed">',
                    'INFO', 'AC', 'A', 'Integer',
                    'Allele count in genotypes, for each ALT allele, in the same order as listed',
                    {
                        'ID':
                        'AC',
                        'Number':
                        'A',
                        'Type':
                        'Integer',
                        'Description':
                        'Allele count in genotypes, for each ALT allele, in the same order as listed'
                    }))

            self.assertEqual(
                reader.get_header().get_format('AD'),
                simplevcf.header.HeaderLine(
                    '##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths for the ref and alt alleles in the order listed">',
                    'FORMAT', 'AD', 'R', 'Integer',
                    'Allelic depths for the ref and alt alleles in the order listed',
                    {
                        'ID':
                        'AD',
                        'Number':
                        'R',
                        'Type':
                        'Integer',
                        'Description':
                        'Allelic depths for the ref and alt alleles in the order listed'
                    }))

            self.assertEqual(
                reader.get_header().get_contig('13'),
                simplevcf.header.HeaderLine(
                    '##contig=<ID=13,length=115169878>', 'contig', '13', None,
                    None, None, {
                        'ID': '13',
                        'length': '115169878'
                    }))
