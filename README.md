# A sample NLLB + CTranslate2 Server for [Visual Novel Translate](https://apps.microsoft.com/detail/9NJBR6DV99DM)

This is a simple Python server that hosts a CTranslate2-optimized NLLB model for local offline translation.

## Prerequisites

- [Python 3.8+](https://apps.microsoft.com/detail/9PNRBTZXMB4Z?hl=en-us&gl=US&ocid=pdpshare)

## 1. Purpose
This directory contains a lightweight implementation of a local translation server. Its primary goal is to wrap complex AI models (like Meta's **NLLB-200**) into a simple local API.
* **The Bridge**: It allows the app to communicate with a local AI model just as it would with an online service like Google Translate.
* **Local Processing**: It handles model loading, text inference, and result delivery entirely on your machine.

## 2. Origin
The scripts are built upon industry-leading open-source technologies:
* **Core Model**: Based on the **NLLB (No Language Left Behind)** project by Meta (Facebook AI), renowned for high-quality translation across 200+ languages.
* **Backend**: Powered by Python and the Hugging Face `transformers` library.
* **Implementation**: A minimal, streamlined script provided by the `Visual Novel Translate` team to enable "one-click" AI deployment for everyday users.

## 3. Safety & Privacy
**It is completely safe and secure.**
* **100% Offline**: The server runs solely on your local loopback address (`127.0.0.1`). Your data never leaves your computer and is never sent to any cloud provider.
* **Transparent Code**: The scripts (`.py` and `.bat` files) are plain text. You are free to inspect every line of code using any text editor. There are no encrypted binaries or hidden backdoors.
* **Clean Installation**: It uses Python's virtual environment to manage dependencies without altering your system-wide settings.

## 4. Key Benefits
* **No Limits**: Unlike cloud APIs (Google, DeepL), there are no usage quotas or subscription fees.
* **Maximum Privacy**: Ideal for sensitive content that should not be shared with third parties.
* **Resource Utilization**: Leverages your own hardware (CPU/GPU) for high-performance, cost-free translation.

## 5. Installation & Setup
1. **Download & Locate**: Download all files to your local machine. 
2. **Run the Script**: Simply double-click on `run_server.bat` to launch the server.
3. **Automatic Setup**: On the first launch, the script will automatically set up the environment and download the required AI models. This may take several minutes depending on your internet speed.
4. **Ready to Use**: Subsequent launches will be near-instant, as the model data is cached locally on your machine.

*Note: If you encounter a Windows security prompt, please ensure you allow the script to run, as it needs to set up a local Python environment.*

