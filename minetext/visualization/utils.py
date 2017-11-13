def match_documents(source, target, comparable_field_source="id", comparable_field_target="id_str"):
    matched_documents = list()
    for document in source[:1]:
        for target_document in target[:50]:
            if document[comparable_field_source] == target_document[comparable_field_target]:
                matched_documents.append(target_document)
                break
    return matched_documents
