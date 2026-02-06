"""
SEAD 4 Guideline Knowledge Base
Simplified excerpts from actual SEAD 4 Adjudicative Guidelines
"""

SEAD4_GUIDELINES = {
    "G": {
        "title": "Guideline G: Alcohol Consumption",
        "concern": (
            "Excessive alcohol consumption often leads to the exercise of questionable judgment "
            "or the failure to control impulses, and can raise questions about an individual's "
            "reliability and trustworthiness."
        ),
        "disqualifying_conditions": [
            "Alcohol-related incidents away from work, such as driving while under the influence",
            "Habitual or binge consumption of alcohol to the point of impaired judgment",
            "Diagnosis by a medical professional of alcohol use disorder",
        ],
        "mitigating_conditions": [
            "So much time has passed since the incident that it is unlikely to recur",
            "The individual acknowledges the issue and has taken steps (e.g., counseling, AA)",
            "A favorable prognosis by a qualified medical professional",
        ],
        "citation": "SEAD 4, Adjudicative Guidelines, Paragraph 21"
    },
    
    "H": {
        "title": "Guideline H: Drug Involvement and Substance Misuse",
        "concern": (
            "The illegal use of controlled substances can raise questions about an individual's "
            "ability or willingness to comply with laws, rules, and regulations."
        ),
        "disqualifying_conditions": [
            "Any drug abuse (use of illegal drugs or prescription drugs without authorization)",
            "Testing positive for illegal drug use",
            "Illegal drug possession, including cultivation, processing, or distribution",
        ],
        "mitigating_conditions": [
            "The behavior happened so long ago or under such unusual circumstances that recurrence is unlikely",
            "A demonstrated intent not to abuse drugs in the future (e.g., signed statement)",
            "Satisfactory completion of a prescribed drug treatment program",
        ],
        "citation": "SEAD 4, Adjudicative Guidelines, Paragraph 24"
    },
    
    "D": {
        "title": "Guideline D: Sexual Behavior",
        "concern": (
            "Sexual behavior that involves a criminal offense, reflects a lack of judgment, "
            "or may subject the individual to coercion or duress."
        ),
        "disqualifying_conditions": [
            "Sexual behavior of a criminal nature",
            "Sexual behavior that causes vulnerability to coercion, exploitation, or duress",
            "Sexual behavior of a public nature or that reflects lack of discretion or judgment",
        ],
        "mitigating_conditions": [
            "The behavior occurred prior to or during adolescence and there is no evidence of subsequent conduct",
            "The behavior no longer serves as a basis for coercion, exploitation, or duress",
        ],
        "citation": "SEAD 4, Adjudicative Guidelines, Paragraph 12"
    },
    
    "J": {
        "title": "Guideline J: Criminal Conduct",
        "concern": (
            "Criminal activity creates doubt about a person's judgment, reliability, and "
            "trustworthiness. By its very nature, it calls into question a person's ability "
            "or willingness to comply with laws, rules, and regulations."
        ),
        "disqualifying_conditions": [
            "A single serious crime or multiple lesser offenses",
            "Discharge or dismissal from the Armed Forces under dishonorable conditions",
            "Allegation or admission of criminal conduct, regardless of whether the person was formally charged",
        ],
        "mitigating_conditions": [
            "So much time has elapsed since the criminal behavior happened that it is unlikely to recur",
            "Evidence of successful rehabilitation (e.g., employment, community ties)",
            "Pressured or coerced into committing the act and those pressures are no longer present",
        ],
        "citation": "SEAD 4, Adjudicative Guidelines, Paragraph 30"
    },
    
    "E": {
        "title": "Guideline E: Personal Conduct",
        "concern": (
            "Conduct involving questionable judgment, lack of candor, dishonesty, or unwillingness "
            "to comply with rules and regulations can raise questions about an individual's reliability, "
            "trustworthiness, and ability to protect classified or sensitive information."
        ),
        "disqualifying_conditions": [
            "Deliberate omission or falsification of relevant facts from any personnel security questionnaire",
            "Personal conduct that creates vulnerability to coercion, exploitation, or duress",
        ],
        "mitigating_conditions": [
            "The individual made prompt, good-faith efforts to correct the omission before being confronted",
            "The offense is so minor, or so much time has passed, that it is unlikely to recur",
        ],
        "citation": "SEAD 4, Adjudicative Guidelines, Paragraph 15"
    }
}


def search_guidelines(query: str) -> list[dict]:
    """
    Simple keyword-based RAG search.
    In production, this would use vector embeddings (ChromaDB, Pinecone, etc.)
    """
    query_lower = query.lower()
    results = []
    
    # Keyword matching
    if "alcohol" in query_lower or "dui" in query_lower or "drink" in query_lower:
        results.append({"guideline": "G", "data": SEAD4_GUIDELINES["G"]})
    
    if "drug" in query_lower or "substance" in query_lower or "marijuana" in query_lower:
        results.append({"guideline": "H", "data": SEAD4_GUIDELINES["H"]})
    
    if "sexual" in query_lower or "harassment" in query_lower:
        results.append({"guideline": "D", "data": SEAD4_GUIDELINES["D"]})
    
    if "assault" in query_lower or "violence" in query_lower or "criminal" in query_lower:
        results.append({"guideline": "J", "data": SEAD4_GUIDELINES["J"]})
    
    if "dishonest" in query_lower or "falsif" in query_lower:
        results.append({"guideline": "E", "data": SEAD4_GUIDELINES["E"]})
    
    return results


def get_guideline(code: str) -> dict:
    """Retrieve a specific guideline by code"""
    return SEAD4_GUIDELINES.get(code.upper(), None)


if __name__ == "__main__":
    print("Testing RAG Knowledge Base...")
    
    # Test searches
    test_queries = ["alcohol incident", "marijuana possession", "assault charge"]
    
    for query in test_queries:
        results = search_guidelines(query)
        print(f"\nQuery: '{query}'")
        print(f"Found {len(results)} guidelines:")
        for r in results:
            print(f"  - {r['guideline']}: {r['data']['title']}")