from django.urls import path
import gallery.views as galleryView

urlpatterns = [
    # 图片操作
    path("uploadImage", galleryView.upload_image),
    path("uploadImage2Album", galleryView.upload_image_to_album),
    path("getAlbumImageList", galleryView.get_album_image_list),
    path("getGalleryImageList", galleryView.get_gallery_image_list),
    path("deleteImage", galleryView.delete_image),
    path("downloadImage", galleryView.download_image),

    # 相册操作
    path("getAlbumList", galleryView.get_album_list),
    path("getAlbum", galleryView.get_album),
    path("createAlbum", galleryView.create_album),
    path("deleteAlbum", galleryView.delete_album),
    path("updateAlbum", galleryView.update_album),
    path("searchAlbum", galleryView.search_album),

    path("genSecret", galleryView.gen_secret),
    path("getSecret", galleryView.get_secret),
    path("exchangeSecret", galleryView.exchange_secret),
]