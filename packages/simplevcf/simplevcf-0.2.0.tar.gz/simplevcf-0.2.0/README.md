# simplevcf

[![Python package](https://github.com/informationsea/simplevcf-py/workflows/Python%20package/badge.svg)](https://github.com/informationsea/simplevcf-py/actions)
[![PyPI](https://img.shields.io/pypi/v/simplevcf)](https://pypi.org/project/simplevcf/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/simplevcf)](https://pypi.org/project/simplevcf/)
[![PyPI - License](https://img.shields.io/pypi/l/simplevcf)](https://pypi.org/project/simplevcf/)
[![PyPI - Format](https://img.shields.io/pypi/format/simplevcf)](https://pypi.org/project/simplevcf/)
[![PyPI - Status](https://img.shields.io/pypi/status/simplevcf)](https://pypi.org/project/simplevcf/)

Simple VCF parser/writer with pure python

[Documentation](https://informationsea.github.io/simplevcf-py/)

## Examples

### Read VCF

```python
    with simplevcf.vcfopen('some.vcf.gz') as reader:
        for record in reader:
            # process a record
```


### Read, manipulate and write

```python
    with simplevcf.vcfopen('some.vcf.gz') as reader, with open('output.vcf) as f:
        writer = simplevcf.Writer(f, reader.headers,
                                  reader.samples)
        for record in reader:
            # manipulate a record
            writer.write_record(one)
```

### Access to INFO and CALL

```python
    with simplevcf.vcfopen(test_file) as reader:
        for one in reader:
            print(
                one.INFO['AC'], one.CALL['ERP107576_NovaSeq_SAMEA104707359']['GT'][0])
```