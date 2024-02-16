<template>
  <div class="container">
    <div class="logo">
      <a-space>
        <div class="logo-text">Image Builder</div>
      </a-space>
    </div>
    <LoginBanner />
    <div class="content">
      <div class="content-inner">
        <div v-if="isLogin">
          <LoginForm />
          <a-button type="text" long class="login-form-register-btn" @click="gotoRegister">
            {{ $t('login.form.gotoregister') }}
          </a-button>
        </div>
        <div v-else>
          <RegisterForm />
          <a-button type="text" long class="login-form-register-btn" @click="gotoLogin">
            {{ $t('login.form.gotologin') }}
          </a-button>
        </div>

      </div>
      <div class="footer">
        <LoginFooter />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import LoginFooter from '@/components/footer/index.vue';
  import LoginBanner from './components/banner.vue';
  import LoginForm from './components/login-form.vue';
  import RegisterForm from './components/register-form.vue';

  export default {
    name: 'Login',
    components: {
      LoginFooter,
      LoginBanner,
      LoginForm,
      RegisterForm
    },
    data() {
      return {
        isLogin: true
      }
    },
    methods: {
      gotoLogin(){
        this.isLogin = true
      },
      gotoRegister(){
        console.log("gotoRegister")
        this.isLogin = false
      }
    }
  }
</script>
<style lang="less" scoped>
  .container {
    display: flex;
    height: 100vh;

    .banner {
      width: 550px;
      background: linear-gradient(163.85deg, #1d2129 0%, #00308f 100%);
    }

    .content {
      position: relative;
      display: flex;
      flex: 1;
      align-items: center;
      justify-content: center;
      padding-bottom: 40px;
    }

    .footer {
      position: absolute;
      right: 0;
      bottom: 0;
      width: 100%;
    }
  }

  .logo {
    position: fixed;
    top: 24px;
    left: 22px;
    z-index: 1;
    display: inline-flex;
    align-items: center;

    &-text {
      margin-right: 4px;
      margin-left: 4px;
      color: var(--color-fill-1);
      font-size: 20px;
    }
  }
</style>

<style lang="less" scoped>
  // responsive
  @media (max-width: @screen-lg) {
    .container {
      .banner {
        width: 25%;
      }
    }
  }
</style>
