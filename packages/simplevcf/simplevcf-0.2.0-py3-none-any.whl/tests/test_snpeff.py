#!/usr/bin/env python3

import unittest
import simplevcf
import simplevcf.snpeff
import os.path
import io


class TestSnpEff(unittest.TestCase):
    def test_snpeff(self):
        test_file = os.path.join(os.path.dirname(__file__), "NA12878.vcf")

        records = []

        with simplevcf.vcfopen(test_file) as reader:
            for one in reader:
                records.append(one)

        snpeff = simplevcf.snpeff.SnpEff.parse(records[3])
        self.assertEqual(snpeff, [
            simplevcf.snpeff.SnpEff(
                'C', 'disruptive_inframe_deletion', 'MODERATE', 'HTT',
                'ENSG00000197386.12_9', 'transcript', 'ENST00000355072.10_2',
                'protein_coding', '1/67', 'c.102_110delGCAGCAGCA',
                'p.Gln35_Gln37del', '247/13475', '102/9429', '34/3142', '',
                'INFO_REALIGN_3_PRIME'),
            simplevcf.snpeff.SnpEff(
                'CCAGCAG', 'disruptive_inframe_deletion', 'MODERATE', 'HTT',
                'ENSG00000197386.12_9', 'transcript', 'ENST00000355072.10_2',
                'protein_coding', '1/67', 'c.108_110delGCA', 'p.Gln37del',
                '253/13475', '108/9429', '36/3142', '',
                'INFO_REALIGN_3_PRIME'),
            simplevcf.snpeff.SnpEff(
                'C', 'upstream_gene_variant', 'MODIFIER', 'HTT-AS',
                'ENSG00000251075.2_8', 'transcript', 'ENST00000664062.1_2',
                'pseudogene', '', 'n.-347_-339delCTGCTGCTG', '', '', '', '',
                '339', ''),
            simplevcf.snpeff.SnpEff(
                'CCAGCAG', 'upstream_gene_variant', 'MODIFIER', 'HTT-AS',
                'ENSG00000251075.2_8', 'transcript', 'ENST00000664062.1_2',
                'pseudogene', '', 'n.-347_-345delCTG', '', '', '', '', '345',
                '')
        ])
        self.assertEqual(snpeff[0].Allele, 'C')
        self.assertEqual(snpeff[0].Annotation, 'disruptive_inframe_deletion')
        self.assertEqual(snpeff[0].Annotation_Impact, 'MODERATE')
        self.assertEqual(snpeff[0].Gene_Name, 'HTT')
        self.assertEqual(snpeff[0].Gene_ID, 'ENSG00000197386.12_9')
        self.assertEqual(snpeff[0].Feature_Type, 'transcript')
        self.assertEqual(snpeff[0].Feature_ID, 'ENST00000355072.10_2')
        self.assertEqual(snpeff[0].Transcript_BioType, 'protein_coding')
        self.assertEqual(snpeff[0].Rank, '1/67')
        self.assertEqual(snpeff[0].HGVS_c, 'c.102_110delGCAGCAGCA')
        self.assertEqual(snpeff[0].HGVS_p, 'p.Gln35_Gln37del')
        self.assertEqual(snpeff[0].cDNA_pos__cDNA_length, '247/13475')
        self.assertEqual(snpeff[0].CDS_pos__CDS_length, '102/9429')
        self.assertEqual(snpeff[0].AA_pos__AA_length, '34/3142')
        self.assertEqual(snpeff[0].Distance, '')
        self.assertEqual(snpeff[0].ERRORS, 'INFO_REALIGN_3_PRIME')
