<script setup>

import { useRouter } from "vue-router";
const router = useRouter();

const Item_get = (id) => {
  router.push('/route/' + id);
}

</script>

<template>
  <nav class="navbar navbar-expand-sm bg-dark back">
    <div class="container-fluid">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link active" href="#"><img src="./assets/RZD logo.png" alt="" width="300px" height="50px"></a>
        </li>
      </ul>
    </div>
  </nav>

    <router-view :key='$route.fullPath'></router-view>

</template>

<style>
</style>
