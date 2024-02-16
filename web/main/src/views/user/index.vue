<template>
  <div class="container">
    <Breadcrumb :items="['menu.user']"/>
    <div class="header">
      <a-space :size="12" direction="vertical" align="center">
        <a-avatar :size="64">
          <img :src="userInfo.avatar"/>
        </a-avatar>
        <a-typography-title :heading="6" style="margin: 0">
          {{ userInfo.name }}
        </a-typography-title>
        <div class="user-msg">
          <a-space :size="18">
            <div>
              <icon-user/>
              <a-typography-text>{{ userInfo.name }}</a-typography-text>
            </div>
            <div>
              <icon-email/>
              <a-typography-text>
                {{ userInfo.email }}
              </a-typography-text>
            </div>
            <div>
              <icon-user-group/>
              <a-typography-text>
                {{ userInfo.inviter }}
              </a-typography-text>
            </div>
          </a-space>
        </div>
      </a-space>
    </div>
    <div class="gallery">
      <div v-if="userInfo.inviter == null">
        <div class="content">
          <a-space>
            <a-input v-model="inviter" :style="{width:'320px'}" placeholder="填写邀请人后刷新页面开启机器人功能" allow-clear/>
            <a-button type="primary" @click="updateInviterInfo">确定</a-button>
          </a-space>
        </div>
      </div>
      <div v-else>
        <div v-if="userInfo.inviteNum != undefined && userInfo.inviteNum>0">
          <a-card class="general-card" :title="$t('我的相册')">
            <template #extra>
              <a-link href="/#/myalbum">查看更多</a-link>
            </template>
            <a-row :gutter="16">
              <a-col
                  v-for="(album, index) in albumList"
                  :key="index"
                  :xs="12"
                  :sm="12"
                  :md="12"
                  :lg="12"
                  :xl="8"
                  :xxl="8"
                  class="my-album-item"
              >
                <a-card>
                  <template #cover>
                    <div
                        :style="{
                          marginTop: '10px',
                          padding: '10px',
                          height: 'auto',
                          overflow: 'hidden',
                        }"
                    >
                      <img
                          :style="{ width: '100%', height: 'auto' }"
                          alt="dessert"
                          :src="album.cover"
                      />
                    </div>
                  </template>
                  <a-skeleton v-if="loading" :loading="loading" :animation="true">
                    <a-skeleton-line :rows="3"/>
                  </a-skeleton>
                  <a-space v-else direction="vertical">
                    <a-typography-text bold>
                      {{ album.album_name }}
                    </a-typography-text>
                    <a-typography-text type="secondary">
                      {{ album.desc }}
                    </a-typography-text>
                    <a-space>
                      <a-typography-text type="secondary">
                        共 {{ album.image_num }} 张
                      </a-typography-text>
                    </a-space>
                  </a-space>
                </a-card>
              </a-col>
            </a-row>
          </a-card>
        </div>
        <div v-else>
          <div class="content">
            <a-typography-text>
              邀请一人开启相册及分享功能哦～（暂未过滤自己邀请自己）
            </a-typography-text>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script lang="ts">
import {useUserStore} from '@/store';
import {updateInviterInfoApi} from '@/api/user';
import {Message} from "@arco-design/web-vue";

const userInfo = useUserStore();

export default {
  name: 'User',
  data() {
    return {
      "userInfo": userInfo,
      "avatar": userInfo.avatar,
      "inviter": userInfo.inviter,
      "email": userInfo.email,
      "albumList": userInfo.albumList,
      "loading": false,
    }
  },
  created() {
    return null
  },
  methods: {
    updateInviterInfo() {
      updateInviterInfoApi({
        inviter: this.inviter
      }).then(
        ()=>{
          Message.success("邀请人更新成功，请刷新页面～");
        }
      ).catch(
        ()=>{
          Message.error("邀请人更新失败，请确认信息后重试～");
        }
      )
    }
  }
};
</script>

<style scoped lang="less">

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

.header {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 204px;
  color: var(--gray-10);
  background: url(//p3-armor.byteimg.com/tos-cn-i-49unhts6dw/41c6b125cc2e27021bf7fcc9a9b1897c.svg~tplv-49unhts6dw-image.image) no-repeat;
  background-size: cover;
  border-radius: 4px;

  :deep(.arco-avatar-trigger-icon-button) {
    color: rgb(var(--arcoblue-6));

    :deep(.arco-icon) {
      vertical-align: -1px;
    }
  }

  .user-msg {
    .arco-icon {
      color: rgb(var(--gray-10));
    }

    .arco-typography {
      margin-left: 6px;
    }
  }
}

.gallery {
  margin-top: 10px;
}

.my-album {
  &-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
  }

  &-title {
    margin-top: 0 !important;
    margin-bottom: 18px !important;
  }

  &-list {
    display: flex;
    justify-content: space-between;
  }

  &-item {
    // padding-right: 16px;
    margin-bottom: 16px;

    &:last-child {
      padding-right: 0;
    }
  }
}
.content {
  position: relative;
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
  padding-top: 40px;
  padding-bottom: 40px;
}
</style>
