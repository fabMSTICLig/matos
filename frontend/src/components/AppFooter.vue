<template>
  <div>
    <div class="featured-bottom">
      <aside class="container-liquid clearfix" role="complementary">
        <div>
          <div id="block-tutellesblock">
            <aside class="container-liquid clearfix" role="complementary">
              <div class="uga-partner-block">
                <div class="d-flex justify-content-center flex-wrap">
                  <div class="item">
                    <a
                      href="https://www.univ-grenoble-alpes.fr"
                      target="_blank"
                    >
                      <img :src="`${publicPath}UGA.svg`" class="logo" />
                    </a>
                  </div>
                </div>
              </div>
            </aside>
          </div>
        </div>
      </aside>
    </div>
    <footer class="site-footer">
      <div class="container-liquid">
        <div class="row">
          <div class="col-10">
            <div class="row">
              <div class="col-12 col-sm-8 col-md-4">
                <div
                  id="block-uga-theme-contact-address"
                  class="contact-address"
                >
                  <p>
                    FabLab MASTIC<br />
                    Université Grenoble Alpes<br />
                    740, Rue de la Piscine<br />
                    38400 Saint-Martin-d’Hères France
                  </p>
                  <p>
                    La plateforme est soutenue par l'IRT Nanoelec au titre du
                    programme d'Investissement d'Avenir financé par l’État
                    français, référence ANR-10- AIRT-05.
                  </p>
                </div>
              </div>
              <div
                class="col-12 col-sm-4 col-md-4 d-flex justify-content-md-center"
              >
                <nav
                  id="block-uga-theme-menu-footer"
                  role="navigation"
                  aria-labelledby="block-uga-theme-menu-footer-menu"
                >
                  <h2
                    id="block-uga-theme-menu-footer-menu"
                    class="visually-hidden"
                  >
                    Menu footer
                  </h2>

                  <ul class="list-unstyled">
                    <li>
                      <a href="/"> Matos </a>
                    </li>
                    <li>
                      <router-link to="/legalnotice">
                        Mentions légales
                      </router-link>
                    </li>
                    <li>
                      <router-link to="/datapolicy">
                        Traitement des données
                      </router-link>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
          <div class="col-2">
            <a href="#" @click.prevent="backToTop()" class="back-to-top" title="Back to top">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                viewBox="0 0 16 16"
                fill="var(--link-color-bg-secondary)"
              >
                <path
                  d="m0 8 1.455 1.455 5.506-5.506V16h2.078V3.948l5.506 5.507L16 8 8 0Z"
                ></path>
              </svg>
            </a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
const publicPath = import.meta.env.BASE_URL;
function backToTop()
{
window.scrollTo(0,0)
}
</script>
