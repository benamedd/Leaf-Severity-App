# -*- coding: utf-8 -*-
import streamlit as st
import leaf_analysis
from PIL import Image
import numpy as np
import os
import logging

# Configure basic logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set page title
st.title("Leaf Severity Analysis")

# File uploader
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png"])

if uploaded_file is not None:
    # Open and display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Save the image temporarily for processing
    image_path = "temp_image.jpg"
    image.save(image_path)
    logger.debug(f"Temporary image saved at: {image_path}")

    try:
        # Analyze the image
        logger.debug("Starting image analysis")
        processed_image, leaf_mask, infected_mask = leaf_analysis.load_and_process_image(image_path)
        severity = leaf_analysis.calculate_severity(leaf_mask, infected_mask)
        logger.debug(f"Severity calculated: {severity:.2f}%")

        # Display the severity
        st.write(f"**Infection Severity: {severity:.2f}%**")

        # Display the infected mask for visualization
        infected_image = Image.fromarray((infected_mask * 255).astype(np.uint8))
        st.image(infected_image, caption="Infected Areas (White)", use_column_width=True)

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        st.error(f"Error processing image: {str(e)}")

    finally:
        # Clean up the temporary file
        if os.path.exists(image_path):
            os.remove(image_path)
            logger.debug(f"Temporary file {image_path} removed")