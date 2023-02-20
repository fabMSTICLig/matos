<template>
  <footer>
    <div class="container-fluid mt-3 mb-3 border-top border-dark">
      <div class="row mt-3">
        <div class="col">
          <a
            class="logo-font"
            href="/"
          >Matos</a> 
          | 
          <router-link
            class="logo-font"
            to="/legalnotice"
          >Mentions légales</router-link>
          | 
          <router-link
            class="logo-font"
            to="/datapolicy"
          >Traitement des données</router-link>
        </div>
        <div class="col align-self-end media">
          <img
            :src="`${publicPath}logos-inp-uga.jpg`"
            width="30%"
            class="mr-4 float-end"
          >
          <img
            :src="`${publicPath}nanoelec-logo.jpg`"
            width="20%"
            class="mr-3 float-end"
          >
        </div>
      </div>
      <div class="row">
        <div class="col">
          <span class="justify">La plateforme est soutenue par l'IRT Nanoelec au titre du programme
            d'Investissement d'Avenir financé par l’État français, référence
            ANR-10- AIRT-05.
          </span>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
const publicPath = import.meta.env.BASE_URL
</script>
