import axios from 'axios';

// 图片管理相关
export function getAlbumListApi(galleryId: string) {
  return axios.get(`/api/v1/gallery/getAlbumList?galleryId=${galleryId}`);
}

export interface ImageUploadInfo {
  album_id: string;
  tag: string;
  url: string;
  width: string;
  height: string;
}

export function uploadImage2AlbumApi(params: ImageUploadInfo) {
  return axios.post(`/api/v1/gallery/uploadImage2Album`, params);
}

export interface AlbumCreateInfo {
  gallery_id: string;
  album_name: string;
  title: string;
  desc: string
}

export function createAlbumApi(params: AlbumCreateInfo) {
  return axios.post(`/api/v1/gallery/createAlbum`, params);
}

export interface AlbumUpdateInfo {
  id: string;
  album_name: string;
  title: string;
  desc: string
}
export function updateAlbumApi(params: AlbumUpdateInfo) {
  return axios.post(`/api/v1/gallery/updateAlbum`, params);
}

export function deleteImageApi(imageId: string) {
  return axios.get(`/api/v1/gallery/deleteImage?imageId=${imageId}`);
}

export interface shareInfo {
  share_type: string;
  image_url: string;
}
export function shareImageApi(params: shareInfo) {
  return axios.post(`/api/v1/user/createShare`, params);
}

export async function downloadImageApi(imgUrl: string) {
  const response = await fetch(`/api/v1/gallery/downloadImage?imgUrl=${imgUrl}`);
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'image.jpg'; // 或者你想要的任何其他文件名
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

export function deleteAlbumApi(albumId: string) {
  return axios.get(`/api/v1/gallery/deleteAlbum?albumId=${albumId}`);
}

export function searchAlbumApi(searchText: string) {
  return axios.post(`/api/v1/gallery/searchAlbum`, { "searchText": searchText });
}




