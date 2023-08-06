from xml.dom import minidom
from prepnlp.base import AbsaDoc, AspectTerm
from typing import List, Tuple


class Semeval(object):
    POLARITY_MAP = {
        'positive': 'POS',
        'negative': 'NEG',
        'neutral': 'NEU'
    }
    LABEL_VOCAB = {
        'O': 0,
        'B-ASPECT-POS': 1,
        'I-ASPECT-POS': 2,
        'B-ASPECT-NEG': 3,
        'I-ASPECT-NEG': 4,
        'B-ASPECT-NEU': 5,
        'I-ASPECT-NEU': 6,
    }

    LABEL_VOCAB_NO_POLAR = {
        'O': 0,
        'B-ASPECT': 1,
        'I-ASPECT': 2
    }

    def __init__(self):
        pass

    @staticmethod
    def _create_absa_doc(xml_sentence_node) -> AbsaDoc:
        doc_id = int(xml_sentence_node.getAttribute('id'))
        doc_text = xml_sentence_node.getElementsByTagName('text')[0].firstChild.nodeValue
        absa_doc = AbsaDoc(text=doc_text, doc_id=doc_id)

        # add all aspect terms
        for aspect_term in xml_sentence_node.getElementsByTagName('aspectTerm'):
            term = aspect_term.getAttribute('term')
            sentiment = aspect_term.getAttribute('polarity')
            from_idx = int(aspect_term.getAttribute('from'))
            to_idx = int(aspect_term.getAttribute('to'))

            absa_doc.add_aspect_term(
                AspectTerm(
                    term=term,
                    offset_start=from_idx,
                    offset_end=to_idx,
                    polarity=sentiment,
                    doc_id=doc_id
                )
            )
        return absa_doc

    @staticmethod
    def loads_xml(xml_doc_path: str) -> list:
        xml_doc = minidom.parse(xml_doc_path)
        sentences_xml = xml_doc.getElementsByTagName('sentence')
        documents = list()
        for xml_sentence_node in sentences_xml:
            documents.append(Semeval._create_absa_doc(xml_sentence_node))

        return documents

    @staticmethod
    def _is_intersect_with(aspect_term: AspectTerm, token_offset_start, token_offset_end):
        return (
                aspect_term.offset_start <= token_offset_start <= aspect_term.offset_end or
                aspect_term.offset_start <= token_offset_end <= aspect_term.offset_end
        )

    @staticmethod
    def _should_go_to_next_aspect(aspect_term: AspectTerm, token_offset_start):
        return aspect_term.offset_end <= token_offset_start

    @staticmethod
    def bio_from_bert_tokenized_sentence(tokenized_sentence_input_ids: List, offset_mappings: List[Tuple[int, int]],
                                         aspect_terms: List[AspectTerm], with_polarity: bool = True,
                                         with_cls: bool = False, cls_token_id: int = 101) -> List[str]:
        """

        :param tokenized_sentence_input_ids:
        :param offset_mappings:
        :param aspect_terms:
        :param with_polarity:
        :param with_cls:
        :param cls_token_id:
        :return:
        """
        assert len(tokenized_sentence_input_ids) == len(offset_mappings)

        if not aspect_terms or len(aspect_terms) == 0:
            return ['O'] * len(tokenized_sentence_input_ids)

        i = 0
        aspect_term = aspect_terms[i]
        is_begin_aspect = True
        result = list()
        for t, (token, offset_mapping) in enumerate(zip(tokenized_sentence_input_ids, offset_mappings)):
            offset_start, offset_end = offset_mapping

            if with_cls and token == cls_token_id:
                result.append('O')
                continue

            if t < len(tokenized_sentence_input_ids) and Semeval._is_intersect_with(aspect_term,
                                                                                    offset_start,
                                                                                    offset_end):
                polarity = Semeval.POLARITY_MAP.get(aspect_term.sentiment, 'NEU')
                base_tag = 'I-ASPECT'
                if is_begin_aspect:
                    base_tag = 'B-ASPECT'
                    is_begin_aspect = False

                tag = base_tag
                if with_polarity:
                    tag = '{}-{}'.format(base_tag, polarity)

                result.append(tag)

            else:
                result.append('O')

            if Semeval._should_go_to_next_aspect(aspect_term, offset_start):
                is_begin_aspect = True
                i += 1
                if i < len(aspect_terms):
                    aspect_term = aspect_terms[i]

        return result

    @staticmethod
    def bio_to_ids(bios: list, with_polarity: bool = True):
        """

        :param bios:
        :param with_polarity:
        :return:
        """
        mapping = Semeval.LABEL_VOCAB_NO_POLAR
        if with_polarity:
            mapping = Semeval.LABEL_VOCAB

        return [mapping.get(bio_tag) for bio_tag in bios]
