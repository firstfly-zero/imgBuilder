<template>
  <div class="container">
    <Breadcrumb :items="['menu.gallery', 'gallery.upload']"/>
    <div class="content">
      <div class="upload-component">
        命令模版管理
      </div>
    </div>
  </div>
</template>


<script lang="ts">
export default {
  name: 'CommandMan',
  data() {
    return {}
  },
  created() {
  },
  methods: {}
};
</script>

<style scoped lang="less">
.upload-component {
  width: 80%;
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
