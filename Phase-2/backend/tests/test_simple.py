"""Simple unit tests using unittest"""
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Test basic imports and model structure
class TestBasicImports:
    """Test that all modules can be imported"""

    def test_models_importable(self):
        """Test models can be imported"""
        try:
            from models.user import User, UserResponse
            print("✅ User models imported successfully")
        except Exception as e:
            print(f"❌ Failed to import User models: {e}")
            raise

    def test_models_importable_task(self):
        """Test task model can be imported"""
        try:
            from models.task import Task, TaskResponse
            print("✅ Task models imported successfully")
        except Exception as e:
            print(f"❌ Failed to import Task models: {e}")
            raise


if __name__ == "__main__":
    test = TestBasicImports()
    test.test_models_importable()
    test.test_models_importable_task()
    print("\n✅ All basic import tests passed!")
