<!--
Copyright (C) 2020-2024 LIG Université Grenoble Alpes


This file is part of Matos.

Matos is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
@author Clément Lesaulnier
@author Robin Courault

-->

<template>
  <div class="container text-justify p-4 col-lg-8 offset-lg-2">
    <main class="row">
      <h1 class="uga-page-title">Crédits</h1>
      <PartageTools />

      <div class="uga-page-content">
        <h3>Conception du site</h3>
        <p><strong>Réalisation :</strong> Fablab MASTIC</p>
        <p><strong>Contenus :</strong> Les entités prêteuses de matériels</p>
        <p>
          <strong>Conception graphique :</strong> Université Grenoble Alpes -
          Direction de la communication.
        </p>
        <h3>Outils de gestion et d'administration du site</h3>
        <p>
          <strong>Gestion des contenus :</strong> ce site fonctionne avec
          les outils Django et VusJs.
        </p>
        <p>
          <strong>Gestion des cookies :</strong> la gestion des cookies est
          opérée par Tarte au Citron.
        </p>
        <h3>Photographies/Vidéos</h3>
        <p>Droits réservés :</p>
        <p>© Université Grenoble Alpes</p>
      </div>

      <PartageTools />

      <footer class="uga-page-date">
        <div>
          <p>
            <time class="published" datetime="2023-09-01T00:00:00+02:00">
              Publié le 01 septembre 2023
            </time>
          </p>
        </div>
      </footer>
    </main>
  </div>
</template>
<script setup>
import PartageTools from "@/components/ui/PartageTools.vue";
</script>
