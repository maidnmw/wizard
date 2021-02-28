<template>
  <div class="container-index">
    <div>
      <h1 class="title">
        Wizard
      </h1>
      <p class="subtitle">
        Поможет тебе подобрать программу обучения в УрФУ
      </p>

      <div class="buttons">
        <button
          class="button button--green"

          @click="onAuthVKClick()"
        >
          Авторизоваться через ВК
        </button>

        <p class="subtitle-2">
          Или введите свой ID ВК
        </p>

        <div class="groups">
          <div v-if="groupsError" class="groups-error">
            Профиль закрыт, попробуйте через авторизацию или
            <span class="groups-error-other" @click="onOtherIdClick()">введите другой ID</span>
          </div>

          <input v-model="vkId" class="input input--green" type="text" placeholder="XXX">

          <button
            class="button button--grey"

            @click="onGetGroupsByIdClick()"
          >
            Подобрать по ID
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      vkId: null,
      VK: null,
      groupsError: false
    }
  },

  head: {
    script: [
      { src: 'https://vk.com/js/api/openapi.js?168' }
    ]
  },

  mounted () {
    this.VK = window.VK

    this.VK.init({
      apiId: 7772790
    })
  },

  methods: {
    onAuthVKClick () {
      this.VK.Auth.login((response) => {
        if (response.status === 'connected') {
          this.vkId = response.session.user.id

          this.VK.Api.call('groups.get', { v: '5.73' }, (r) => {
            if (r.response) {
              this.redirectSuccess(r.response.items)
            }
          })
        }
      })
    },

    onGetGroupsByIdClick () {
      this.VK.Api.call('groups.get', { user_id: this.vkId, v: '5.73' }, (r) => {
        if (r.response) {
          this.redirectSuccess(r.response.items)
        } else {
          this.groupsError = true
        }
      })
    },

    onOtherIdClick () {
      this.vkId = null
      this.groupsError = false
    },

    redirectSuccess (groups) {
      this.$router.push(`/${this.vkId}?groups=${groups.join(',')}`)
    }
  }
}
</script>

<style>
.container-index {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  max-width: 800px;
}

.title {
  font-family: "Quicksand", "Source Sans Pro", -apple-system, BlinkMacSystemFont,
    "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.subtitle-2 {
  font-weight: 300;
  font-size: 25px;
  color: #526488;
  word-spacing: 5px;
  margin: 20px 0;
}

.groups {
  position: relative;
}

.groups-error {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255,255,255, 0.8);

  display: flex;
  justify-content: center;
  align-items: center;

  font-weight: 300;
  font-size: 18px;
  color: #ff4466;
  word-spacing: 5px;
}

.groups-error-other {
  text-decoration: underline;
  cursor: pointer;
  margin-left: 7px;
}

.buttons {
  padding-top: 15px;
}

.button--grey {
  margin-left: 15px;
}
</style>
