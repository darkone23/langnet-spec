#!/usr/bin/env python3
"""
Python writer example for LangNet schema.

This demonstrates:
1. Creating protobuf messages in Python
2. Serializing to binary (for Zig consumption)
3. Serializing to JSON (for human-readable debugging)
4. Writing files for Zig to read
"""

import sys
import os
import json

# Add generated Python code to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'generated', 'python'))

from google.protobuf.json_format import MessageToJson, MessageToDict, Parse
from langnet_pb2 import (
    SearchRequest,
    SearchResponse,
    User,
    Timestamp,
    ApiRequest,
    ApiResponse,
    Config,
    Batch,
    Event,
    Error
)
import langnet_pb2


def create_search_request():
    """Create a search request with sample data."""
    request = SearchRequest(
        query="protocol buffers python zig",
        page_number=1,
        results_per_page=20
    )
    return request


def create_search_response():
    """Create a search response with sample results."""
    response = SearchResponse(
        total_results=3,
        page_number=1
    )
    
    # Add results
    results = [
        {
            'id': 'result-1',
            'title': 'Protocol Buffers Documentation',
            'url': 'https://protobuf.dev',
            'snippet': 'Official Protocol Buffers documentation',
            'metadata': {'source': 'official', 'language': 'multiple'}
        },
        {
            'id': 'result-2', 
            'title': 'Zig Programming Language',
            'url': 'https://ziglang.org',
            'snippet': 'Official Zig programming language website',
            'metadata': {'source': 'official', 'language': 'zig'}
        },
        {
            'id': 'result-3',
            'title': 'Python Protocol Buffers Guide',
            'url': 'https://developers.google.com/protocol-buffers/docs/pythontutorial',
            'snippet': 'Using Protocol Buffers with Python',
            'metadata': {'source': 'google', 'language': 'python'}
        }
    ]
    
    for result_data in results:
        result = response.results.add()
        result.id = result_data['id']
        result.title = result_data['title']
        result.url = result_data['url']
        result.snippet = result_data['snippet']
        result.metadata.update(result_data['metadata'])
    
    return response


def create_user():
    """Create a user with sample data."""
    from datetime import datetime
    
    now = datetime.utcnow()
    timestamp = Timestamp(
        seconds=int(now.timestamp()),
        nanos=now.microsecond * 1000
    )
    
    user = User(
        id='user-123',
        username='testuser',
        email='test@example.com',
        roles=['user', 'admin'],
        preferences={'theme': 'dark', 'language': 'en'},
        created_at=timestamp,
        updated_at=timestamp
    )
    
    return user


def create_config():
    """Create configuration settings."""
    from datetime import datetime
    
    now = datetime.utcnow()
    timestamp = Timestamp(
        seconds=int(now.timestamp()),
        nanos=now.microsecond * 1000
    )
    
    config = Config(
        settings={
            'api_endpoint': 'https://api.example.com',
            'timeout': '30',
            'retries': '3'
        },
        enabled_features=['search', 'users', 'analytics'],
        last_updated=timestamp
    )
    
    return config


def create_batch():
    """Create a batch of operations."""
    batch = Batch(
        batch_id='batch-2025-01-15'
    )
    
    # Add search requests
    for i in range(3):
        search = batch.searches.add()
        search.query = f"search query {i}"
        search.page_number = 1
        search.results_per_page = 10
    
    # Add users
    for i in range(2):
        user = batch.users.add()
        user.id = f"batch-user-{i}"
        user.username = f"user{i}"
        user.email = f"user{i}@example.com"
        user.roles.append('user')
    
    return batch


def create_event():
    """Create an event for tracking."""
    from datetime import datetime
    
    now = datetime.utcnow()
    timestamp = Timestamp(
        seconds=int(now.timestamp()),
        nanos=now.microsecond * 1000
    )
    
    event = Event(
        type=Event.EventType.SEARCH,
        id='event-123',
        data={'query': 'test', 'results': '3'},
        occurred_at=timestamp,
        source='python-writer'
    )
    
    return event


def write_binary_files():
    """Write binary protobuf files for Zig to read."""
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Create and write each message type
    messages = [
        ('search_request.bin', create_search_request()),
        ('search_response.bin', create_search_response()),
        ('user.bin', create_user()),
        ('config.bin', create_config()),
        ('batch.bin', create_batch()),
        ('event.bin', create_event())
    ]
    
    for filename, message in messages:
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(message.SerializeToString())
        print(f"Written: {filepath} ({len(message.SerializeToString())} bytes)")
    
    return output_dir


def write_json_files():
    """Write JSON files for debugging and cross-language compatibility."""
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    messages = [
        ('search_request.json', create_search_request()),
        ('search_response.json', create_search_response()),
        ('user.json', create_user()),
        ('config.json', create_config()),
        ('batch.json', create_batch()),
        ('event.json', create_event())
    ]
    
    for filename, message in messages:
        filepath = os.path.join(output_dir, filename)
        json_data = MessageToJson(message, preserving_proto_field_name=True)
        
        with open(filepath, 'w') as f:
            f.write(json_data)
        
        # Also create Python-native JSON for comparison
        dict_data = MessageToDict(message)
        native_filepath = os.path.join(output_dir, f"native_{filename}")
        with open(native_filepath, 'w') as f:
            json.dump(dict_data, f, indent=2)
        
        print(f"Written JSON: {filepath}")
        print(f"Written native JSON: {native_filepath}")
    
    return output_dir


def create_api_request():
    """Create an API request wrapper."""
    from datetime import datetime
    
    now = datetime.utcnow()
    timestamp = Timestamp(
        seconds=int(now.timestamp()),
        nanos=now.microsecond * 1000
    )
    
    request = ApiRequest(
        request_id='req-123',
        sent_at=timestamp
    )
    
    # Set the search payload
    search = create_search_request()
    request.search.CopyFrom(search)
    
    return request


def create_api_response():
    """Create an API response wrapper."""
    from datetime import datetime
    
    now = datetime.utcnow()
    timestamp = Timestamp(
        seconds=int(now.timestamp()),
        nanos=now.microsecond * 1000
    )
    
    response = ApiResponse(
        request_id='req-123',
        received_at=timestamp
    )
    
    # Set the search response payload
    search_response = create_search_response()
    response.search_response.CopyFrom(search_response)
    
    return response


def create_error_response():
    """Create an error response."""
    from datetime import datetime
    
    now = datetime.utcnow()
    timestamp = Timestamp(
        seconds=int(now.timestamp()),
        nanos=now.microsecond * 1000
    )
    
    error = Error(
        code='NOT_FOUND',
        message='Resource not found',
        details={'resource_id': 'xyz-123'},
        timestamp=timestamp
    )
    
    return error


def main():
    """Main demonstration function."""
    print("=== Python Writer Example ===\n")
    
    # Create output directory
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    print("1. Creating sample messages...")
    
    # Create various messages
    search_request = create_search_request()
    search_response = create_search_response()
    user = create_user()
    config = create_config()
    batch = create_batch()
    event = create_event()
    api_request = create_api_request()
    api_response = create_api_response()
    error = create_error_response()
    
    print(f"   Created {len(search_response.results)} search results")
    print(f"   Created user: {user.username} ({user.email})")
    print(f"   Created config with {len(config.settings)} settings")
    print(f"   Created batch with {len(batch.searches)} searches and {len(batch.users)} users")
    
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
    json_str = MessageToJson(search_request, preserving_proto_field_name=True)
    print(f"   SearchRequest JSON (first 100 chars): {json_str[:100]}...")
    
    # Show binary size comparison
    binary_size = len(search_request.SerializeToString())
    json_size = len(json_str.encode('utf-8'))
    print(f"\n5. Size comparison:")
    print(f"   Binary: {binary_size} bytes")
    print(f"   JSON: {json_size} bytes")
    print(f"   Ratio: {json_size/binary_size:.1f}x larger")
    
    print("\n6. Creating API wrapper messages...")
    
    # Write API messages
    with open(os.path.join(output_dir, 'api_request.bin'), 'wb') as f:
        f.write(api_request.SerializeToString())
    
    with open(os.path.join(output_dir, 'api_response.bin'), 'wb') as f:
        f.write(api_response.SerializeToString())
    
    with open(os.path.join(output_dir, 'error_response.bin'), 'wb') as f:
        f.write(error.SerializeToString())
    
    print("   API messages written")
    
    print("\n=== Example Complete ===")
    print(f"\nNext steps:")
    print(f"1. Run the Zig reader: zig build run -- reader")
    print(f"2. Check the 'output/' directory for generated files")
    print(f"3. Use 'just generate-all' to regenerate code if schema changes")


if __name__ == '__main__':
    main()