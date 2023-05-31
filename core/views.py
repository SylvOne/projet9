from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount, Review
from itertools import chain
from django.shortcuts import get_object_or_404
from django.http import Http404
import os
from .forms import CritiqueForm, RequestCritiqueForm


# Vue gérant la page d'accueil après connexion
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user)

    for user in user_following:
        user_following_list.append(user.user)

    # voir les critiques de l'utilisateur connecté en plus des critiques des autres utilisateurs qu'il suit
    feed_me = Post.objects.filter(user=request.user.username)
    feed.append(feed_me)

    for username in user_following_list:
        feed_lists = Post.objects.filter(user=username)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))
    feed_list.sort(key=lambda x: x.created_at, reverse=True)
    # Récupérer les critiques associées à chaque post
    # Créer un dictionnaire pour stocker les critiques associées à chaque poste
    post_reviews = {}
    for post in feed_list:
        reviews = Review.objects.filter(post=post).order_by('-time_created')
        has_user_reviewed = reviews.filter(user=request.user).exists()
        post_reviews[post] = {
            'reviews': reviews,
            'has_user_reviewed': has_user_reviewed
        }

    # Création d'une liste de valeurs pour l'utiliser dans le template pour la modification du rating
    rating_values = list(range(1, 6))
    return render(
        request,
        'index.html',
        {
            'user_profile': user_profile,
            'post_reviews': post_reviews,
            'rating_values': rating_values
        }
    )


# Vue gérant la création d'un post avec une critique
@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        form = CritiqueForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user.username
            image = form.cleaned_data['image_upload']
            title_post = form.cleaned_data['title']
            title_review = form.cleaned_data['title_review']
            rating = form.cleaned_data['radio']
            caption = form.cleaned_data['caption']
            caption_review = form.cleaned_data['commentaire']

            new_post = Post.objects.create(
                user=user,
                user_id=request.user,
                image=image,
                caption=caption,
                title=title_post
            )
            new_post.save()
            # Récupérer le post nouvellement créé depuis la base de données
            new_post = Post.objects.get(pk=new_post.pk)

            new_review = Review.objects.create(
                post=new_post,
                rating=rating,
                headline=title_review,
                body=caption_review,
                user=request.user
            )
            new_review.save()
        else:
            messages.info(request, 'Vous devez remplir toutes les informations', extra_tags='error_post_and_critique')
        return redirect('/')
    else:
        return redirect('/')


# Vue gérant la création d'un post unique (demande de critique)
@login_required(login_url='signin')
def upload_request(request):
    if request.method == 'POST':
        form = RequestCritiqueForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user.username
            image = form.cleaned_data['image_upload']
            title_post = form.cleaned_data['title']
            caption = form.cleaned_data['caption']

            new_post = Post.objects.create(
                user=user,
                user_id=request.user,
                image=image,
                caption=caption,
                title=title_post
            )
            new_post.save()
        else:
            messages.info(request, 'Vous devez remplir toutes les informations', extra_tags='error_critique')
        return redirect('/')
    else:
        return redirect('/')


# Vue gérant l'ajout d'une critique
@login_required(login_url='signin')
def add_review(request):
    if request.method == 'POST':
        if (
            request.POST['post_to_add_review'] != ""
            or request.POST['radio'] != ''
            or request.POST['title_review'] != ''
            or request.POST['title_review'] != ' '
        ):
            title_review = request.POST['title_review']
            rating = request.POST['radio']
            caption_review = request.POST['commentaire']
            post_to_add_review = request.POST['post_to_add_review']
            # Récupérer le post depuis la base de données
            post = get_object_or_404(Post, pk=post_to_add_review)

            new_review = Review.objects.create(
                post=post,
                rating=rating,
                headline=title_review,
                body=caption_review,
                user=request.user
            )
            new_review.save()
        else:
            messages.info(request, 'Vous devez remplir les informations du livre')

        # Si c'est un ajout à partir du profil de l'utilisateur on le redirige sur son profil
        profile = request.POST.get('profile')
        if profile:
            return redirect('/profile/'+profile)
        else:
            return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='signin')
def delete_post(request, post_id):
    # Récupérer le post depuis la base de données
    post = get_object_or_404(Post, pk=post_id)
    if post.user == request.user.username:
        image_path = post.image.path
        # Récupérer toutes les critiques liées au post
        reviews = Review.objects.filter(post=post)
        # Supprimer toutes les critiques
        reviews.delete()
        # Supprimer le post lui-même
        post.delete()

        # Si l'image du post existe on la supprime après la suppression du post lui-même
        if os.path.exists(image_path):
            os.remove(image_path)

        return redirect('/')
    else:
        messages.info(request, "Vous devez être l'auteur du post pour le supprimer")
        return redirect('/')


# Vue gérant la modification d'un post (Ticket)
@login_required(login_url='signin')
def update_post(request, post_id):
    # Récupérer le post depuis la base de données
    post = get_object_or_404(Post, pk=post_id)

    if post.user == request.user.username:
        if request.method == 'POST':
            if (
                request.POST['caption'] != ""
                or request.POST['caption'] != ' '
                or request.POST['title'] != ''
                or request.POST['title'] != ' '
            ):
                title = request.POST['title']
                caption = request.POST['caption']
                post.title = title
                post.caption = caption
                post.save()
            else:
                messages.info(request, 'Vous devez remplir les informations du livre')

        # Si c'est une suppression à partir du profil de l'utilisateur on le redirige sur son profil
        profile = request.POST.get('profile')
        if profile:
            return redirect('/profile/'+request.POST['profile'])
        else:
            return redirect('/')
    else:
        messages.info(request, "Vous devez être l'auteur du post pour le modifier")
        return redirect('/')


# Vue gérant la suppression d'une critique
@login_required(login_url='signin')
def delete_review(request, review_id):
    # Récupérer le post depuis la base de données
    review = get_object_or_404(Review, pk=review_id)
    if review.user_id == request.user.id:
        # Supprimer toutes les critiques
        review.delete()
        # Si c'est une suppression à partir du profil de l'utilisateur on le redirige sur son profil
        userprofile = request.POST.get('userProfile')
        if userprofile:
            return redirect('/profile/' + userprofile)
        else:
            return redirect('/')
    else:
        messages.info(request, "Vous devez être l'auteur de la review pour la supprimer")
        return redirect('/')


# Vue gérant la modification d'une critique
@login_required(login_url='signin')
def update_review(request, review_id):
    # Récupérer le post depuis la base de données
    review = get_object_or_404(Review, pk=review_id)

    if review.user_id == request.user.id:
        if request.method == 'POST':
            if (
                request.POST['body'] != ""
                or request.POST['body'] != " "
                and request.POST['radio'] != ''
                and request.POST['headline'] != ''
                or request.POST['headline'] != ' '
            ):
                headline = request.POST['headline']
                body = request.POST['body']
                rating = request.POST['radio']
                review.headline = headline
                review.body = body
                review.rating = rating
                review.save()
            else:
                messages.info(request, 'Vous devez remplir les informations requises')

        profile = request.POST.get('profile')
        if profile is not None:
            return redirect('/profile/'+request.POST['profile'])
        else:
            return redirect('/')
    else:
        messages.info(request, "Vous devez être l'auteur de la review pour la modifier")
        return redirect('/')


# Vue gérant la recherche d'un utilisateur
@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    username_profile_list = []
    username = request.GET.get('username')
    if username is not None:
        username_object = User.objects.filter(username__icontains=username)
        username_profile = []
        for users in username_object:
            username_profile.append(users.id)
        # On récupère les profils des utilisateurs correspondants à la recherche
        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        # On concatene plusieurs listes pour en avoir qu'une seule
        username_profile_list = list(chain(*username_profile_list))
    return render(
        request,
        'search.html',
        {
            'user_profile': user_profile,
            'username_profile_list': username_profile_list
        }
    )


# Vue gérant les likes (pour les posts)
@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter is None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('/')


# Vue gérant la page profil d'un utilisateur
@login_required(login_url='signin')
def profile(request, pk):
    try:
        user_object = get_object_or_404(User, username=pk)
        user_profile = Profile.objects.get(user=user_object)
        user_posts = Post.objects.filter(user=pk)
        user_post_length = len(user_posts)
        follower = request.user
        user = user_object

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            button_text = 'Ne plus suivre'
        else:
            button_text = 'Suivre'

        # nbr de personnes qui suivent l'utilisateur
        user_followers = len(FollowersCount.objects.filter(user=user))
        # nbr de personnes que suit l'utilisateur
        user_following = len(FollowersCount.objects.filter(follower=follower))
        # recupération des posts de l'utilisateur
        feed_list = list(user_posts)
        feed_list.sort(key=lambda x: x.created_at, reverse=True)
        # Récupérer les critiques associées à chaque post
        # Créer un dictionnaire pour stocker les critiques associées à chaque poste
        post_reviews = {}
        for post in feed_list:
            reviews = Review.objects.filter(post=post).order_by('-time_created')
            has_user_reviewed = reviews.filter(user=request.user).exists()
            post_reviews[post] = {
                'reviews': reviews,
                'has_user_reviewed': has_user_reviewed
            }
        # recup des utilisateurs suivi
        # on commence par recupérer tous les objets FollowersCount de l'utilisateur connecté
        followersCount_for_user_connected = FollowersCount.objects.filter(follower=follower)
        # Pour chaque objet FollowersCount on recupere l'utilisateur et on l'ajoute à une liste
        user_following_all = [fc.user for fc in followersCount_for_user_connected]
        # On s'assure que l'utilisateur lui meme n'est pas compté dans la liste des utilisateurs suivi
        current_user = User.objects.filter(username=request.user.username)
        final_following_list = [x for x in list(user_following_all) if (x not in list(current_user))]
        username_profile = []
        username_profile_list = []

        for users in final_following_list:
            username_profile.append(users.id)
        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        followings_username_profile_list = list(chain(*username_profile_list))
        # Création d'une liste de valeurs pour l'utiliser dans le template
        rating_values = list(range(1, 6))

        context = {
            'user_object': user_object,
            'user_profile': user_profile,
            'user_posts': user_posts,
            'user_post_length': user_post_length,
            'button_text': button_text,
            'user_followers': user_followers,
            'user_following': user_following,
            'post_reviews': post_reviews,
            'rating_values': rating_values,
            'followings_username_profile_list': followings_username_profile_list,
        }
        return render(request, 'profile.html', context)
    except Http404:
        messages.info(request, "Profil inexistant.", extra_tags='no_profile')
        return redirect('/profile/'+request.user.username)


# Vue gérant le suivi ou non d'un utilisateur
@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower_username = request.POST['follower']
        # On verifie que l'utilisateur qui initie la demande est bien l'utilisateur connecté
        if follower_username == request.user.username:
            user_username = request.POST['user']
            follower = User.objects.get(username=follower_username)
            user = User.objects.get(username=user_username)

            if FollowersCount.objects.filter(follower=follower, user=user).first():
                delete_follower = FollowersCount.objects.get(follower=follower, user=user)
                delete_follower.delete()
                return redirect('/profile/'+user.username)
            else:
                new_follower = FollowersCount.objects.create(follower=follower, user=user)
                new_follower.save()
                return redirect('/profile/'+user.username)
        else:
            messages.info(
                request,
                "Vous ne pouvez pas réaliser cette action pour quelqu'un d'autre", extra_tags='not_user_connected'
            )
            return redirect('/profile/'+request.user.username)

    else:
        return redirect('/')


# Vue gérant la page setting.html (les paramètres utilisateur)
@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') is None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('image') is not None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return render(request, 'setting.html', {'user_profile': user_profile})
    return render(request, 'setting.html', {'user_profile': user_profile})


# Vue gérant la page d'inscription
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Cet email est déjà existant")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Ce nom d'utilisateur est déjà existant")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # connecter l'utilisateur et le rediriger vers la page settings
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # créer un objet Profile pour le nouvel utilisateur
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, "La confirmation du mot de passe n'est pas identique")
            return redirect('signup')
    else:
        return render(request, 'signup.html')


# Vue gérant la connexion
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Identifiants invalides')
            return redirect('signin')
    else:
        return render(request, 'signin.html')


# Vue gérant la déconnexion d'un utilisateur
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
