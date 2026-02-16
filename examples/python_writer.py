#!/usr/bin/env python3
"""
Python writer example for LangNet schema.

This demonstrates:
1. Creating protobuf messages in Python using the generated modules (standard protobuf)
2. Serializing to binary (for Zig consumption)
3. Serializing to JSON (for human-readable debugging)
4. Writing files for Zig to read
"""

import sys
import os
import json

from google.protobuf.json_format import MessageToJson, MessageToDict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "generated", "python"))

import langnet_spec


def create_query_response():
    """Create a complete QueryResponse with sample data."""
    # Create Query
    query = langnet_spec.Query(
        surface="si\u0301va",
        language_hint=langnet_spec.LANGUAGE_HINT_SAN,
        normalized="si\u0301va",
    )
    step = query.normalization_steps.add()
    step.operation = "normalize_unicode"
    step.input = "si\u0301va"
    step.output = "si\u0301va"
    step.tool = "unicodedata"

    # Create Lemmas
    lemma1 = langnet_spec.Lemma(
        lemma_id="san:\u015bi\u0301va",
        display="\u015aiva",
        language=langnet_spec.LANGUAGE_SAN,
    )
    lemma1.sources.append(langnet_spec.SOURCE_MW)
    lemma1.sources.append(langnet_spec.SOURCE_HERITAGE)

    lemma2 = langnet_spec.Lemma(
        lemma_id="san:\u015bi\u0301va\u1e25",
        display="\u015aiva\u1e25",
        language=langnet_spec.LANGUAGE_SAN,
    )
    lemma2.sources.append(langnet_spec.SOURCE_MW)

    lemma3 = langnet_spec.Lemma(
        lemma_id="san:\u015bi\u0301va\u1e25",
        display="\u015aiva\u1e25",
        language=langnet_spec.LANGUAGE_SAN,
    )
    lemma3.sources.append(langnet_spec.SOURCE_MW)

    # Create Morphological Features for noun analysis
    noun_features = langnet_spec.MorphologicalFeatures(
        pos=langnet_spec.POS_NOUN,
        case=langnet_spec.CASE_NOMINATIVE,
        number=langnet_spec.NUMBER_SINGULAR,
        gender=langnet_spec.GENDER_MASCULINE,
    )

    # Create Analysis with witness
    analysis = langnet_spec.Analysis(
        type=langnet_spec.ANALYSIS_TYPE_MORPHOLOGY,
        features=noun_features,
    )
    witness1 = analysis.witnesses.add()
    witness1.source = langnet_spec.SOURCE_MW
    witness1.ref = "217497"

    witness2 = analysis.witnesses.add()
    witness2.source = langnet_spec.SOURCE_HERITAGE
    witness2.ref = "heritage:morph:ziva"

    # Create Senses
    sense1 = langnet_spec.Sense(
        sense_id="B1",
        semantic_constant="AUSPICIOUSNESS",
        display_gloss="auspicious, propitious, gracious, benign, kind",
    )
    sense1.domains.append("general")
    sense1.domains.append("religious")
    sense1.register.append("epithet")
    sense1.register.append("poetic")
    sense1_witness = sense1.witnesses.add()
    sense1_witness.source = langnet_spec.SOURCE_MW
    sense1_witness.ref = "217497"

    sense2 = langnet_spec.Sense(
        sense_id="B2",
        semantic_constant="DESTRUCTION",
        display_gloss="the destroying or dissolving principle",
    )
    sense2.domains.append("religious")
    sense2.domains.append("mythological")
    sense2.register.append("formal")
    sense2_witness = sense2.witnesses.add()
    sense2_witness.source = langnet_spec.SOURCE_MW
    sense2_witness.ref = "217497"

    sense3 = langnet_spec.Sense(
        sense_id="B2",
        semantic_constant="DESTRUCTION",
        display_gloss="the destroying or dissolving principle",
    )
    sense3.domains.append("religious")
    sense3.domains.append("mythological")
    sense3.register.append("formal")
    sense3_witness = sense3.witnesses.add()
    sense3_witness.source = langnet_spec.SOURCE_MW
    sense3_witness.ref = "217497"

    # Create Citations
    citation1 = langnet_spec.Citation(
        source="Monier-Williams Sanskrit-English Dictionary",
        type=langnet_spec.CITATION_TYPE_DICTIONARY,
        ref="MW 217497",
        text="\u015bi\u0301va mf(\u0101)n. auspicious, propitious, gracious, benign, kind",
        translation="auspicious, propitious, gracious, benign, kind",
    )

    citation2 = langnet_spec.Citation(
        source="Rigveda",
        type=langnet_spec.CITATION_TYPE_CTS,
        ref="RV 1.114.1",
        text="\u015biva\u1e25 \u015biv\u0101bhir \u1e9btubhir yaj\u0101mahe",
        translation="We worship \u015aiva with auspicious seasons",
    )

    # Create Provenance
    prov1 = langnet_spec.Provenance(tool="langnet-analyzer-v1.0")
    prov2 = langnet_spec.Provenance(tool="morphology-parser-v0.5")

    # Create UI Hints
    ui_hints = langnet_spec.UiHints(
        default_mode="open",
        primary_lemma="san:\u015bi\u0301va",
    )
    ui_hints.collapsed_senses.append("B2")

    # Create QueryResponse
    response = langnet_spec.QueryResponse(
        schema_version="1.0.0",
        query=query,
    )
    response.lemmas.extend([lemma1, lemma2, lemma3])
    response.analyses.append(analysis)
    response.senses.extend([sense1, sense2, sense3])
    response.citations.extend([citation1, citation2])
    response.provenance.extend([prov1, prov2])
    response.ui_hints.CopyFrom(ui_hints)

    return response


def create_simple_search_query():
    """Create a SimpleSearchQuery for testing."""
    query = langnet_spec.SimpleSearchQuery(
        query="\u015bi\u0301va",
        language=langnet_spec.LANGUAGE_SAN,
        max_results=10,
        include_morphology=True,
        include_definitions=True,
    )
    return query


def create_simple_search_result():
    """Create a SimpleSearchResult for testing."""
    result = langnet_spec.SimpleSearchResult(
        word="\u015bi\u0301va",
        lemma="\u015aiva",
        language="Sanskrit",
        part_of_speech="noun",
        definition="auspicious, propitious, gracious",
        morphology="nominative singular masculine",
        relevance_score=0.95,
    )
    result.sources.append("MW")
    result.sources.append("Heritage")
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
            f.write(message.SerializeToString())
        print(f"Written: {filepath} ({len(message.SerializeToString())} bytes)")

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
        json_data = MessageToJson(message, indent=2)

        with open(filepath, "w") as f:
            f.write(json_data)

        # Also create Python-native JSON for comparison
        dict_data = MessageToDict(message)
        native_filepath = os.path.join(output_dir, f"native_{filename}")
        with open(native_filepath, "w") as f:
            json.dump(dict_data, f, indent=2, default=str)

        print(f"Written JSON: {filepath}")
        print(f"Written native JSON: {native_filepath}")

    return output_dir


def main():
    """Main demonstration function."""
    print("=== Python Writer Example (standard protobuf) ===\n")

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
    json_str = MessageToJson(query_response, indent=2)
    print(f"   QueryResponse JSON (first 100 chars): {json_str[:100]}...")

    # Show binary size comparison
    binary_size = len(query_response.SerializeToString())
    json_size = len(json_str.encode("utf-8"))
    print(f"\n5. Size comparison:")
    print(f"   Binary: {binary_size} bytes")
    print(f"   JSON: {json_size} bytes")
    print(f"   Ratio: {json_size / binary_size:.1f}x larger")

    print("\n6. Testing message equality and copy...")

    # Test comparison
    query_response_copy = create_query_response()
    print(
        f"   QueryResponse binary equality: {query_response.SerializeToString() == query_response_copy.SerializeToString()}"
    )

    print("\n=== Example Complete ===")
    print(f"\nNext steps:")
    print(f"1. Run the Zig reader: zig build run -- reader")
    print(f"2. Check the 'output/' directory for generated files")
    print(f"3. Use 'just generate-python' to regenerate protobuf code if schema changes")


if __name__ == "__main__":
    main()
