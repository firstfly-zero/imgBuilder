<template>
  <div class="container">
    <Breadcrumb :items="['menu.robot', 'menu.robot.lark']"/>
    <div class="content">
      <div class="frame-bg">
        <div class="frame-body">
          <div class="frame-aside">
            <a-steps :current="current" direction="vertical">
              <a-step>新建机器人</a-step>
              <a-step>添加机器人</a-step>
              <a-step>机器人事件订阅</a-step>
            </a-steps>
          </div>
          <div class="frame-main">
            <div class="main-content">
              <div v-if="current===1" style="margin-top: 15%;width: 400px">
                去<a-link href="https://open.feishu.cn/app/" target="_blank">飞书后台</a-link>新建机器人并查看 appId 与 appSecret
              </div>
              <div v-if="current===2" style="margin-top: 15%;width: 400px">
                <a-space direction="vertical">
                  <a-input v-model="appId" :style="{width:'200px'}" placeholder="请输入 appId" allow-clear/>
                  <a-input v-model="appSecret" :style="{width:'200px'}" placeholder="请输入 appSecret" allow-clear/>
                  <a-button type="primary" @click="addLarkBot">添加飞书机器人</a-button>
                </a-space>

              </div>
              <div v-if="current===3" style="margin-top: 15%;width: 400px">
                去<a-link href="https://open.feishu.cn/app/" target="_blank">飞书后台</a-link>添加机器人监听
              </div>
            </div>
          </div>
        </div>

      </div>
      <div class="main-bottom">
        <a-button :disabled="current===1" @click="onPrev">
          <icon-left />
          上一步
        </a-button>
        <a-button :disabled="current===3" @click="onNext">
          下一步
          <icon-right />
        </a-button>
      </div>

    </div>

  </div>
</template>

<script lang="ts">

import { ref } from 'vue';

import { addLarkBotApi } from '@/api/robot'

export default {
  name: 'Lark',
  setup() {
    const current = ref(1);

    const onPrev = () => {
      current.value = Math.max(1, current.value - 1);
    };

    const onNext = () => {
      current.value = Math.min(3, current.value + 1);
    };

    return {
      current,
      onPrev,
      onNext,
    }
  },
  data() {
    return {
      data: {},
      appId: "",
      appSecret: ""
    }
  },
  created() {
    return null
  },
  methods: {
    addLarkBot(){
      addLarkBotApi({
        app_id: this.appId,
        app_secret: this.appSecret
      }).then(
          (res)=>{
            this.data = res.data
            this.$message.success("添加成功，请刷新页面")
          }
      )
    }
  }
};
</script>

<style scoped lang="less">

.frame-bg {
  max-width: 780px;
  padding: 40px;
  background: var(--color-fill-2);
}

.frame-body {
  display: flex;
  background: var(--color-bg-2);
}

.frame-aside {
  padding: 24px;
  height: 272px;
  border-right: 1px solid var(--color-border);
}

.frame-main {
  width: 100%;
}

.main-content {
  text-align: center;
  line-height: 50px;
}

.main-bottom {
  display: flex;
  justify-content: center;

  button {
    margin: 0 20px;
  }
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
  }
}
</style>
