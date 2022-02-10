<template>
    <div class='thumbnail-wrapper'>
        <p>thumbnail</p>
        <form @submit.prevent='userUpdate'>
            <input type="file" @change='getImage' enctype="multipart/form-data">
            <div v-if="selectedFile">
                <img ref='image' :src="selectedFile">
            </div>
             <button>save</button>
        </form>
         <button v-if='selectedFile' @click='chancel'>chancel</button>
        <div>
            <!-- <div>
                <img id="image" src="@/assets/logo.png">
            </div> -->
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import Cropper from 'cropperjs';
export default {
    data(){
        return{
            file:'',
            image:'',
            selectedFile:null,
            cropper:{},
            destination:{}
        }
    },
    mounted(){
        // this.cropper()
        console.log(this.image)
    },
    methods:{
        async getImage(event){
            console.log('event',event)
            this.selectedFile = URL.createObjectURL(event.target.files[0])
            this.image = event.target.files[0]
            await console.log(this.image)
            this.imageCropper()
        },
        async imageCropper(){
            // console.log(Cropper.getCanvasData())
            this.cropper = new Cropper(this.$refs.image, {
            zoomable: false,
            scalable: false,
            zoomOnTouch: true,
            aspectRatio: 1,
            crop(event) {
                    console.log(event.detail.x);
                    console.log(event.detail.y);
                    console.log(event.detail.width);
                    console.log(event.detail.height);
                    console.log(event.detail.rotate);
                    console.log(event.detail.scaleX);
                    console.log(event.detail.scaleY);
                },
            })
        },
        chancel(){
            this.selectedFile=null
        },
        async userUpdate(){
            const canvas = this.cropper.getCroppedCanvas({
                width: 160,
                height: 90,
                minWidth: 256,
                minHeight: 256,
                maxWidth: 4096,
                maxHeight: 4096,
                fillColor: '#fff',
                imageSmoothingEnabled: false,
                imageSmoothingQuality: 'high',
                });
            canvas.toBlob(async (blob) => {
            const formData = new FormData();
            formData.append('thumbnail',blob, `${this.image}.png`),
            console.log('getthumb',formData.get('thumbnail')),
            await axios.patch(`/api/user/${this.$route.params.uid}`,
                formData
            )
            }, 'image/png')
            // this.$router.go({path: this.$router.currentRoute.path, force: true})
        }
    }
}
</script>

<style>
.thumbnail-wrapper{
    width: 100%;
    height: 100%;
    overflow:scroll;  
}
.cropper-area img {
  display: block;
  max-width: 100%;
}
.cropper-view-box,
    .cropper-face {
      border-radius: 50%;
      cursor: grab;
      outline: initial;
    }
    .cropper-face:active {
      cursor: grabbing;
    }

</style>