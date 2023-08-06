import pytest
from prepnlp.semeval import Semeval2014
from prepnlp.base import AspectTerm
from unittest.mock import Mock, MagicMock


def test_bio_from_bert_tokenized_sentence__when_input_len_and_offsets_len_not_equal():
    with pytest.raises(Exception):
        Semeval2014.bio_from_bert_tokenized_sentence([1, 2], [(0, 1)])


def test_bio_from_bert_tokenized_sentence_when_no_aspect():
    result = Semeval2014.bio_from_bert_tokenized_sentence(
        [1, 2],
        [(0, 1), (2, 3)],
        []
    )

    assert all([r == 'O' for r in result])


def test_bio_from_bert_tokenized_sentence_with_one_aspect():
    inputs = [1, 2]
    result = Semeval2014.bio_from_bert_tokenized_sentence(
        inputs,
        [(0, 1), (2, 3)],
        [AspectTerm('term', offset_start=0, offset_end=1, polarity='positive')]
    )
    assert len(result) == len(inputs)
    assert result[0] == 'B-ASPECT-POS'


def test_bio_from_bert_tokenized_sentence_with_mwe_aspect():
    inputs = [1, 2]
    result = Semeval2014.bio_from_bert_tokenized_sentence(
        inputs,
        [(0, 1), (2, 3)],
        [AspectTerm('term', offset_start=0, offset_end=2, polarity='positive')]
    )
    assert len(result) == len(inputs)
    assert result[0] == 'B-ASPECT-POS'
    assert result[1] == 'I-ASPECT-POS'


def test_bio_from_bert_tokenized_sentence_with_mwe2_aspect():
    inputs = [1, 2]
    result = Semeval2014.bio_from_bert_tokenized_sentence(
        inputs,
        [(0, 1), (2, 3)],
        [AspectTerm('term', offset_start=0, offset_end=3, polarity='positive')]
    )
    assert len(result) == len(inputs)
    assert result[0] == 'B-ASPECT-POS'
    assert result[1] == 'I-ASPECT-POS'


def test_bio_from_bert_tokenized_sentence_with_2_aspects():
    inputs = [1, 2, 3, 4]
    result = Semeval2014.bio_from_bert_tokenized_sentence(
        inputs,
        [(0, 1), (2, 3), (4, 5), (6, 7)],
        [AspectTerm('term', offset_start=1, offset_end=2, polarity='negative'),
         AspectTerm('term', offset_start=4, offset_end=5, polarity='positive')]
    )
    assert len(result) == len(inputs)
    assert result[0] == 'B-ASPECT-NEG'
    assert result[1] == 'I-ASPECT-NEG'
    assert result[2] == 'B-ASPECT-POS'
    assert result[3] == 'O'


def test_bio_from_bert_tokenized_sentence_with_2_mwe_aspects():
    inputs = [1, 2, 3, 4, 5, 6, 7]
    result = Semeval2014.bio_from_bert_tokenized_sentence(
        inputs,
        [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13)],
        [AspectTerm('term', offset_start=3, offset_end=4, polarity='negative'),
         AspectTerm('term', offset_start=7, offset_end=10, polarity='positive')]
    )
    expected = ['O', 'B-ASPECT-NEG', 'I-ASPECT-NEG', 'B-ASPECT-POS', 'I-ASPECT-POS', 'I-ASPECT-POS', 'O']
    assert all(le == r for le, r in zip(result, expected))


def test__create_absa_doc():
    expected_text = 'some text here, nothing more'
    expected_id = 300

    def get_attribute_side_effect(inp):
        if inp == 'id':
            return '{}'.format(expected_id)
        return None

    def getElementsByTagName_side_effect(inp):
        if inp == 'text':
            r = MagicMock()
            r.firstChild = MagicMock()
            r.firstChild.nodeValue = expected_text
            return [r]
        if inp == 'aspectTerm':
            def _aspect_get_attribute(inp):
                if inp == 'term':
                    return 'some'
                if inp == 'polarity':
                    return 'neutral'
                if inp == 'from':
                    return '{}'.format(0)
                if inp == 'to':
                    return '{}'.format(3)
                return None

            r = MagicMock()
            r.getAttribute = MagicMock(side_effect=_aspect_get_attribute)
            return [r]
        return None

    xml_sentence_node = Mock()
    xml_sentence_node.getAttribute = MagicMock(side_effect=get_attribute_side_effect)
    xml_sentence_node.getElementsByTagName = MagicMock(side_effect=getElementsByTagName_side_effect)
    result = Semeval2014._create_absa_doc(xml_sentence_node)

    assert result.text == expected_text
    assert result.doc_id == expected_id
    assert len(result.aspect_terms) == 1
    first_aspect = result.aspect_terms[0]
    assert first_aspect.term == 'some'
    assert first_aspect.sentiment == 'neutral'
    assert first_aspect.offset_start == 0
    assert first_aspect.offset_end == 3
    assert first_aspect.doc_id == expected_id
