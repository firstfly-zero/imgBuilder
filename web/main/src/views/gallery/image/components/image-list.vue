<template>
  <div class="list-wrap">
    <a-row style="margin-bottom: 16px;">
      <a-col
          v-for="item in imageList" :key="item.id"
         :xs="{span: 14, offset: 0}"
         :sm="{span: 10, offset: 0}"
         :lg="{span: 8, offset: 0}"
         :xl="{span: 6, offset: 0}"
      >
        <ImageWrap
          :id="item.id"
          :height="item.height"
          :width="item.width"
          :tag="item.tag"
          :url="item.url"
          @deleteImage="deleteImage"
        />
      </a-col>
    </a-row>

  </div>
</template>

<script lang="ts">
  import ImageWrap from './image-wrap.vue';

  export default {
    name: 'ImageList',
    props: ['imageList'],
    components: {
      ImageWrap
    },
    data() {
      return {
      }
    },
    created() {

      return null
    },
    methods: {
      deleteImage(id: string){
        this.$emit('deleteImage', id);
      }
    }
  };


</script>

<style scoped lang="less">
.card-wrap {
  height: 100%;
  transition: all 0.3s;

  :deep(.arco-card-meta-description) {
    color: rgb(var(--gray-6));

    .arco-descriptions-item-label-inline {
      font-weight: normal;
      font-size: 12px;
      color: rgb(var(--gray-6));
    }

    .arco-descriptions-item-value-inline {
      color: rgb(var(--gray-8));
    }
  }
}

.empty-wrap {
  height: 200px;
  border-radius: 4px;

  :deep(.arco-card) {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;

    .arco-result-title {
      color: rgb(var(--gray-6));
    }
  }
}
</style>
