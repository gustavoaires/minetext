def match_documents(source, target, comparable_field="id"):
    matched_documents = list()
    for document in source:
        if type(document) is dict:
            for target_document in target:
                if type(target_document) is dict:
                    if str(document[comparable_field]) == str(target_document[comparable_field]):
                        matched_documents.append(target_document)
                        break
    return matched_documents
