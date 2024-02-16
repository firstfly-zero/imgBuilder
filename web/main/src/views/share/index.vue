<template>
  <div v-if="shareIdUndefined">
    <header class="user-profile">
      <h1 class="nickname">分享加载失败，请检查shareId</h1>
    </header>
  </div>
  <div v-if="loadFinished" class="container">
    <header class="user-profile">
      <img :src="user.avatar" alt="User Avatar" class="avatar">
      <h1 class="nickname">{{ user.username }}</h1>
    </header>
    <section class="content">
      <div class="content-item">
        <div v-if="share.share_type==='mjImage'">
          <a-typography-title :heading="6" style="text-align:center;">来自Midjourney</a-typography-title>
          <img :src="JSON.parse(share.share_info).image" alt="AI Generated Image" class="generated-image">
          <a-divider />

          <a-card title="提示词">
            {{ JSON.parse(share.share_info).final_prompt }}
          </a-card>
        </div>
        <div v-if="share.share_type==='sdImage'">
          <a-typography-title :heading="6" style="text-align:center;">来自扩散模型</a-typography-title>
          <img :src="JSON.parse(share.share_info).image" alt="AI Generated Image" class="generated-image">
          <a-divider />

          <h2 class="content-title" style="text-align:center;">生成条件</h2>
          <ul class="conditions-list">
            <div v-for="(value, name) in JSON.parse(share.share_info).params" :key="name">
              <li><strong>{{ name }}：</strong>{{ value }}</li>
            </div>
          </ul>

        </div>
        <div v-if="share.share_type==='image'">
          <a-typography-title :heading="6" style="text-align:center;">来自用户</a-typography-title>
          <img :src="JSON.parse(share.share_info).image" alt="AI Generated Image" class="generated-image">
          <a-divider />
        </div>

      </div>
    </section>
  </div>
</template>

<script lang="ts">
  import { getShareApi } from '@/api/user';

  export default {
    name: "Share",
    data() {
      return {
        "shareId": "1",
        "loadFinished": false,
        "shareIdUndefined": false,
        "user": {
          "username": "admin",
          "avatar": "https://aiclub-1311445709.cos.ap-guangzhou.myqcloud.com/imgbuilder/9/1702750512/tmp/1702750512711.png"
        },
        "share": {
          "share_type": "sdImage",
          "share_info": "{\"image\": \"https://aiclub-1311445709.cos.ap-guangzhou.myqcloud.com/imgbuilder/15/1706072076/1706072074.png\", \"params\": {\"seed\": -1, \"steps\": 20, \"width\": 512, \"height\": 512, \"prompt\": \"Spring Festival Authentic Roast Fish Broadcast Activity Package\", \"cfg_scale\": 12, \"batch_size\": 1, \"sampler_name\": \"Euler a\", \"negative_prompt\": \"(worst quality:2),(low quality:2),(normal quality:2),lowres,watermark,\"}}"
        }
      }
    },
    created() {
      this.getShareInfo()
    },
    methods: {
      getShareInfo(){
        if (this.$router.currentRoute.value.query.shareId === undefined){
          this.shareIdUndefined = true
        } else {
          this.shareId = this.$router.currentRoute.value.query.shareId as string;
          getShareApi(this.shareId).then(
              (res)=>{
                this.user = res.data.user
                this.share = res.data.share
                this.loadFinished = true
              }
          ).catch()
        }

      }
    }

  }
</script>

<style scoped>

.container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.user-profile {
  text-align: center;
  margin-bottom: 20px;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 10px;
}

.nickname {
  color: #333;
  margin: 0;
}

.content-item {
  border-bottom: 1px solid #eee;
  padding-bottom: 20px;
  margin-bottom: 20px;
}

.content-title {
  color: #555;
}

.generated-text, .generated-image, .generated-audio, .generated-video {
  display: block;
  width: 100%;
  margin-top: 10px;
}

.actions {
  margin-top: 20px;
}

button, .link {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  text-decoration: none;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 10px;
}

button:hover, .link:hover {
  background-color: #0056b3;
}

.conditions-list {
  list-style-type: none; /* 移除默认的列表符号 */
  padding: 0;
  margin: 0;
}

.conditions-list li {
  background-color: #f0f0f0; /* 给列表项添加背景色 */
  margin-bottom: 5px; /* 添加列表项之间的间距 */
  padding: 10px; /* 添加内边距 */
  border-radius: 5px; /* 添加圆角边框 */
}

.conditions-list li strong {
  color: #333; /* 为列表项中的强调文本添加颜色 */
}


</style>
