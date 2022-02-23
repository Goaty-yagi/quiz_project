<template>
    <div class="l-wrapper">
        <!-- <CropperField 
        v-if="showCropper"
        :selectedFile='selectedFile'
        @handleShowCropper="handleShowCropper"
        @getCanvas='getCanvas'
        />  -->
        <div class='l-container'>
            <div class="title-black">
                <p>質問投稿</p>
            </div>
            <form class="form" @submit.prevent='submitForm'>
                <div class="question-title-container">
                    <div class='title-flex'>
                         <p>TITLE</p>
                    </div>
                    <input class='question-title' maxlength="20" type="text" v-model='title' placeholder="20字以内">
                </div>

                <div class="line"></div>

                <div class="question-description">
                    <p class="title-black">質問文</p>
                </div>
                <div class='text-field'>
                    <textarea class='form-text' v-model='description'>
                     </textarea>
                </div>
                <!-- <label class="image">
                    <input class="label" type="file" @change='getImage' enctype="multipart/form-data">
                    <i class="fas fa-camera"></i>
                    <p>写真を添付</p>
                </label>
                {{ canvas}} -->
                <div class="button-group">
                    <p @click="$emit('handleShowCreateQuestion')">キャンセル</p>
                    <button class='btn-tr-black-base-sq' @click='confirm'>確認</button>
                </div>                
            </form>
        </div>
    </div>
</template>

<script>
import Cropper from 'cropperjs';
import CropperField from '@/components/board/CropperField.vue'
export default {
    components: {
        CropperField,
  },
    data(){
        return{
            title: '',
            description:'',
            selectedFile:'',
            showCropper: false,
        }
    },
    methods:{
        confirm(){
            console.log('in confirm')
            this.$store.commit('getTitle', this.title)
            this.$store.commit('getDescription', this.description)
            this.$emit('handleShowConfirm')
        },
        // resize(e){
        //     e.target.style.height = 'auto'
        //     e.target.style.height = `$(e.target.scrollHeight)px`
        // },
        getCanvas(canvas){
            this.canvan = canvas
        },
        handleShowCropper(){
            console.log(this.showCropper)
            this.showCropper = !this.showCropper
        },
        async getImage(event){
            console.log('event',event)
            this.selectedFile = URL.createObjectURL(event.target.files[0])
            this.image = event.target.files[0]
            await console.log(this.image)
            this.handleShowCropper()
        },
    }    
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
.l-container{
    display: flex;
    flex-direction: column;
    // justify-content: center;
    align-items: center;
    .title-black{
        margin-top: 2rem;
    }
    .form{
        width: 100%;
        display: flex;
        flex-direction: column;
        // justify-content: center;
        align-items: center;
        .question-title-container{
            width:100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            .title-flex{
                display: flex;
                width: 80%;
            }
            .question-title{
                border: solid $base-color;
                width: 80%;
                height: 2.5rem;
                background: $back-white;
                padding-left: 1rem;                
            }
        }
        .line{
            width: 80%;
            border-bottom: 0.2rem solid $dark-blue;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        .question-description{
            .title-black{
                margin: 0;
            }
        }
        .text-field{
            width:80%;
            .form-text{
                width: 100%;
                background: $back-white;
                height: auto;
                min-height: 200px;
                border: 0.1rem solid $base-color;
                border-radius: 1vh;
                padding: 1rem;
                resize: none;
            }
            .form-text:focus{
                outline: none;
            }

        }
        // .image{
        //     width:80%;
        //     display:flex;
        //     // align-items: left;  
        //     margin:1rem;
        //     // justify-content: flex-start;
        //     .label{
        //         display: none;
        //     }
        //     .fas{
        //         margin-top: 0.1rem;
        //     }
        //     p{
        //         margin-left: 0.5rem;
        //     }
        // }
        .button-group{
            width: 80%;
            display:flex;
            margin:1rem;
            justify-content: flex-end;
            .btn-tr-black-base-sq{
                margin-left: 0.5rem;
                padding-right: 0.5rem;
                padding-left: 0.5rem;
            }
        }
    }
}
// .cropper-wrapper{
//     position: relative;
//     .img{
//         position: absolute;
//     }
// }
.textarea{
    width: 100%;
    border: 2px solid #ddd;
    border-radius: 10px;
    font-size: inherit;
    outline: none;
    padding: 20px;
    min-height: 100px;
    box-sizing: border-box;
}
</style>