<template>
  <div class="card-wrap">
    <a-image
      :src=url
      :title=tag
      width="260"
    >
      <template #extra>
        <div class="actions">
          <a-space>
            <span class="action" @click="shareImage(url)"><icon-share-alt size="20"/></span>
            <span class="action" @click="onDownLoad(url)"><icon-download size="20"/></span>
            <span class="action" @click="copyId(url)"><icon-copy size="20"/></span>
            <span class="action" @click="openDeleteImage"><icon-delete size="20"/></span>
          </a-space>
        </div>
      </template>
    </a-image>
    <a-modal v-model:visible="isDeleteImage" title="删除图片" @ok="deleteImage(id)">
      <div>删除后不可恢复，确定要删除吗？</div>
    </a-modal>
  </div>
</template>

<script lang="ts">
import copy from 'clipboard-copy';
import { downloadImageApi, deleteImageApi, shareImageApi } from '@/api/gallery';
import {Message} from "@arco-design/web-vue";

export default {
  name: 'ImageList',
  props: ['id', 'url', 'tag'],
  emits: ['deleteImage'],
  data() {
    return {
      isDeleteImage: false,
    }
  },
  created() {
    return null
  },
  methods: {
    openDeleteImage() {
      this.isDeleteImage = true;
    },
    deleteImage(id: string) {
      deleteImageApi(id).then(
        ()=>{
          this.$emit('deleteImage', id);
          this.isDeleteImage = false;
        }
      ).catch()
    },
    copyId(url: string){
      copy(url);
      Message.success(`图片链接已复制`)
    },
    shareImage(url: string) {
      shareImageApi({
        "share_type": "image",
        "image_url": url
      }).then(
          (res)=>{
            copy(`${window.location.protocol.toString()}//${window.location.host.toString()}/#/share?shareId=${res.data.share_id}`)
            Message.success(`分享链接已复制`)
          }
      ).catch(
          (res)=>{
            console.log(res);
            copy("error")
          }
      )
    },
    async onDownLoad(url: string){
      await downloadImageApi(url)
    }
  }
};

</script>

<style scoped lang="less">

  .action {
    &:hover {
      transform: translateY(-4px);
    }
  }
  .card-wrap {
    height: 100%;
    display: inline-flex;
    transition: all 0.3s;
    border-radius: 4px;
    margin-bottom: 10px;

    :deep(.arco-card) {
      height: 100%;
      border-radius: 4px;

      .arco-card-body {
        height: 100%;

        .arco-space {
          width: 100%;
          height: 100%;

          .arco-space-item {
            height: 100%;

            &:last-child {
              flex: 1;
            }

            .arco-card-meta {
              height: 100%;
              display: flex;
              flex-flow: column;

              .arco-card-meta-content {
                flex: 1;

                .arco-card-meta-description {
                  margin-top: 8px;
                  color: rgb(var(--gray-6));
                  line-height: 20px;
                  font-size: 12px;
                }
              }

              .arco-card-meta-footer {
                margin-top: 0;
              }
            }
          }
        }
      }
    }

    :deep(.arco-card-meta-title) {
      display: flex;
      align-items: center;

      // To prevent the shaking
      line-height: 28px;
    }

    :deep(.arco-skeleton-line) {
      &:last-child {
        display: flex;
        justify-content: flex-end;
        margin-top: 20px;
      }
    }
  }
</style>
