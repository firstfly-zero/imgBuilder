<template>
  <div class="login-form-wrapper">
    <div class="login-form-title">{{ $t('register.form.title') }}</div>
    <div class="login-form-sub-title">{{ $t('register.form.subtitle') }}</div>
    <a-form
        ref="registerForm"
        :model="registerInfo"
        class="login-form"
        layout="vertical"
    >
      <a-form-item
          field="username"
          :rules="[{ required: true, message: $t('login.form.userName.errMsg') }]"
          :validate-trigger="['change', 'blur']"
          hide-label
      >
        <a-input
            v-model="registerInfo.username"
            :placeholder="$t('login.form.userName.placeholder')"
        >
          <template #prefix>
            <icon-user />
          </template>
        </a-input>
      </a-form-item>
      <a-form-item
          field="password"
          :rules="[{ required: true, message: $t('login.form.password.errMsg') }]"
          :validate-trigger="['change', 'blur']"
          hide-label
      >
        <a-input-password
            v-model="registerInfo.password"
            :placeholder="$t('login.form.password.placeholder')"
            allow-clear
        >
          <template #prefix>
            <icon-lock />
          </template>
        </a-input-password>
      </a-form-item>
      <a-form-item
          field="email"
          :rules="[{ required: true, message: $t('register.form.email.errMsg') }]"
          :validate-trigger="['change', 'blur']"
          hide-label
      >
        <a-input
            v-model="registerInfo.email"
            :placeholder="$t('register.form.email.placeholder')"
        >
          <template #prefix>
            <icon-email />
          </template>
        </a-input>
      </a-form-item>
      <a-form-item
          field="code"
          :rules="[{ required: true, message: $t('register.form.code.errMsg') }]"
          :validate-trigger="['change', 'blur']"
          hide-label
      >
        <a-space>
          <a-input
              v-model="registerInfo.code"
              :placeholder="$t('register.form.code.placeholder')"
              allow-clear
          >
            <template #prefix>
              <icon-safe />
            </template>
          </a-input>
          <a-button :type="sendVerifyCodeButtonType" :loading="isSendingVerifyCode" @click="sendVerifyCode">{{ sendVerifyCodeButtonText }}</a-button>
        </a-space>
      </a-form-item>


      <a-space :size="16" direction="vertical">
        <a-button type="primary" html-type="submit" long :loading="isRegistering" @click="register">
          {{ $t('register.form.register') }}
        </a-button>
      </a-space>
    </a-form>
  </div>
</template>

<script lang="ts">
import { registerApi, sendVerifyCodeApi } from '@/api/user';
import { Message } from '@arco-design/web-vue';

export default {
    name: "Registerform",
    data(){
      return {
        registerInfo: {
          username: "",
          password: "",
          email: "",
          code: ""
        },
        sendVerifyCodeButtonType: "primary" as "text" | "dashed" | "outline" | "primary" | "secondary" | undefined,
        sendVerifyCodeButtonText: "发送验证码",
        isSendingVerifyCode: false,
        isRegistering: false
      }
    },
    methods: {
      sendVerifyCode(){
        this.isSendingVerifyCode = true
        if(this.sendVerifyCodeButtonType === "primary"){
          sendVerifyCodeApi({
            email: this.registerInfo.email
          }).then(
              (res)=>{
                this.isSendingVerifyCode = false
                this.sendVerifyCodeButtonType = "dashed" as "text" | "dashed" | "outline" | "primary" | "secondary" | undefined
                this.sendVerifyCodeButtonText = "验证码已发送"
                Message.success(res.data)
              }
          ).catch(
              (res)=>{
                this.isSendingVerifyCode = false
                Message.error(res.msg)
              }
          )
        }
      },
      register(){
        this.isRegistering=true
        registerApi({
          username: this.registerInfo.username,
          password: this.registerInfo.password,
          email: this.registerInfo.email,
          code: this.registerInfo.code,
        }).then(
            (res)=>{
              this.isRegistering=false
              Message.success(res.data)
              window.location.reload()
            }
        ).catch(
            (res)=>{
              this.isRegistering=false
              Message.error(res.msg)
            }
        )
      }
    }

  }
</script>

<style lang="less" scoped>
.login-form {
  &-wrapper {
    width: 320px;
  }

  &-title {
    color: var(--color-text-1);
    font-weight: 500;
    font-size: 24px;
    line-height: 32px;
  }

  &-sub-title {
    color: var(--color-text-3);
    font-size: 16px;
    line-height: 24px;
  }

  &-error-msg {
    height: 32px;
    color: rgb(var(--red-6));
    line-height: 32px;
  }

  &-password-actions {
    display: flex;
    justify-content: space-between;
  }

  &-register-btn {
    color: var(--color-text-3) !important;
  }
}
</style>
