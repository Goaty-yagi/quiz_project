<template>
    <div class='l-wrapper'>
        <div class="cropper-outer-wrapper" v-if="previewFile">
            <div class='cropper-wrapper'>
                <img ref='image' :src="previewFile">
                <button class='save-button' v-if='previewFile' @click='chancel'>chancel</button>
                <button @click="saveImg">save</button>
            </div>
        </div>
    </div>
</template>

<script>
import Cropper from 'cropperjs';
export default {
    
    data(){
        return{
            previewFile:'',
            canvas:''
        }
    },
    props:[
        'selectedFile',
    ],
    beforeMount(){
        this.previewFile = this.selectedFile
    },
    mounted(){
        console.log('cropperOpen',this.previewFile)
        this.imageCropper()
    },
    methods:{
        saveImg(){
            this.canvas = this.cropper.getCroppedCanvas({
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
            console.log(this.canvas)
            this.$emit('getCanvas', this.canvas)
            this.$emit('handleShowCropper')
        },
        async imageCropper(){
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
            this.previewFile=null
            this.$emit('handleShowCropper')
        },
    }
}
</script>

<style>

</style>