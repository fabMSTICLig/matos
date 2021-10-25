<template>
  <div class="home">
    <div class="row justify-content-center">
      <div class="col-12 col-md-12">
        <div class="card">
          <div class="card-header">
            <h4>Le site MATOS</h4>
          </div>
          <div class="card-body">
            <h4>Contexte</h4>
            <p class="text-justify">
              Pour réduire son impact écologique, la première étape est de moins
              et mieux consommer.
            </p>

            <p class="text-justify">
              L'université possède beaucoup de matériels à des fins pédagogiques
              et de recherche. Ces matériels sont répartis dans les nombreuses
              composantes universitaires, écoles d'ingénieurs, laboratoires de
              recherche et services qui lui sont rattachés. Parfois certains
              matériels sont inutilisés pendant de longues périodes et les
              différentes entités, qui les possèdent, sont disposé à prêter ces
              matériels. Cependant, il est difficile de savoir qui possède quoi
              et ce qui est disponible.
            </p>

            <p class="text-justify">
              Pour cette raison, le site de prêt Matos a été créé afin d'aider à
              la mutualisation du matériel. L'idée est que toutes entités de
              l'université puissent mettre à disposition le matériel qu'elle
              souhaite.
            </p>
            <h4>Principe de fonctionnement</h4>
            <p class="text-justify">
              Dans la suite, nous allons utilisé le terme
              <strong>entité</strong>. Une <strong>entité</strong> n'a pas de
              granularité définie. Elle peut être un laboratoire, un service
              dans un laboratoire, une composante universitaire, une plateforme
              technique, un fablab, ...
            </p>
            <p class="text-justify">
              Une entité souhaite mettre à disposition du matériel.
            </p>
            <ul>
              <li>
                Elle contacte les administrateurs du site afin que ceux-ci lui
                créent un espace sur le site.
                <a href="mailto:matos@univ-grenoble-alpes.fr"
                  >matos@univ-grenoble-alpes.fr</a
                >
              </li>
              <li>
                Une ou plusieurs personnes seront définie comme
                <strong>manager</strong> de cette entité. Ils pourront modifier
                les différentes informations affichées, rajouter du matériel et
                gérer les prêts sur le site.
              </li>
              <li>
                Une fois les matériels rentrer sur le site, ceux-ci seront
                visibles à toutes personnes connectées au site.
              </li>
            </ul>

            <p class="text-justify">
              Une personne souhaite emprunter du matériel.
            </p>
            <ul>
              <li>Elle se connecte au site.</li>
              <li>Elle recherche sur le site le matériel qu'elle a besoin.</li>
              <li>
                Elle remplir l'équivalent d'un panier d'un site de commerce.
              </li>
              <li>
                Elle remplit la date de l'emprunt et la date de retour prévue du
                matériel.
              </li>
              <li>
                Elle valide la demande, une notification est envoyé à l'entité.
              </li>
              <li>
                L'entité peut alors prendre contact par mail avec le demandeur
                afin d'avoir des précisions.
              </li>
              <li>L'entité valide ensuite le prêt.</li>
              <li>
                Une fois la matériel rendu l'entité inscrit la date de retour
                effective du matériel.
              </li>
              <li>Le prêt est clos.</li>
            </ul>

            <p class="text-justify">
              Sur le site, il existe deux types de matériel:
              <strong>Spécifique</strong> et <strong>Générique</strong>:
            </p>

            <ul>
              <li>
                Le matériel Spécifique correspond au matériel dont on ne peut
                pas intervertir les instances. Par exemple le fablab possède 10
                tablettes MarqueX (10 instances), chaque tablette a un numéro de
                série, s'il prête la tablette 1 (l'instance 1), il est important
                que ce soit la tablette 1 qui revienne.
              </li>
              <li>
                Le matériel Générique correspond au matériel dont on peut
                intervertir les instances. Par exemple, le fablab possède des
                cartes Arduino Uno, quand il prête une carte Arduino Uno, il
                souhaite qu'une carte Arduino Uno soit retournée, mais ce n'est
                pas très grave si ce n'est pas la même que celle prêtée.
              </li>
            </ul>

            <p class="text-justify">
              Le site permet d'aider à la gestion des prêts, mais chaque entité
              peut avoir des procédure interne en plus pour prêter son matériel
              comme des documents à remplir. Il est donc préférable de le noter
              dans la description de l'entité.
            </p>

            <p class="text-justify">
              La seule restriction à l'utilisation du site est que le prêt doit
              être gratuit et donc il ne doit pas y avoir de contrepartie
              financière.
            </p>
          </div>
        </div>
      </div>
      <div class="col-12 mt-4">
        <div class="card">
          <div class="card-header">
            <h4>Traitement des données</h4>
          </div>
          <div class="card-body scroll">
            <section>
              <article>
                <h3>Destinataires</h3>
                <p align="justify">
                  Chaque entité, composante universitaire, école, laboratoire ou
                  plateforme pédagogique representée par un ayant droit, dispose
                  de ses données sur la plateforme.
                </p>
              </article>
              <article>
                <h3>Stockage des informations</h3>
                <p>
                  Pour permettre le bon fonctionnment du site certaines de vos
                  informations sont stockées au moyen d'un cookie. Votre login
                  <i>Agalan</i> vous permet d'utiliser la plateforme, et le nom
                  d'utilisateur est enregistré pendant la session. Un cookie est
                  également utilisé pour enregistrer le prêt en cours
                  d'utilisation (création ou modification)
                </p>
                <h4>Données utilisées</h4>
                <p>
                  Nom d'utilisateur, Prénom, Nom, Email sont utilisés afin de
                  vous contacter. Les managers des entités et les administrateur
                  du site ont accés à ces informations.
                </p>
              </article>
              <article>
                <h3>Durée de stockage</h3>
                <p>
                  Ces informations ainsi que celles liées aux prêts seront
                  stockées 1 ans après que vous ayez quitté l'université ou sur
                  demande aux adresses :
                </p>
                <ul>
                  <li>relaisdpo@grenoble-inp.fr</li>
                  <li>dpo@grenet.fr</li>
                </ul>
              </article>
              <article>
                <h3>Accès aux données personnelles</h3>
                <p>
                  A tout moment, vous pouvez demander un accès aux données vous
                  concernant, rectifier ou supprimer vos données avec les
                  contacts cités précédemment
                </p>
              </article>
              <article>
                <h3>Sécurité des données</h3>
                Les données enregistrées concernant les entités et les prêts
                sont accessibles aux managers des entités concernées et aux
                administrateurs du site.
              </article>
            </section>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Home",
};
</script>
