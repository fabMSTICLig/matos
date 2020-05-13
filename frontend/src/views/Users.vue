<template>
<div id="users">
    <Breadcumb />
<router-view></router-view>
</div>
</template>

<script>
import Breadcumb from "@/components/Breadcumb";
import { PUSH_BREADCUMB, POP_BREADCUMB} from "@/store/actions.type";
  export default {
    name: "Users",
    components: {
      Breadcumb,
    },
    data() {
      return {
      }
    },

    computed: {
    },
    methods: {

    },
    beforeMount(){
      this.$store.dispatch(PUSH_BREADCUMB, {label: 'Utilisateurs', url: this.$route.matched[0].path})
    },
    beforeRouteLeave(to, from , next){
        this.$store.dispatch(POP_BREADCUMB)
        next()
    },


  };
</script>
