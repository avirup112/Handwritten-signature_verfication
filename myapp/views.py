from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserRegistrationForm, SignatureVerificationForm
from .models import OriginalSignature, VerificationAttempt
from django.conf import settings
import os
import tensorflow as tf
from keras.models import load_model
from keras.utils import load_img, img_to_array
import numpy as np

# Load your pre-trained signature verification model (make sure it is in the 'models/' directory)
MODEL_PATH = os.path.join(settings.BASE_DIR, 'Handwritten_signature_verfication', 'ml_models', 'best_model.h5')
model = load_model(MODEL_PATH)

# Function to predict whether the signature is real or fake and return confidence
def predict_signature(real_signature_path, uploaded_signature_path):
    real_signature = load_img(real_signature_path, target_size=(224, 224))
    uploaded_signature = load_img(uploaded_signature_path, target_size=(224, 224))
    
    # Preprocess images
    real_signature = np.expand_dims(img_to_array(real_signature) / 255.0, axis=0)
    uploaded_signature = np.expand_dims(img_to_array(uploaded_signature) / 255.0, axis=0)

    # Predict using the model
    real_prediction = model.predict(real_signature)[0]
    uploaded_prediction = model.predict(uploaded_signature)[0]

    # Calculate similarity score (e.g., cosine similarity or difference)
    similarity = np.dot(real_prediction, uploaded_prediction) / (np.linalg.norm(real_prediction) * np.linalg.norm(uploaded_prediction))
    confidence = float(similarity) * 100  # convert to percentage

    # Determine result based on similarity threshold
    threshold = 0.7
    if similarity >= threshold:
        result = "Real"
    else:
        result = "Fake"

    return result, confidence

# View for user registration
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            # Log in the user
            login(request, user)
            return redirect('verify_signature')
        else:
            print("User form errors:", user_form.errors)

    else:
        user_form = UserRegistrationForm()

    return render(request, 'index.html', {'user_form': user_form})

# View for user login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('verify_signature')
        else:
            print("Login form errors:", form.errors)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# View to verify the uploaded signature
@login_required
def verify_signature(request):
    result = None
    confidence = None
    original_signature_url = None
    uploaded_signature_url = None
    matched_user = None

    if request.method == 'POST':
        verification_form = SignatureVerificationForm(request.POST, request.FILES)
        
        if verification_form.is_valid():
            uploaded_signature = verification_form.save(commit=False)
            uploaded_signature.user = request.user
            uploaded_signature.save()
            uploaded_signature_url = uploaded_signature.uploaded_signature.url

            # Iterate over all original signatures to find best match
            best_confidence = -1
            best_result = "Fake"
            best_original_signature = None

            for orig_sig in OriginalSignature.objects.all():
                res, conf = predict_signature(
                    orig_sig.signature_image.path,
                    uploaded_signature.uploaded_signature.path
                )
                if conf > best_confidence:
                    best_confidence = conf
                    best_result = res
                    best_original_signature = orig_sig

            result = best_result
            confidence = best_confidence
            original_signature_url = best_original_signature.signature_image.url if best_original_signature else None

            # Save verification attempt with request.user
            VerificationAttempt.objects.create(
                user=request.user,
                uploaded_signature=uploaded_signature.uploaded_signature,
                result=result
            )

    else:
        verification_form = SignatureVerificationForm()

    context = {
        'verification_form': verification_form,
        'result': result,
        'confidence': confidence,
        'original_signature_url': original_signature_url,
        'uploaded_signature_url': uploaded_signature_url,
    }
    return render(request, 'verify_signature.html', context)
