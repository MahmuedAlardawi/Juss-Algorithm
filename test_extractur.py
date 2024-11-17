from RAG_PassageExtractor import PassageExtractor

# Passage extractor
passage_extractor = PassageExtractor()
retrieved_data = passage_extractor.extract_passages_sea_type('الطويل')

passage_extractor.display_passages(retrieved_data)
# passage_extractor.save_passages_to_json_file(retrieved_data)
