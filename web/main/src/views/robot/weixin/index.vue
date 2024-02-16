<template>
  <div class="container">
    <Breadcrumb :items="['menu.robot', 'menu.robot.weixin']"/>
    <div class="content">
      <a-row>
        <a-col :span="9" :offset="2">
          <a-space size="large">
            <a-space direction="vertical" size="large">
              <a-space size="large">
                <a-checkbox v-model="config.switch_mj">mj机器人</a-checkbox>
                <a-checkbox v-model="config.switch_sd">sd机器人</a-checkbox>
                <a-checkbox v-model="config.switch_gpt">gpt机器人</a-checkbox>
              </a-space>
              <div>
                群白名单 <a-input v-model="config.group_name_white_list[0]" :style="{width:'320px'}" size="large" placeholder="请输入内容"></a-input><br/>
              </div>
              <div v-if="config.switch_mj">
                mj帮助文本 <a-input v-model="config.help_text_mj" :style="{width:'320px'}" size="large" placeholder="请输入内容"></a-input><br/>
              </div>
              <div v-if="config.switch_sd">
                sd帮助文本 <a-input v-model="config.help_text_sd" :style="{width:'320px'}" size="large" placeholder="请输入内容"></a-input><br/>
              </div>
              <div v-if="config.switch_gpt">
                gpt帮助文本 <a-input v-model="config.help_text_gpt" :style="{width:'320px'}" size="large" placeholder="请输入内容"></a-input><br/>
              </div>

            </a-space>
          </a-space>
        </a-col>
        <a-col :span="9" :offset="2">
          <a-space direction="vertical" size="large">
            <a-button type="primary" @click="addWxBot">添加机器人</a-button>
            <div id="QRcode" style="width: 320px; height: 320px">
              此处显示二维码
            </div>
          </a-space>
        </a-col>
      </a-row>
    </div>
  </div>
</template>


<script lang="ts">
  import { addWxBotApi, getWxBotDefaultConfig } from '@/api/robot';
  import { useUserStore } from '@/store';

  const userStore = useUserStore();

  export default {
    name: 'Weixin',
    data() {
      return {
        config: {
          "server": "http://127.0.0.1:8000",
          "group_name_white_list": [
            "ALL_GROUP"
          ],
          "ib_username": "",
          "switch_mj": false,
          "help_text_mj": "",
          "switch_sd": false,
          "help_text_sd": "",
          "switch_gpt": false,
          "help_text_gpt": "",
        },
      }
    },
    created() {
      getWxBotDefaultConfig().then(
          (res) => {
            this.config = res.data
          }
      ).catch()
      return null
    },
    methods: {
      addWxBot(){
        if(userStore.name?.toString()!==undefined){
          this.config.ib_username = userStore.name
        }
        addWxBotApi(JSON.stringify(this.config)).then(
          (res) => {
            const imageNode = document.createElement("img")
            imageNode.src=res.data.QRcode
            const qrNode=document.getElementById("QRcode")
            if(qrNode != null){
              qrNode.append(imageNode)
            }
          }
        ).catch()
      }
    }
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
