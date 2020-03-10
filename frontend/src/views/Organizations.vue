<template>
    
</template>


<script>
import { mapGetters } from "vuex";
import {
    GET_ORGA,
    FETCH_ORGAS,
    CREATE_ORGA,
    UPDATE_ORGA
} from '@/store/actions.type'

export default {
    name: 'Organizations',

    data(){
        return {
            actions: {
                GET: GET_ORGA,
                UPDATE: UPDATE_ORGA,
                CREATE: CREATE_ORGA,
                FETCH: FETCH_ORGAS,
            },
            objectName: "Organization"

        }
    },
    computed: {
        ...mapGetters(["orgas", "users"]),
        orga() {
        return this.object;
        },
        orgaMembers() {
        return this.users.filter(user => {
            return this.orga.members.includes(user.id);
        });
        },
    },
    methods: {
        deleteMember(user) {
        this.orga.members.splice(this.orga.members.indexOf(user.id), 1);
        },
        addUser(userid) {
        userid = parseInt(userid);
        if (!isNaN(userid) && this.orga.members.indexOf(userid) == -1) {
            this.orga.members.push(userid);
        }
        },
    },
  beforeMount() {
    this.$store.dispatch(FETCH_USERS);

  }
}


</script>
