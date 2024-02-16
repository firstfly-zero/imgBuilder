<template>
  <div class="container">
    <Breadcrumb :items="['menu.gallery', 'menu.album']"/>
    <div class="content">
      <a-layout style="width: 100%;">
        <a-layout-header>
          <div style="margin-top: 20px;">
            <a-input-search
                :style="{width:'320px',height: '30px'}"
                placeholder="请输入相册名"
                @change="searchAlbum"
                @search="searchAlbum"
            />
          </div>
        </a-layout-header>
        <a-layout-content class="album-list-container">
          <div class="album-list-table">
            <a-table :columns="albumColumns" :data="albumList">
              <template #optional="{ record }">
                <a-space>
                  <a-button type="outline" @click="openEditAlbum(record)">编辑</a-button>
                  <a-button type="outline" status="danger" @click="openDeleteAlbum(record)">删除</a-button>
                </a-space>
              </template>
            </a-table>
          </div>

          <a-modal v-model:visible="isDeleteAlbum" title="删除相册" @ok="deleteAlbum">
            <div>删除后无法恢复，确认删除吗？</div>
          </a-modal>

          <a-modal v-model:visible="isEditAlbum" title="编辑相册" @ok="updateAlbum">
            <div style="margin-right: 50px">
              <a-form :model="editingAlbumInfo">
                <a-form-item field="album_name" label="相册名">
                  <a-input v-model="editingAlbumInfo.album_name" />
                </a-form-item>
                <a-form-item field="title" label="标题">
                  <a-input v-model="editingAlbumInfo.title" />
                </a-form-item>
                <a-form-item field="description" label="描述">
                  <a-input v-model="editingAlbumInfo.desc" />
                </a-form-item>
              </a-form>
            </div>

          </a-modal>

        </a-layout-content>
      </a-layout>
    </div>
  </div>
</template>

<script lang="ts">
import { getAlbumListApi, deleteAlbumApi, updateAlbumApi, searchAlbumApi } from "@/api/gallery"
import { useUserStore } from '@/store';

const userStore = useUserStore();

export default {
  name: 'Album',
  data() {
    return {
      galleryId: "",
      albumColumns: [
        {
          title: '相册名',
          dataIndex: 'album_name',
        },{
          title: '标题',
          dataIndex: 'title',
        },{
          title: '备注',
          dataIndex: 'desc',
        },{
          title: '图片数',
          dataIndex: 'image_num',
        },{
          title: '操作',
          slotName: 'optional'
        }],
      albumList: [],
      isEditAlbum: false,
      isDeleteAlbum: false,
      editingAlbumInfo: {
        id: "",
        album_name: "",
        title: "",
        desc: ""
      },
      deleteAlbumInfo: {
        id: "0"
      },

    }
  },
  created() {
    this.loadData()
  },
  methods: {
    loadData(){
      if(userStore.galleryId?.toString()!==undefined){
        this.galleryId=userStore.galleryId?.toString()
      }
      getAlbumListApi(this.galleryId).then(
          (res)=>{
            this.albumList = res.data
          }
      ).catch()
    },
    openEditAlbum(album: any){
      this.editingAlbumInfo = album;
      this.isEditAlbum = true
    },
    openDeleteAlbum(album: any){
      this.deleteAlbumInfo = album
      this.isDeleteAlbum = true
    },
    deleteAlbum(){
      deleteAlbumApi(this.deleteAlbumInfo.id).then(
          () => {
            this.isDeleteAlbum = false
            this.loadData()
          }
      ).catch()
    },
    updateAlbum(){
      updateAlbumApi({
        id: this.editingAlbumInfo.id,
        album_name: this.editingAlbumInfo.album_name,
        title: this.editingAlbumInfo.title,
        desc: this.editingAlbumInfo.desc
      }).then(
          () => {
            this.isEditAlbum = false
            this.loadData()
          }
      ).catch()
    },
    searchAlbum(value: string){
      searchAlbumApi(value).then(
          (res)=>{
            this.albumList = res.data
          }
      )
    },
  }
};
</script>

<style scoped lang="less">
.album-list-container {
  padding: 0 20px 20px 20px;
}

.album-list-table {
  width: 100%;
  padding-top: 30px;
}

.container {
  padding: 0 20px 20px 20px;
  height: calc(100% - 40px);

  :deep(.content) {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
    background-color: var(--color-bg-1);
    border-radius: 4px;
  }
}
</style>
