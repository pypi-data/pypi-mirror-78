import re
import logging

logger = logging.getLogger('MARKDOWN')

from markdown import Extension
from markdown.preprocessors import Preprocessor
import xml.etree.ElementTree as etree
from markdown.blockparser import BlockParser
from markdown.blockprocessors import BlockProcessor

class DivClassProcessor(BlockProcessor):
    '''
    =class:container=
    hey there
    kdoksd
    skdsk
    =endclass=
    '''
    CLASS_BOUNDARY_START = r'=class:([a-zA-Z0-9\-]+)='
    CLASS_BOUNDARY_END = r'=endclass='

    def test(self, parent, block):
        return re.match(self.CLASS_BOUNDARY_START, block)

    def run(self, parent, blocks):
        original_block = blocks[0]
        compiled_regex = re.compile(self.CLASS_BOUNDARY_START)
        class_name = compiled_regex.findall(blocks[0])[0]
        blocks[0] = re.sub(self.CLASS_BOUNDARY_START, '', blocks[0])
        for block_num, block in enumerate(blocks):
            if re.search(self.CLASS_BOUNDARY_END, block):
                blocks[block_num] = re.sub(self.CLASS_BOUNDARY_END, '', block)
                e = etree.SubElement(parent, 'div')
                e.set('class', class_name)
                self.parser.parseBlocks(e, blocks[0:block_num+1])
                for i in range(0, block_num+1):
                    blocks.pop(0)
                return True
        blocks[0] = original_block
        return False

class AddDivClassExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(DivClassProcessor(md.parser), 'add-div-class', 90)
