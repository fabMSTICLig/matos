<template>
  <footer class="site-footer">
    <div class="logo-area">
      <a href="https://www.univ-grenoble-alpes.fr" target="_blank">
        <img :src="`${publicPath}21-UGA.png`" class="logo-uga"/>
      </a>
    </div>
    <div class="container-fluid">
      <div class="row computer-footer">
        <div class="col-6">
          <div class="contact-address">
            <p>
              FabLab MASTIC<br>
              Université Grenoble Alpes<br>
              740, Rue de la Piscine<br>
              38400 Saint-Martin-d’Hères France
            </p>
            <p class="text-foot">
              La plateforme est soutenue par l'IRT Nanoelec au titre du programme
              d'Investissement d'Avenir financé par l’État français, référence
              ANR-10- AIRT-05.
            </p>
          </div>
        </div>
        <div class="col-6 d-flex justify-content-md-center">
          <nav role="navigation">
            <ul class="list-unstyled">
              <li>
                <a
                  class="logo-font"
                  href="/"
                >
                  Matos
                </a>
              </li>
              <li>
                <router-link
                  class="logo-font"
                  to="/legalnotice"
                >
                  Mentions légales
                </router-link>
              </li>
              <li>
                <router-link
                  class="logo-font"
                  to="/datapolicy"
                >
                  Traitement des données
                </router-link>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
  </footer>
</template>

<style>
  @import "../assets/CSS/footer-screen.css";
</style>

<script setup>
  const publicPath = import.meta.env.BASE_URL
</script>
