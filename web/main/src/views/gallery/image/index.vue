<template>
  <div class="container">
    <Breadcrumb :items="['menu.gallery', 'menu.image']" />
    <a-row :gutter="20" align="stretch">
      <a-col :span="24">
        <a-card class="general-card" title="图片列表">
          <template #extra>
            <a-space>
              <a-button type="primary" @click="openCreateAlbum">新建相册</a-button>
              <a-button type="primary" @click="openUploadImage">上传图片</a-button>
            </a-space>
          </template>
          <a-row justify="space-between">
            <a-col :span="24">
              <a-tabs :default-active-tab="1" type="rounded">
                <a-tab-pane v-for="album in albumList" :key="album.id" :title="album.title">
                  <ImageList
                    :albumId="album.id"
                    :imageList = "album.imageList"
                    @deleteImage="deleteImage"
                  />
                </a-tab-pane>
              </a-tabs>
            </a-col>
          </a-row>
        </a-card>
      </a-col>
    </a-row>

    <a-modal v-model:visible="isUploadImage" title="上传图片" @ok="uploadImage">
      <div style="margin-right: 50px">
        <a-form :model="newImage">
          <a-form-item field="tag" label="标签">
            <a-input v-model="newImage.tag" />
          </a-form-item>
          <a-form-item field="album" label="相册">
            <a-select v-model="newImage.album">
              <a-option v-for="album in albumList" :key="album.id" :value="album.id">{{ album.title }}</a-option>
            </a-select>
          </a-form-item>
        </a-form>
        <div style="margin-left: 40px; margin-top: 30px">
          <a-upload
              draggable
              action="/api/v1/gallery/uploadImage"
              :auto-upload="true"
              :headers="headers"
              @success="upload_success"
          />
        </div>
      </div>

    </a-modal>

    <a-modal v-model:visible="isCreateAlbum" title="新建相册" @ok="createAlbum">
      <div style="margin-right: 50px">
        <a-form :model="newAlbum">
          <a-form-item field="album_name" label="相册名">
            <a-input v-model="newAlbum.album_name" placeholder="相册名，图片上传时使用" />
          </a-form-item>
          <a-form-item field="title" label="标题">
            <a-input v-model="newAlbum.title" placeholder="相册标题，后台展示时使用"/>
          </a-form-item>
          <a-form-item field="desc" label="备注">
            <a-input v-model="newAlbum.desc" placeholder="请输入描述信息"/>
          </a-form-item>
        </a-form>
      </div>
    </a-modal>

  </div>
</template>

<script lang="ts">
  import { getAlbumListApi, uploadImage2AlbumApi, createAlbumApi } from '@/api/gallery';
  import { useUserStore } from '@/store';
  import { Message } from '@arco-design/web-vue';
  import ImageList from './components/image-list.vue';


  export default {
    name: 'IbImage',
    components: {
      ImageList
    },
    data(){
      return {
        galleryId: "1",
        albumList: [
          {
            "id": 1,
            "album_name": "默认图库-sd",
            "title": "默认图库-sd",
            "desc": "默认图库",
            "image_num": 0,
            "status": "public",
            "imageList": []
          }
        ],
        isUploadImage: false,
        newImage: {
          "album": "",
          "url": "",
          "height": "",
          "width": "",
          "tag": ""
        },
        isCreateAlbum: false,
        newAlbum: {
          gallery_id: this.galleryId,
          album_name: "",
          title: "",
          desc: ""
        },

        headers: {
          "Authorization": `Bearer ${window.localStorage.getItem("token")}`
        },
      }
    },
    created() {
      const userStore = useUserStore();
      // @ts-ignore
      this.galleryId = userStore.galleryId;
      this.loadData();
    },
    methods: {
      deleteImage(){
        this.loadData();
      },
      loadData(){
        getAlbumListApi(this.galleryId).then(
            (res)=>{
              this.albumList = res.data
            }
        ).catch()
      },
      openUploadImage(){
        this.isUploadImage = true
      },
      openCreateAlbum(){
        this.isCreateAlbum = true
      },

      upload_success(response?: any) {
        this.newImage.url = response.response.data.url
        this.newImage.height = response.response.data.height
        this.newImage.width = response.response.data.width
      },
      uploadImage() {
        uploadImage2AlbumApi({
          "album_id": this.newImage.album,
          "url": this.newImage.url,
          "height": this.newImage.height,
          "width": this.newImage.width,
          "tag": this.newImage.tag
        }).then(
            ()=>{
              this.isUploadImage = false;
              Message.success("图片上传成功");
              this.loadData()
            }
        ).catch()
      },
      createAlbum(){
        createAlbumApi({
          gallery_id: this.galleryId,
          album_name: this.newAlbum.album_name,
          title: this.newAlbum.title,
          desc: this.newAlbum.desc
        }).then(
            ()=>{
              this.isCreateAlbum = false;
              Message.success("相册创建成功");
              this.loadData()
            }
        ).catch()
      }

    }
  };
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px 20px;
    :deep(.arco-list-content) {
      overflow-x: hidden;
    }

    :deep(.arco-card-meta-title) {
      font-size: 14px;
    }
  }
  :deep(.arco-list-col) {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: space-between;
  }

  :deep(.arco-list-item) {
    width: 33%;
  }

  :deep(.block-title) {
    margin: 0 0 12px 0;
    font-size: 14px;
  }
  :deep(.list-wrap) {
    // min-height: 140px;
    .list-row {
      align-items: stretch;
      .list-col {
        margin-bottom: 16px;
      }
    }
    :deep(.arco-space) {
      width: 100%;
      .arco-space-item {
        &:last-child {
          flex: 1;
        }
      }
    }
  }
</style>
