def match_documents(source, target, comparable_field="id"):
    matched_documents = list()
    for document in source[:1]:
        for target_document in target[:50]:
            if str(document[comparable_field]) == str(target_document[comparable_field]):
                matched_documents.append(target_document)
                break
    return matched_documents
