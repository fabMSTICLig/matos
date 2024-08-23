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
      <h1 class="uga-page-title">Données personnelles</h1>
      <PartageTools />

      <div class="uga-page-content">
        <h3>Politique de confidentialité</h3>
        <p>Matos, s’engage à ce que les traitements de données personnelles effectués dans le cadre de la mise à disposition de son site internet soient conformes au règlement européen n° 2016/679, dit Règlement Général sur la Protection des Données à caractère personnel (RGPD) ainsi qu’à la loi Informatique et Libertés.</p>
        <p>Dans la présente politique de confidentialité (la « <strong>Politique</strong> »), nous vous expliquons comment et pourquoi nous utilisons vos données, quels sont vos droits et comment les exercer.</p>
        <h3>1. C’est quoi une donnée à caractère personnel ?</h3>
        <p>Une donnée personnelle (« <strong>Donnée Personnelle </strong>» ou « <strong>Donnée</strong> ») désigne toute information relative à une personne physique identifiée ou identifiable :</p>
 <ul>
   <li>directement (nom, prénom, adresse e-mail) ; ou</li>
   <li>indirectement (adresse IP, géolocalisation).</li>
 </ul>
    <h3>2. A qui s’adresse cette politique de confidentialité ?</h3>
 <p>La présente politique, s’adresse à tous les utilisateurs du site matos.univ-grenoble-alpes.fr qui créent un compte ou se connectent ou naviguent sur ledit site.</p>
    <h3>3. Pourquoi vos données sont-elles collectées ?</h3>
 <p>Nous collectons vos données identifiantes : nom, prénom et adresse mail pour :</p>
 <ul>
    <li>La gestion des prêts sur la base de l’intérêt légitime</li>
    <li>La réalisation de statistiques annuelles des prêts sur l’intérêt légitime</li>
    <li>Enquête d’amélioration du service sur la base de votre de votre consentement.</li>
 </ul>
    <h3>4. Combien de temps conservons-nous vos données ?</h3>
 <p>Nous conservons vos données dans nos serveurs pendant 2 ans. Elles sont traitées par les services internes ne font objet d’aucun transfert vers des destinataires ou partenaires externes.</p>
    <h3>5. Quels sont vos droits</h3>
 <p>Vous pouvez :</p>
 <ul>
    <li>Solliciter une copie des Données – <strong>Droit d’accès</strong></li>
    <li>Corriger une Donnée inexacte vous concernant – <strong>Droit de rectification</strong></li>
    <li>Demander l’effacement de certaines Données qui vous concernent, – <strong>Droit d’effacement</strong></li>
    <li>S’opposer à ce que nous traitions vos Données – <strong>Droit d’opposition</strong></li>
    <li>Limiter l’utilisation de vos Données le temps que votre demande soit traitée – <strong>Droit de limitation du traitement</strong></li>
 </ul>
    <h3>6. Comment exercer vos droits ?</h3>
 <p>Ces droits peuvent être exercés en nous écrivant :</p>
 <p>Par voie postale : 621 avenue Centrale
 </br>
 38400 Saint-Martin-d'Hères
 </br>
 France</p>
 <p>Par voie électronique : relaisdpo@univ-grenoble-alpes.fr</p>
 <p>Vous pouvez également vous adresser à la <strong>Commission Nationale de l’Informatique et des Libertés (CNIL)</strong>, autorité de régulation chargée de faire respecter la réglementation sur la protection des données à caractère personnel en France, par internet https://www.cnil.fr/fr/agir ou par voie postale à l’adresse suivante : Commission Nationale de l'Informatique et des Libertés, 3 Place de Fontenoy - TSA 80715, 75334 PARIS CEDEX.</p>
    <h3>7.  Sécurité des données :</h3>
 <p>Matos s’engage à mettre en place les mesures techniques et organisationnelles afin de garantir une sécurité maximale de vos données personnelle interdisant ainsi l’accès non autorisé ou la modification, divulgation, perte ou destruction de vos données. Aussi, l’accès à vos données personnelles et à leur traitement est limité aux seules personnes autorisées.</p>
 <p>Lorsqu’une violation de Données susceptible d’engendrer un risque élevé pour vos droits et libertés est détectée, vous serez informés de cette violation dans les meilleurs délais.</p>
 <p>Pour toute question concernant la politique de confidentialité ou relative au traitement de vos données, contactez-nous à l’adresse relaisdpo@univ-grenoble-alpes.fr.</p>
      </div>

      <PartageTools />

      <footer class="uga-page-date">
        <div>
          <p>
            <time class="published" datetime="2023-09-01T00:00:00+02:00">
              Publié le 23 aout 2024
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
