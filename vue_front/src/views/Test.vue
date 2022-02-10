<template>
  <div class="home">
    <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
      <div class="lds-dual-ring"></div>
    </div>
     <form @submit.prevent='registerUserOndDjango' >
          <input type="file" @change='getImage'>
          <div v-if="selectedFile">
              <img ref='image' :src="selectedFile">
          </div>
            <button>save</button>
      </form>
  </div>
</template>

<script>
import {mapGetters,mapActions} from 'vuex'
import axios from 'axios'
export default {
  name:'questions',
  data(){
    return{
      st:'o',
      id: 5,
      selectedFile:''
    }
  },
  methods:{
    async getImage(event){
            console.log('event',event)
            this.selectedFile = URL.createObjectURL(event.target.files[0])
            this.image = event.target.files
            await console.log()
            // this.imageCropper()
        },
    registerUserOndDjango(){
            console.log('start add')
            const formData = new FormData()
            formData.append('thumbnail',this.image[0])
            formData.append('UID','kokomoko')
            formData.append('name','mokokoko')
            formData.append('email','ko@k.com')
            formData.append('grade','kokomoko')
            formData.append('country','japan')
            axios({
                method: 'post',
                url: '/api/user/',
                data: formData
                // {
                //   headers:{'Content-Type': "multipart/form-data"},
                //     UID: 'kokomoko',
                //     name: 'mokkoro',
                //     email: 'koko@k.com',
                //     grade: 'unko',
                //     thumbnail: this.selectedFile,
                //     country: 'japan'
                // },
            })
        },
      async userUpdate(){
            const formData = new FormData()
            formData.append('thumbnail',this.selectedFile)
            console.log('getthumb',formData.get('thumbnail'))
          await axios.patch(`/api/user/${this.$route.params.uid}`,
              formData, formData.name
          )
        //   ({
        //       methods: 'patch',
        //       url: `/api/user/${this.$route.params.uid}`,
        //       data:{
        //         //   thumbnail: this.selectedFile
        //         name: 'unko'
        //             }
        //         })      
            },
    quizRouter(i,f,n){
      return { name: 'Quiz', params:{ id:i, field:f, num:n}}
    },
    ...mapActions(['getquiz','getquestions'])
    // unko(){
    //   this.$store.commit('unko',)
    // }
    },
    
    created(){
      // this.$store.commit('setNum',this.id)
      // this.getquiz()
      // this.getquestions()
    },
    
  // mounted(){
  //     this.st = this.$store.commit('unko')
  //     console.log(this.st)
  // }
  computed: mapGetters(['questions','quizzes'])

}
</script>

<style>

</style>