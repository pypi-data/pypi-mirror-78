from tokenizer_tools.format_converter.corpus_to_rasa_json import CorpusToRasaJson


def conllx_to_rasa(conllx_file, output_rasa):
    converter = CorpusToRasaJson.read_from_file(conllx_file)
    converter.convert_to_file(output_rasa)
