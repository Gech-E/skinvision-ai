import os
import numpy as np
from typing import Tuple, Optional
from PIL import Image

try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    tf = None


def generate_gradcam_heatmap(model, image_array: np.ndarray, layer_name: Optional[str] = None) -> np.ndarray:
    """
    Generate Grad-CAM heatmap for the predicted class.
    Falls back to a simple visualization if model doesn't support Grad-CAM.
    """
    if not TENSORFLOW_AVAILABLE or model is None:
        raise ValueError("TensorFlow or model not available")
    
    try:
        # Try to find the last convolutional layer
        if layer_name is None:
            for layer in reversed(model.layers):
                if len(layer.output_shape) == 4:  # Convolutional layer
                    layer_name = layer.name
                    break
        
        if layer_name is None:
            raise ValueError("No convolutional layer found")
        
        # Build model that outputs the conv layer and final predictions
        conv_layer = model.get_layer(layer_name)
        grad_model = tf.keras.Model(
            [model.inputs],
            [conv_layer.output, model.output]
        )
        
        # Compute gradients
        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(image_array)
            class_idx = tf.argmax(predictions[0])
            class_channel = predictions[:, class_idx]
        
        grads = tape.gradient(class_channel, conv_outputs)
        
        # Global average pooling of gradients
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        # Multiply conv outputs with pooled gradients
        conv_outputs = conv_outputs[0]
        heatmap = tf.reduce_mean(tf.multiply(conv_outputs, pooled_grads), axis=-1)
        
        # Normalize heatmap
        heatmap = np.maximum(heatmap, 0)
        heatmap /= np.max(heatmap)
        
        # Resize to original image size
        heatmap = tf.image.resize(heatmap[..., tf.newaxis], (image_array.shape[1], image_array.shape[2]))
        heatmap = np.squeeze(heatmap.numpy())
        
        return heatmap
    except Exception as e:
        # Fallback: generate a simple attention-like heatmap
        print(f"Grad-CAM failed: {e}. Using fallback visualization.")
        # Create a center-focused gradient
        h, w = image_array.shape[1:3]
        y, x = np.ogrid[:h, :w]
        center_y, center_x = h // 2, w // 2
        dist_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        max_dist = np.sqrt(center_x**2 + center_y**2)
        heatmap = 1 - (dist_from_center / max_dist)
        heatmap = np.clip(heatmap, 0, 1)
        return heatmap


def save_heatmap_overlay(orig_path: str, out_dir: str, model=None, preprocessed_img: Optional[np.ndarray] = None) -> str:
    """
    Generate and save a heatmap overlay visualization.
    
    Args:
        orig_path: Path to original image
        out_dir: Directory to save heatmap
        model: Optional TensorFlow model for Grad-CAM
        preprocessed_img: Optional preprocessed image array (224x224 normalized)
    
    Returns:
        Path to saved heatmap image
    """
    os.makedirs(out_dir, exist_ok=True)
    
    # Load original image
    image = Image.open(orig_path).convert("RGB")
    orig_size = image.size
    w, h = orig_size
    
    # Generate heatmap
    if model is not None and preprocessed_img is not None:
        heatmap = generate_gradcam_heatmap(model, preprocessed_img)
        # Resize heatmap to original image size
        heatmap_pil = Image.fromarray((heatmap * 255).astype(np.uint8)).resize(orig_size, Image.Resampling.LANCZOS)
    else:
        # Fallback: simple center-focused gradient
        arr = np.zeros((h, w), dtype=np.float32)
        center_y, center_x = h // 2, w // 2
        y, x = np.ogrid[:h, :w]
        dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        max_dist = np.sqrt(center_x**2 + center_y**2)
        arr = 1 - np.clip(dist / max_dist, 0, 1)
        heatmap_pil = Image.fromarray((arr * 255).astype(np.uint8))
    
    # Create colored heatmap (red-yellow colormap)
    heatmap_colored = Image.new("RGB", orig_size, (0, 0, 0))
    heatmap_arr = np.array(heatmap_pil).astype(np.float32) / 255.0
    
    # Apply red-yellow colormap
    heatmap_rgb = np.zeros((h, w, 3), dtype=np.uint8)
    heatmap_rgb[:, :, 0] = (heatmap_arr * 255).astype(np.uint8)  # Red
    heatmap_rgb[:, :, 1] = (heatmap_arr * 200).astype(np.uint8)  # Yellow component
    heatmap_rgb[:, :, 2] = (heatmap_arr * 50).astype(np.uint8)   # Low blue
    
    heatmap_colored = Image.fromarray(heatmap_rgb)
    
    # Blend with original image
    overlay = heatmap_colored.convert("RGBA")
    overlay.putalpha(Image.fromarray((heatmap_arr * 180).astype(np.uint8)))  # Semi-transparent
    
    blended = Image.alpha_composite(image.convert("RGBA"), overlay)
    
    # Save
    out_path = os.path.join(out_dir, f"heatmap_{os.path.basename(orig_path)}")
    blended.convert("RGB").save(out_path)
    return out_path


