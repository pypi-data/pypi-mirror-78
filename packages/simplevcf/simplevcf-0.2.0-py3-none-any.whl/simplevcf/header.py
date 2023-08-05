import typing


class Header:
    """VCF Header
    """
    def __init__(self, header_lines: typing.List['HeaderLine'],
                 samples: typing.List[str]):
        super().__init__()
        self.header_lines = header_lines
        self.samples = samples
        self.info = {
            x.header_id: x
            for x in header_lines if x.header_tag == 'INFO'
        }
        self.format = {
            x.header_id: x
            for x in header_lines if x.header_tag == 'FORMAT'
        }
        self.contig = {
            x.header_id: x
            for x in header_lines if x.header_tag == 'contig'
        }

    def get_samples(self) -> typing.List[str]:
        return self.samples

    def get_header_lines(self) -> typing.List['HeaderLine']:
        return self.header_lines

    def get_info(self, info_id: str) -> typing.Optional['HeaderLine']:
        return self.info.get(info_id, None)

    def get_format(self, info_id: str) -> typing.Optional['HeaderLine']:
        return self.format.get(info_id, None)

    def get_contig(self, info_id: str) -> typing.Optional['HeaderLine']:
        return self.contig.get(info_id, None)

    @staticmethod
    def parse_header(lines: typing.List[str]) -> 'Header':
        header_lines = []
        for one_line in lines:
            if one_line.startswith('##'):
                header_lines.append(HeaderLine.parse(one_line))
            elif one_line.startswith('#'):
                elements = one_line.strip().split('\t')
                if len(elements) >= 10:
                    samples = elements[9:]
                else:
                    samples = []
        return Header(header_lines, samples)


class HeaderLine(typing.NamedTuple):
    """VCF Header line
    """

    line: str
    """Raw header line
    """

    header_tag: str
    """Header tag type (INFO, FORMAT...)
    """

    header_id: typing.Optional[str]
    """ID value in INFO/FORMAT
    """

    header_number: typing.Optional[str]
    """Nubmer value in INFO/FORMAT
    """

    header_type: typing.Optional[str]
    """Type value in INFO/FORMAT
    """

    header_description: typing.Optional[str]
    """Description value in INFO/FORMAT
    """

    header_contents: typing.Dict[str, str]
    """Dictionary of header contents
    """
    @staticmethod
    def parse(line: str) -> 'HeaderLine':
        """Parse single VCF Header

            Args:
                line: a header line
        """
        line = line.strip()
        if not line.startswith('##'):
            raise Exception('Header line should be started with ##')

        elements = line[2:].strip().split('=', 1)
        if len(elements) == 1:
            return HeaderLine(line, elements[0], None, None, None, None, {})
        tag, content_str = elements
        contents = _parse_content(content_str)

        return HeaderLine(line, tag, contents.get('ID', None),
                          contents.get('Number', None),
                          contents.get('Type', None),
                          contents.get('Description', None), contents)


def _parse_content(value: str) -> typing.Dict[str, str]:
    if not value.startswith('<') or not value.endswith('>'):
        return {"value": value}

    value = value[1:-1]

    contents = {}
    status = "key"
    current_key = ""
    current_value = ""
    for one in value:
        if status == "key":
            if one == "=":
                status = "value"
            else:
                current_key += one
        elif status == "value":
            if one == ",":
                contents[current_key] = current_value
                current_key = ""
                current_value = ""
                status = "key"
            elif one == "\"":
                status = "quote_value"
            else:
                current_value += one
        elif status == "quote_value":
            if one == "\"":
                status = "value"
            else:
                current_value += one
        else:
            raise Exception("unreachable")
    if current_key:
        contents[current_key] = current_value
    return contents
