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
                <div class="tag-container">
                    <div class="tag-select">
                        <div class="tag-comment">
                            <p v-if="showParentTag==false">タグを選んでください</p>
                        </div>
                        <div class="tag-angle">
                             <i @click="handleShowParentTag" class="fas fa-angle-down"></i>
                        </div>
                    </div>
                    <div class="tag-pull-down">
                        <div class="tag-loop"
                        v-for="(parentTag,tagindex) in parentTags"
                        v-bind:key="tagindex"
                        :label="parentTag.parent_tag">
                            <div class="tag-parent" v-if="showParentTag">
                                {{ parentTag.parent_tag }}
                                <div class="tag-child">   
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="line"></div>

                <div class="question-description">
                    <p class="title-black">質問文</p>
                </div>
                <div class='text-field'>
                    <textarea class='form-text' v-model='description'>
                     </textarea>
                </div>
                <!-- <v-select :options="parentTagList"> -->
                    <!-- <optgroup
                     class="select-wrapper"
                     v-for="(parentTag,tagindex) in parentTags"
                     v-bind:key="tagindex"
                     :label="parentTag.parent_tag"
                     >{{parentTag.parent_tag}}
                     <option
                      v-for="(tag,tagindex) in parentTag.center_tag"
                      v-bind:key="tagindex"
                      :label="tag.tag">{{ tag.tag}}</option>
                    </optgroup> -->
                <!-- </v-select> -->
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
            <div v-if="alerts.title||alerts.description" :class="{'notification-red':alerts.title||alerts.description}">
                <div v-if="alerts.title" class="notification-text">
                    タイトルを入力してください。
                </div>
                <div v-if="alerts.description" class="notification-text">
                    文章を入力してください。
                </div>
            </div>
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
    props:[
        'parentTags',
        // 'parentTagList'
    ],
    data(){
        return{
            title: '',
            unko:["chinko","manko"],
            description:'',
            selectedFile:'',
            showParentTag: false,
            showChildTag: false,
            alerts: {
                title: false,
                description: false
            },
            showCropper: false,
        }
    },
    mounted(){
        console.log("CQmounted",this.parentTags)
    },
    methods:{
        confirm(){
            console.log('in confirm')
            this.descriptionTitleCheck()
            console.log(this.alerts.title, this.alerts.description)
            if(this.alerts.title==false&&this.alerts.description==false){
                this.$store.commit('getTitle', this.title)
                this.$store.commit('getDescription', this.description)
                this.$emit('handleShowConfirm')
            }
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
        resetNotifications(){
            this.alerts.description = false
            this.alerts.title = false
        },
        descriptionTitleCheck(){
            if(this.description==''){
                this.alerts.description = true
                setTimeout(this.resetNotifications, 3000)
            }
            if(this.title==''){
                this.alerts.title = true
                setTimeout(this.resetNotifications, 3000)
            }
        },
        handleShowParentTag(){
            this.showParentTag = !this.showParentTag
        }
    }    
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
.l-container{
    animation: l-container 3s;
    display: flex;
    flex-direction: column;
    position: relative;
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
        position:relative;
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
        .tag-container{
            border: solid $base-color;
            border-radius: 0.5rem;
            width: 80%;
            margin-top: 0.5rem;
            .tag-select{
                display: flex;
                align-items: center;
                .tag-comment{
                    flex-basis:90%;
                    margin:0.3rem;
                    height: 1.5rem;
                    p{

                    }
                }
                .tag-angle{
                    flex-basis:10%;
                    display: flex;
                    align-items: center;
                    // justify-content: flex-end;
                }
            }
            .tag-pull-down{
                position: fixed;
                background:whitesmoke;
                border: solid $base-color;
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