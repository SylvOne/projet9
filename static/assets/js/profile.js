/* Script de gestion de la page profile.html */

document.getElementById('image-upload').addEventListener('change', function (event) {
            
    var input = event.target;
    var imagePreview = document.getElementById('image-preview');
    imagePreview.style.display = 'block';
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            imagePreview.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
});

document.getElementById('image-upload-request').addEventListener('change', function (event) {
    
    var input = event.target;
    var imagePreview = document.getElementById('image-preview-request');
    imagePreview.style.display = 'block';
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            imagePreview.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
});

function confirmPostDelete(postId, userProfile) {
    if (confirm('Êtes-vous sûr de vouloir supprimer ce post ?')) {
    // Créer un formulaire caché
    const form = document.createElement('form');
    form.action = '/delete_post/' + postId + '/';
    form.method = 'POST';
    form.style.display = 'none';

    // Ajout du jeton CSRF
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;
    
    // Ajout de userProfile
    const userProfileInput = document.createElement('input');
    userProfileInput.type = 'hidden';
    userProfileInput.name = 'userProfile';
    userProfileInput.value = userProfile;

    // Ajouter le formulaire au corps du document
    form.appendChild(csrfInput);
    form.appendChild(userProfileInput);
    document.body.appendChild(form);

    // Soumettre le formulaire
    form.submit();
    }
}

function showEditPostModal(postId) {
    const modal = document.getElementById(postId);
    modal.style.display = 'block';
}

function closeEditPostModal(postId) {
    const modal = document.getElementById(postId);
    modal.style.display = 'none';
}



function confirmReviewDelete(reviewId, userProfile) {
    if (confirm('Êtes-vous sûr de vouloir supprimer ce review ?')) {
    // Créer un formulaire caché
    const form = document.createElement('form');
    form.action = '/delete_review/' + reviewId + '/';
    form.method = 'POST';
    form.style.display = 'none';

    // Ajout du jeton CSRF
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;

     // Ajout de userProfile
    const userProfileInput = document.createElement('input');
    userProfileInput.type = 'hidden';
    userProfileInput.name = 'userProfile';
    userProfileInput.value = userProfile;

    // Ajouter le formulaire au corps du document
    form.appendChild(csrfInput);
    form.appendChild(userProfileInput);
    document.body.appendChild(form);

    // Soumettre le formulaire
    form.submit();
    }
}

function showEditReviewModal(reviewId) {
    const modal = document.getElementById(reviewId);
    modal.style.display = 'block';
}

function closeEditReviewModal(reviewId) {
    const modal = document.getElementById(reviewId);
    modal.style.display = 'none';
}