def validate_uploaded_documents(uploaded_docs, requirements_message):
    """
    Validate the uploaded documents against the requirements_message.
    """
    try:
        required_docs = [req.strip() for req in requirements_message.split('\n') if req.strip() and (not req.startswith('Requirements for'))]
        identified_docs = set()
        extra_docs = []
        for doc in uploaded_docs:
            document_type = analyze_document_type(doc['path'], required_docs)
            if document_type in required_docs:
                identified_docs.add(document_type)
            else:
                extra_docs.append(doc['path'])
        missing_docs = [doc for doc in required_docs if doc not in identified_docs]
        results = []
        for doc in sorted(identified_docs):
            results.append(f'✅ {doc}')
        for doc in sorted(missing_docs):
            results.append(f'❌ {doc}')
        results.append('\n⚠️ Extra documents uploaded:')
        if extra_docs:
            results.extend((f'- {os.path.basename(doc)}' for doc in extra_docs))
        else:
            results.append('None')
        return ('\n'.join(results), 'green' if not missing_docs else 'red')
    except Exception as e:
        logger.error(f'Error validating documents: {e}')
        return (f'An error occurred: {str(e)}', 'red')
