<template>
  <div class="container">
    <div>
      <p class="subtitle">
        Wizard определил ваше направление:
      </p>

      <p class="title">
        {{ direction }}
      </p>
    </div>
  </div>
</template>

<script>
export default {
  async asyncData ({ params, $axios, route }) {
    const { groups } = route.query
    const direction = await $axios.$get(`http://127.0.0.1:8080/api/v1/direction?groups=${groups}`)
    return { direction }
  }
}
</script>

<style>
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.title {
  font-family: "Quicksand", "Source Sans Pro", -apple-system, BlinkMacSystemFont,
    "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  display: block;
  font-weight: 300;
  font-size: 80px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
  max-width: 800px;
}
</style>
