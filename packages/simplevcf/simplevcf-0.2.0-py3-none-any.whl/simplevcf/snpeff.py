import typing
import simplevcf


class SnpEff(typing.NamedTuple):
    """SnpEff annotation representation
    """
    Allele: str
    Annotation: str
    Annotation_Impact: str
    Gene_Name: str
    Gene_ID: str
    Feature_Type: str
    Feature_ID: str
    Transcript_BioType: str
    Rank: str
    HGVS_c: str
    HGVS_p: str
    cDNA_pos__cDNA_length: str
    CDS_pos__CDS_length: str
    AA_pos__AA_length: str
    Distance: str
    ERRORS: str

    @staticmethod
    def parse(record: simplevcf.Record) -> typing.List['SnpEff']:
        """Parse VCF record

           Args:
               record: A VCF record
        """
        if 'ANN' in record.INFO:
            return [SnpEff(*x.split('|')) for x in record.INFO['ANN']]
        return []
