"""Unit tests for ML and Grad-CAM functionality."""
import os
import tempfile
import numpy as np
from PIL import Image

from app.ml.grad_cam import generate_gradcam_heatmap, save_heatmap_overlay


def test_save_heatmap_overlay_creates_file():
    """Test that heatmap overlay is generated and saved."""
    # Create a temporary image
    temp_dir = tempfile.mkdtemp()
    test_image_path = os.path.join(temp_dir, "test_image.png")
    test_image = Image.new("RGB", (224, 224), (128, 128, 128))
    test_image.save(test_image_path)

    # Generate heatmap
    output_path = save_heatmap_overlay(test_image_path, temp_dir)
    
    assert os.path.exists(output_path)
    assert output_path.endswith("heatmap_test_image.png")
    
    # Verify output is a valid image
    output_img = Image.open(output_path)
    assert output_img.size == test_image.size
    assert output_img.mode == "RGB"
    
    # Cleanup
    os.remove(test_image_path)
    os.remove(output_path)
    os.rmdir(temp_dir)


def test_save_heatmap_overlay_with_model_fallback():
    """Test heatmap generation falls back gracefully when model is None."""
    temp_dir = tempfile.mkdtemp()
    test_image_path = os.path.join(temp_dir, "test_image.png")
    test_image = Image.new("RGB", (256, 256), (200, 150, 100))
    test_image.save(test_image_path)

    # Generate heatmap without model (should use fallback)
    output_path = save_heatmap_overlay(test_image_path, temp_dir, model=None, preprocessed_img=None)
    
    assert os.path.exists(output_path)
    
    # Cleanup
    os.remove(test_image_path)
    os.remove(output_path)
    os.rmdir(temp_dir)


def test_generate_gradcam_heatmap_fallback():
    """Test Grad-CAM fallback when no valid model layer found."""
    # Create a dummy array
    dummy_img = np.random.rand(1, 224, 224, 3).astype(np.float32)
    
    # Should fall back to center-focused gradient when model is None
    heatmap = generate_gradcam_heatmap(None, dummy_img)
    
    assert isinstance(heatmap, np.ndarray)
    assert heatmap.shape == (224, 224)
    assert 0.0 <= heatmap.min() <= heatmap.max() <= 1.0


def test_heatmap_overlay_handles_different_image_sizes():
    """Test that heatmap generation works with various image sizes."""
    temp_dir = tempfile.mkdtemp()
    
    sizes = [(100, 100), (512, 512), (800, 600)]
    
    for w, h in sizes:
        test_image_path = os.path.join(temp_dir, f"test_{w}x{h}.png")
        test_image = Image.new("RGB", (w, h), (100, 100, 100))
        test_image.save(test_image_path)
        
        output_path = save_heatmap_overlay(test_image_path, temp_dir)
        assert os.path.exists(output_path)
        
        output_img = Image.open(output_path)
        assert output_img.size == (w, h)
        
        os.remove(test_image_path)
        os.remove(output_path)
    
    os.rmdir(temp_dir)
