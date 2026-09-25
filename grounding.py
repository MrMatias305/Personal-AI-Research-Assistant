def validate_claims(research):
    valid_source_ids = [source.id for source in research.sources]
    validation_results = []

    for claim in research.claims:
        missing_values = [
            source_id
            for source_id in claim.source_ids
            if source_id not in valid_source_ids
        ]

        validation_results.append(
            {
                "claim": claim.text,
                "valid": len(missing_values) == 0,
                "missing_sources": missing_values,
            }
        )

    return validation_results
