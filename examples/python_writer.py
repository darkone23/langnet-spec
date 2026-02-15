#!/usr/bin/env python3
"""
Python writer example for LangNet schema.

This demonstrates:
1. Creating protobuf messages in Python using betterproto2
2. Serializing to binary (for Zig consumption)
3. Serializing to JSON (for human-readable debugging)
4. Writing files for Zig to read
"""

import sys
import os
import json

# Add generated betterproto2 code to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "generated", "python"))

from langnet_spec import (
    QueryResponse,
    Query,
    Lemma,
    Language,
    LanguageHint,
    NormalizationStep,
    Analysis,
    AnalysisType,
    MorphologicalFeatures,
    PartOfSpeech,
    Case,
    Number,
    Gender,
    Person,
    Tense,
    Mood,
    Voice,
    Degree,
    Sense,
    Witness,
    Citation,
    CitationType,
    Provenance,
    UiHints,
    SimpleSearchQuery,
    SimpleSearchResult,
)


def create_query_response():
    """Create a complete QueryResponse with sample data."""
    # Create Query
    query = Query(
        surface="śiva",
        language_hint=LanguageHint.SAN,
        normalized="śiva",
        normalization_steps=[
            NormalizationStep(
                operation="normalize_unicode", input="śiva", output="śiva", tool="unicodedata"
            )
        ],
    )

    # Create Lemmas
    lemmas = [
        Lemma(
            lemma_id="san:śiva",
            display="Śiva",
            language=Language.SAN,
            sources=["MW", "Heritage"],
        ),
        Lemma(
            lemma_id="san:śivaḥ",
            display="Śivaḥ",
            language=Language.SAN,
            sources=["MW"],
        ),
        Lemma(
            lemma_id="san:śivaḥ",
            display="Śivaḥ",
            language=Language.SAN,
            sources=["MW"],
        ),
    ]

    # Create Morphological Features for noun analysis
    noun_features = MorphologicalFeatures(
        pos=PartOfSpeech.POS_NOUN,
        case=Case.NOMINATIVE,
        number=Number.SINGULAR,
        gender=Gender.MASCULINE,
    )

    # Create Analyses
    analyses = [
        Analysis(
            type=AnalysisType.MORPHOLOGY,
            features=noun_features,
            witnesses=[
                Witness(source="MW", ref="217497"),
                Witness(source="Heritage", ref="heritage:morph:ziva"),
            ],
        )
    ]

    # Create Senses
    senses = [
        Sense(
            sense_id="B1",
            semantic_constant="AUSPICIOUSNESS",
            display_gloss="auspicious, propitious, gracious, benign, kind",
            domains=["general", "religious"],
            register=["epithet", "poetic"],
            witnesses=[Witness(source="MW", ref="217497")],
        ),
        Sense(
            sense_id="B2",
            semantic_constant="DESTRUCTION",
            display_gloss="the destroying or dissolving principle",
            domains=["religious", "mythological"],
            register=["formal"],
            witnesses=[Witness(source="MW", ref="217497")],
        ),
        Sense(
            sense_id="B2",
            semantic_constant="DESTRUCTION",
            display_gloss="the destroying or dissolving principle",
            domains=["religious", "mythological"],
            register=["formal"],
            witnesses=[Witness(source="MW", ref="217497")],
        ),
    ]

    # Create Citations
    citations = [
        Citation(
            source="Monier-Williams Sanskrit-English Dictionary",
            type=CitationType.DICTIONARY,
            ref="MW 217497",
            text="śiva mf(ā)n. auspicious, propitious, gracious, benign, kind",
            translation="auspicious, propitious, gracious, benign, kind",
        ),
        Citation(
            source="Rigveda",
            type=CitationType.CTS,
            ref="RV 1.114.1",
            text="śivaḥ śivābhir ṛtubhir yajāmahe",
            translation="We worship Śiva with auspicious seasons",
        ),
    ]

    # Create Provenance
    provenance = [
        Provenance(tool="langnet-analyzer-v1.0"),
        Provenance(tool="morphology-parser-v0.5"),
    ]

    # Create UI Hints
    ui_hints = UiHints(default_mode="open", primary_lemma="san:śiva", collapsed_senses=["B2"])

    # Create QueryResponse
    response = QueryResponse(
        schema_version="1.0.0",
        query=query,
        lemmas=lemmas,
        analyses=analyses,
        senses=senses,
        citations=citations,
        provenance=provenance,
        ui_hints=ui_hints,
        warnings=[],
    )

    return response


def create_simple_search_query():
    """Create a SimpleSearchQuery for testing."""
    query = SimpleSearchQuery(
        query="śiva",
        language=Language.SAN,
        max_results=10,
        include_morphology=True,
        include_definitions=True,
    )
    return query


def create_simple_search_result():
    """Create a SimpleSearchResult for testing."""
    result = SimpleSearchResult(
        word="śiva",
        lemma="Śiva",
        language="Sanskrit",
        part_of_speech="noun",
        definition="auspicious, propitious, gracious",
        morphology="nominative singular masculine",
        relevance_score=0.95,
        sources=["MW", "Heritage"],
    )
    return result


def write_binary_files():
    """Write binary protobuf files for Zig to read."""
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Create and write each message type
    messages = [
        ("query_response.bin", create_query_response()),
        ("simple_search_query.bin", create_simple_search_query()),
        ("simple_search_result.bin", create_simple_search_result()),
    ]

    for filename, message in messages:
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "wb") as f:
            f.write(bytes(message))
        print(f"Written: {filepath} ({len(bytes(message))} bytes)")

    return output_dir


def write_json_files():
    """Write JSON files for debugging and cross-language compatibility."""
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    messages = [
        ("query_response.json", create_query_response()),
        ("simple_search_query.json", create_simple_search_query()),
        ("simple_search_result.json", create_simple_search_result()),
    ]

    for filename, message in messages:
        filepath = os.path.join(output_dir, filename)
        json_data = message.to_json(indent=2)

        with open(filepath, "w") as f:
            f.write(json_data)

        # Also create Python-native JSON for comparison
        dict_data = message.to_dict()
        native_filepath = os.path.join(output_dir, f"native_{filename}")
        with open(native_filepath, "w") as f:
            json.dump(dict_data, f, indent=2, default=str)

        print(f"Written JSON: {filepath}")
        print(f"Written native JSON: {native_filepath}")

    return output_dir


def main():
    """Main demonstration function."""
    print("=== Python Writer Example (betterproto2) ===\n")

    # Create output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    print("1. Creating sample messages...")

    # Create various messages
    query_response = create_query_response()
    simple_search_query = create_simple_search_query()
    simple_search_result = create_simple_search_result()

    print(f"   Created QueryResponse with:")
    print(f"     - {len(query_response.lemmas)} lemmas")
    print(f"     - {len(query_response.analyses)} analyses")
    print(f"     - {len(query_response.senses)} senses")
    print(f"     - {len(query_response.citations)} citations")
    print(f"   Created SimpleSearchQuery for: {simple_search_query.query}")
    print(f"   Created SimpleSearchResult: {simple_search_result.word}")

    print("\n2. Serializing to binary...")

    # Write binary files
    binary_dir = write_binary_files()
    print(f"   Binary files written to: {binary_dir}/")

    print("\n3. Serializing to JSON...")

    # Write JSON files
    json_dir = write_json_files()
    print(f"   JSON files written to: {json_dir}/")

    print("\n4. Demonstrating JSON serialization...")

    # Show JSON example
    json_str = query_response.to_json(indent=2)
    print(f"   QueryResponse JSON (first 100 chars): {json_str[:100]}...")

    # Show binary size comparison
    binary_size = len(bytes(query_response))
    json_size = len(json_str.encode("utf-8"))
    print(f"\n5. Size comparison:")
    print(f"   Binary: {binary_size} bytes")
    print(f"   JSON: {json_size} bytes")
    print(f"   Ratio: {json_size / binary_size:.1f}x larger")

    print("\n6. Testing message equality and copy...")

    # Test copy functionality
    query_response_copy = create_query_response()
    print(f"   QueryResponse equality: {query_response == query_response_copy}")

    print("\n=== Example Complete ===")
    print(f"\nNext steps:")
    print(f"1. Run the Zig reader: zig build run -- reader")
    print(f"2. Check the 'output/' directory for generated files")
    print(f"3. Use 'just generate-python' to regenerate betterproto2 code if schema changes")


if __name__ == "__main__":
    main()
