ENTITY_TYPES = {
    "person",
    "company",
    "organisation",
    "vessel",
    "aircraft",
}
FILTER_LIST_TYPES = {
    "sanction",
    "warning",
    "fitness-probity",
    "pep",
    "pep-class-1",
    "pep-class-2",
    "pep-class-3",
    "pep-class-4",
    "adverse-media",
    "adverse-media-financial-crime",
    "adverse-media-violent-crime",
    "adverse-media-sexual-crime",
    "adverse-media-terrorism",
    "adverse-media-fraud",
    "adverse-media-narcotics",
    "adverse-media-general",
}
SORT_BY_QUERY_PARAMS = {"id", "created_at", "updated_at", "assignee_id", "searcher_id"}
SORT_DIR_QUERY_PARAMS = {"ASC", "DESC"}
RISK_LEVEL = {"low", "medium", "high", "unknown"}
MATCH_STATUS = {
    "no_match",
    "false_positive",
    "potential_match",
    "true_positive",
    "unknown",
}
MONITORED = {"suspended", "un-suspended", "false"}
