from ctranslate2.converters import TransformersConverter
import os

model_name = "facebook/nllb-200-distilled-600M"
output_dir = "nllb-200-distilled-600M-int8"

print(f"Starting conversion of {model_name}...")
print(f"Output directory: {output_dir}")

try:
    converter = TransformersConverter(
        model_name_or_path=model_name,
    )
    
    converter.convert(
        output_dir=output_dir,
        quantization="int8",
        force=True
    )
    print("Conversion successful!")
    
except Exception as e:
    print(f"Error during conversion: {e}")
    exit(1)
