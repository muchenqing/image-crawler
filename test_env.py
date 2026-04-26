print("Testing Python environment...")
print("Python is working!")

# Test basic functionality
try:
    import os
    print("os module imported successfully")
except Exception as e:
    print(f"Error importing os: {e}")

try:
    import urllib.request
    print("urllib.request imported successfully")
except Exception as e:
    print(f"Error importing urllib.request: {e}")

print("Test completed!")
input("Press Enter to exit...")