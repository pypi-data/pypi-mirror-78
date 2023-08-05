#!/usr/bin/env python3

import unittest
import simplevcf
import simplevcf.snpeff
import os.path
import io


class TestVCFReader(unittest.TestCase):
    def test_printer(self):
        test_file = os.path.join(os.path.dirname(__file__), "NA12878.vcf")

        with simplevcf.vcfopen(
                test_file) as reader, io.StringIO() as output_text:
            writer = simplevcf.Writer(output_text, reader.get_header())
            for one in reader:
                print(one.INFO['AC'],
                      one.CALL['ERP107576_NovaSeq_SAMEA104707359']['GT'][0],
                      file=output_text)

    def test_read(self):
        test_file = os.path.join(os.path.dirname(__file__), "NA12878.vcf")

        records = []

        with simplevcf.vcfopen(
                test_file) as reader, io.StringIO() as output_text:
            writer = simplevcf.Writer(output_text, reader.get_header())

            for one in reader:
                # print(one)
                records.append(one)
                writer.write_record(one)

            self.assertEqual(reader.get_samples(), [
                "ERP107576_NovaSeq_SAMEA104707359",
                "SRP174470_NovaSeq_SRR8454589",
                "ERP107576_BGISeq-500_SAMEA104707357",
                "ERP001775_HiSeq2000_SAMEA1531955-1"
            ])

            with open(test_file, encoding='utf-8') as f:
                original = f.read()
            self.assertEqual(original, output_text.getvalue())
        # print(output_text.getvalue())

        self.assertEqual(6, len(records))
        self.assertEqual(records[0].ID, None)
        self.assertEqual(records[0].FILTER, None)
        self.assertEqual(records[0].INFO['FLAG'], True)

        self.assertEqual(
            records[3],
            simplevcf.Record(
                CHROM="4",
                POS=3076603,
                ID='foo',
                REF="CCAGCAGCAG",
                ALT=["CCAGCAG", "C"],
                QUAL="15011.2",
                FILTER='PASS',
                INFO={
                    'AC': ['3', '2'],
                    'AF': ['0.375', '0.25'],
                    'AN': ['8'],
                    'BaseQRankSum': ['0'],
                    'DP': ['996'],
                    'ExcessHet': ['0.0011'],
                    'FS': ['4.293'],
                    'InbreedingCoeff': ['0.7265'],
                    'MLEAC': ['50', '37'],
                    'MLEAF': ['0.521', '0.385'],
                    'MQ': ['59.89'],
                    'MQRankSum': ['0.967'],
                    'QD': ['28.68'],
                    'ReadPosRankSum': ['-0.524'],
                    'SOR': ['1.23'],
                    'ANN': [
                        'C|disruptive_inframe_deletion|MODERATE|HTT|ENSG00000197386.12_9|transcript|ENST00000355072.10_2|protein_coding|1/67|c.102_110delGCAGCAGCA|p.Gln35_Gln37del|247/13475|102/9429|34/3142||INFO_REALIGN_3_PRIME',
                        'CCAGCAG|disruptive_inframe_deletion|MODERATE|HTT|ENSG00000197386.12_9|transcript|ENST00000355072.10_2|protein_coding|1/67|c.108_110delGCA|p.Gln37del|253/13475|108/9429|36/3142||INFO_REALIGN_3_PRIME',
                        'C|upstream_gene_variant|MODIFIER|HTT-AS|ENSG00000251075.2_8|transcript|ENST00000664062.1_2|pseudogene||n.-347_-339delCTGCTGCTG|||||339|',
                        'CCAGCAG|upstream_gene_variant|MODIFIER|HTT-AS|ENSG00000251075.2_8|transcript|ENST00000664062.1_2|pseudogene||n.-347_-345delCTG|||||345|'
                    ],
                    'NS': ['4'],
                    'MAF': ['0.375', '0.25'],
                    'AC_Het': ['1', '2'],
                    'AC_Hom': ['2', '0'],
                    'AC_Hemi': ['0', '0'],
                    'HWE': ['0.428571', '1'],
                    'ExcHet': ['1', '0.8']
                },
                FORMAT=['GT', 'AD', 'DP', 'GQ', 'PL'],
                CALL={
                    'ERP107576_NovaSeq_SAMEA104707359': {
                        'GT': ['1/2'],
                        'AD': ['0', '17', '9'],
                        'DP': ['26'],
                        'GQ': ['99'],
                        'PL': ['923', '360', '507', '604', '0', '907']
                    },
                    'SRP174470_NovaSeq_SRR8454589': {
                        'GT': ['1/1'],
                        'AD': ['0', '4', '0'],
                        'DP': ['4'],
                        'GQ': ['12'],
                        'PL': ['150', '12', '0', '150', '12', '150']
                    },
                    'ERP107576_BGISeq-500_SAMEA104707357': {
                        'GT': ['0/0'],
                        'AD': ['13', '0', '0'],
                        'DP': ['13'],
                        'GQ': ['27'],
                        'PL': ['0', '27', '405', '27', '405', '405']
                    },
                    'ERP001775_HiSeq2000_SAMEA1531955-1': {
                        'GT': ['0/2'],
                        'AD': ['3', '0', '6'],
                        'DP': ['9'],
                        'GQ': ['73'],
                        'PL': ['212', '221', '313', '0', '92', '73']
                    }
                }))


if __name__ == '__main__':
    unittest.main()
