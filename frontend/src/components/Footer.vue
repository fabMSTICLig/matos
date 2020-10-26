<template>
  <footer>
    <div class="container mt-3 mb-3 border-top border-dark">
      <div class="row d-inline-flex">
        <div class="col col-lg-6">
          <div class="row mt-5">
            <div class="col">
              <a class="logo-font" href="/">
                Matos
              </a>
              |
              <a class="logo-font" href="/legalnotice">
                Legal notice
              </a>
            </div>
          </div>
        </div>
        <div class="col col-lg-6 media">
          <img
            :src="`${publicPath}logos-inp-uga.jpg`"
            width="50%"
            class="mr-4"
          />
          <img
            :src="`${publicPath}nanoelec-logo.jpg`"
            width="40%"
            class="mr-3"
          />
        </div>
      </div>
      <div class="row">
        <div class="col">
          <span class="justify"
            >La plateforme est soutenue par l'IRT Nanoelec au titre du programme
            d'Investissement d'Avenir financé par l’État français, référence
            ANR-10- AIRT-05.
          </span>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "Footer",
  data() {
    return {
      publicPath: process.env.BASE_URL
    };
  }
};
</script>
