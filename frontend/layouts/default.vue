<template>
  <div>
    <Nuxt />
  </div>
</template>

<style>
html {
  font-family:
    'Source Sans Pro',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    'Helvetica Neue',
    Arial,
    sans-serif;
  font-size: 16px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
}

.button, .input {
  display: inline-block;
  border-radius: 4px;
  text-decoration: none;
  background-color: transparent;
  font-size: 16px;
  transition: all ease 400ms;
  border: 1px solid;
  outline: 0;
}

.button {
  padding: 10px 30px;
}

.input {
  padding: 10px;
}

.button:hover {
  cursor: pointer;
}

.button--green, .input--green {
  border-color: #3b8070;
  color: #3b8070;
}

.button--green:hover {
  color: #fff;
  background-color: #3b8070;
}

.button--grey, .input--grey {
  border-color: #35495e;
  color: #35495e;
}

.button--grey:hover {
  color: #fff;
  background-color: #35495e;
}
</style>
