# Handwritten Signature Verification

This project is a handwritten signature verification system built using Django. It allows users to upload and verify handwritten signatures.

## Project Overview

- Web application for signature verification.
- Uses machine learning models to verify signatures.
- Includes user authentication and signature upload features.
- Stores signature images and verification attempts.

## Important Note on Machine Learning Model

The machine learning model file (`best_model.h5`) used for signature verification is **not included** in this repository due to its large size. 

To run the project successfully, you need to obtain the `best_model.h5` file separately and place it in the following directory:

```
Handwritten_signature_verification/Handwritten_signature_verfication/ml_models/
```

## How to Use

1. Clone this repository.
2. Place the `best_model.h5` file in the `ml_models` directory as mentioned above.
3. Install the required dependencies.
4. Run the Django development server.
5. Access the web application to upload and verify signatures.
