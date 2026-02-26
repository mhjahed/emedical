# media_manager/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q

from .models import MediaFolder, MediaFile, Gallery, GalleryImage
from accounts.decorators import superadmin_required, medical_staff_required


@superadmin_required
def media_library(request):
    """Main media library view"""
    folders = MediaFolder.objects.filter(parent=None)
    files = MediaFile.objects.filter(folder=None)
    
    # Filter
    folder_id = request.GET.get('folder')
    file_type = request.GET.get('type')
    search = request.GET.get('search')
    
    if folder_id:
        current_folder = get_object_or_404(MediaFolder, id=folder_id)
        folders = current_folder.subfolders.all()
        files = current_folder.files.all()
    else:
        current_folder = None
    
    if file_type:
        files = files.filter(file_type=file_type)
    
    if search:
        files = files.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )
    
    paginator = Paginator(files, 24)
    page = request.GET.get('page')
    files = paginator.get_page(page)
    
    return render(request, 'media_manager/library.html', {
        'folders': folders,
        'files': files,
        'current_folder': current_folder,
        'file_type': file_type,
        'search': search
    })


@superadmin_required
def upload_file(request):
    """Upload new file"""
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        folder_id = request.POST.get('folder')
        folder = None
        
        if folder_id:
            folder = get_object_or_404(MediaFolder, id=folder_id)
        
        uploaded_files = []
        for file in files:
            media_file = MediaFile.objects.create(
                title=file.name,
                file=file,
                folder=folder,
                uploaded_by=request.user
            )
            uploaded_files.append({
                'id': media_file.id,
                'title': media_file.title,
                'url': media_file.file.url,
                'type': media_file.file_type
            })
        
        return JsonResponse({'success': True, 'files': uploaded_files})
    
    folders = MediaFolder.objects.all()
    return render(request, 'media_manager/upload.html', {'folders': folders})


@superadmin_required
def create_folder(request):
    """Create new folder"""
    if request.method == 'POST':
        name = request.POST.get('name')
        parent_id = request.POST.get('parent')
        
        from django.utils.text import slugify
        slug = slugify(name)
        
        parent = None
        if parent_id:
            parent = get_object_or_404(MediaFolder, id=parent_id)
        
        folder = MediaFolder.objects.create(
            name=name,
            slug=slug,
            parent=parent,
            created_by=request.user
        )
        
        return JsonResponse({'success': True, 'folder_id': folder.id})
    
    return JsonResponse({'success': False})


@superadmin_required
def delete_file(request, file_id):
    """Delete file"""
    file = get_object_or_404(MediaFile, id=file_id)
    file.file.delete()
    file.delete()
    return JsonResponse({'success': True})


@superadmin_required
def delete_folder(request, folder_id):
    """Delete folder and its contents"""
    folder = get_object_or_404(MediaFolder, id=folder_id)
    
    # Delete all files in folder
    for file in folder.files.all():
        file.file.delete()
        file.delete()
    
    folder.delete()
    return JsonResponse({'success': True})


@superadmin_required
def file_details(request, file_id):
    """Get/update file details"""
    file = get_object_or_404(MediaFile, id=file_id)
    
    if request.method == 'POST':
        file.title = request.POST.get('title', file.title)
        file.alt_text = request.POST.get('alt_text', file.alt_text)
        file.description = request.POST.get('description', file.description)
        file.save()
        return JsonResponse({'success': True})
    
    return JsonResponse({
        'id': file.id,
        'title': file.title,
        'url': file.file.url,
        'type': file.file_type,
        'size': file.file_size_display,
        'alt_text': file.alt_text,
        'description': file.description,
        'width': file.width,
        'height': file.height,
        'created_at': file.created_at.strftime('%Y-%m-%d %H:%M')
    })


# ============ Gallery Views ============

@superadmin_required
def gallery_list(request):
    """List all galleries"""
    galleries = Gallery.objects.all()
    return render(request, 'media_manager/gallery_list.html', {'galleries': galleries})


@superadmin_required
def gallery_detail(request, slug):
    """View/manage gallery"""
    gallery = get_object_or_404(Gallery, slug=slug)
    available_images = MediaFile.objects.filter(file_type='image')
    
    return render(request, 'media_manager/gallery_detail.html', {
        'gallery': gallery,
        'available_images': available_images
    })


@superadmin_required
def add_to_gallery(request, gallery_id):
    """Add image to gallery"""
    if request.method == 'POST':
        gallery = get_object_or_404(Gallery, id=gallery_id)
        image_id = request.POST.get('image_id')
        caption = request.POST.get('caption', '')
        
        image = get_object_or_404(MediaFile, id=image_id)
        
        GalleryImage.objects.create(
            gallery=gallery,
            image=image,
            caption=caption,
            order=gallery.images.count()
        )
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})


# ============ Public Gallery View ============

def public_gallery(request, slug):
    """Public gallery view"""
    gallery = get_object_or_404(Gallery, slug=slug, is_active=True)
    return render(request, 'media_manager/public_gallery.html', {'gallery': gallery})