<template>
    <div class='thumbnail-wrapper l-wrapper'>
        <form @submit.prevent='userUpdate'>
            <input id="fileUpload" type="file" @change='getImage' hidden enctype="multipart/form-data">
            <div class="cropper-outer-wrapper" v-if="selectedFile">
                <div class='cropperinner-wrapper'>
                    <img ref='image' :src="selectedFile" style="width: 300px; height: 300px;">
                </div>
                <div class="thumbnail-button-container">
                    <button class='btn-base-white-db-sq thumbnail-save-button'>save</button>
                    <button class='btn-tr-white-base-sq thumbnail-cancel-button' v-if='selectedFile' @click='chancel'>cancel</button>
                </div>
            </div>
        </form>
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
    props:[
        "getDjangouser",
        "minContainerWidth",
        "minContainerHeight"
    ],
    data(){
        return{
            file:'',
            image:'',
            selectedFile:null,
            compoHandle: false,
            cropper:{},
            destination:{},
            inputFile:'',
        }
    },
    mounted(){
        // this.cropper()
        console.log('thumb mounted',this.getDjangouser)
        this.autoClick()
    },
    computed:{
        user(){
            return this.$store.state.signup.djangoUser
        },
        width(){
            if(this.minContainerWidth == 800){
                return 800
            }else{
                return 400
            }
        },
        height(){
            if(this.minContainerHeight == 800){
                return 800
            }else{
                return 400
            }
        }
    },
    methods:{
        async getImage(event){
            console.log('event',event)
            this.selectedFile = URL.createObjectURL(event.target.files[0])
            this.image = event.target.files[0]
            await console.log(this.image,'img',this.selectedFile)
            this.imageCropper()
        },
        async imageCropper(){
            this.cropper = new Cropper(this.$refs.image, {
            zoomable: true,
            scalable: false,
            zoomOnTouch: true,
            aspectRatio: 1,
            dragMode: 'move',
            minContainerHeight:this.height,
            minContainerWidth:this.width,
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
            this.showThumbnailFalse()
        },
        autoClick(){
            document.getElementById("fileUpload").click()
            this.inputFile = document.getElementById("fileUpload");
            document.body.onfocus = this.getEvent
        },
        getEvent(){
            setTimeout(() => {
                if (this.inputFile.value.length) {
                
                } else {
                this.showThumbnailFalse()
                }
                document.body.onfocus = null;
            }, 500);
        },
        openFileOnClick(){
            document.getElementById("fileUpload").value = "";
            document.getElementById("fileUpload").files.length = 0;            
            document.getElementById("fileUpload").click();
            if(document.getElementById("fileUpload").files.length >= 1){
                //Do something 
            }
            else{
                this.showThumbnailFalse()
                //Cancel button has been called.
            }
        },
        // getCroppedURL(){
        //     console.log('croppedURL')
        //     document.getElementById('crop-btn').addEventListener('click', function () {
        //     resultImgUrl = this.cropper.getCroppedCanvas().toDataURL();
        //     var result = document.getElementById('result-img');
        //     result.src = resultImgUrl;
        //      });
        // },
        async userUpdate(){
            try{
                const canvas = this.cropper.getCroppedCanvas({
                width: 160,
                height: 90,
                minCropBoxHeight: 300,
                minCropBoxWidth: 300,
                maxWidth: 4096,
                maxHeight: 4096,
                fillColor: '#fff',
                imageSmoothingEnabled: false,
                imageSmoothingQuality: 'high',
                });
            await canvas.toBlob(async (blob) => {
            const formData = new FormData();
            formData.append('thumbnail',blob, `${this.image}.png`),
            console.log('getthumb',formData.get('thumbnail'),this.image,blob),
            axios.patch(`/api/user/${this.getDjangouser.UID}`,
                formData
            )
            }, 'image/png')
            this.showThumbnailFalse()
            this.$store.commit('setIsLoading', true)
            setTimeout(this.reload,1000)
            }
            catch(e){
                this.showThumbnailFalse()
                console.log('fale',e)
            }
            // this.$router.go({path: this.$router.currentRoute.path, force: true})
        },
        showThumbnailFalse(){
            this.$emit('showThumbnailFalse')
        },
        reload(){
            // this.$store.commit('setIsLoading', false)
            location.reload()
        }
    }
}
</script>

<style  lang="scss">
// not scoped for cropper
@import "style/_variables.scss";

.thumbnail-wrapper{
    position: absolute;
    width: 100%;
    height: 100%;
    /* background: ; */
    overflow:scroll;  
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
.thumbnail-button-container{
    display: flex;
    justify-content: center;
    margin-top: 1rem;
    .thumbnail-save-button{
        display: flex;
        justify-content: center;
        font-size: 1.2rem;
        margin-right: 0.5rem;
        min-width: 5rem;
        min-height: 2rem;
        font-weight: bold;
    }
    .thumbnail-cancel-button{
        display: flex;
        justify-content: center;
        font-size: 1.2rem;
        margin-left: 0.5rem;
        min-width: 5rem;
        min-height: 2rem;
        font-weight: bold;
    }
}
</style>