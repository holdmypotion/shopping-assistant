#!/usr/bin/env python3
"""Debug script to test the shopping assistant workflow."""

import os
from src.agent.graph import graph
from langchain_core.messages import HumanMessage

def test_with_image_message():
    """Test the workflow with a simulated image message."""
    
    # Simulate a message with an image
    test_message = HumanMessage(
        content=[
            {"type": "text", "text": "Please analyze this product image"},
            {
                "type": "image", 
                "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k="
            }
        ]
    )
    
    initial_state = {
        "messages": [test_message]
    }
    
    print("🔍 Testing workflow with image message...")
    print(f"Initial state: {initial_state}")
    
    try:
        # Run the graph
        result = graph.invoke(initial_state)
        print(f"\n✅ Final result: {result}")
        
        # Check if analysis was performed
        if "analysis_output" in result:
            print(f"\n📊 Analysis output: {result['analysis_output']}")
        else:
            print("\n❌ No analysis output found")
            
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()

def test_without_image():
    """Test the workflow without an image."""
    
    test_message = HumanMessage(content="Hello, I want to analyze a product")
    
    initial_state = {
        "messages": [test_message]
    }
    
    print("\n🔍 Testing workflow without image...")
    print(f"Initial state: {initial_state}")
    
    try:
        result = graph.invoke(initial_state)
        print(f"\n✅ Final result: {result}")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")

if __name__ == "__main__":
    print("🚀 Starting Shopping Assistant Debug Test")
    print("=" * 50)
    
    # Test without image first
    test_without_image()
    
    print("\n" + "=" * 50)
    
    # Test with image
    test_with_image_message() 