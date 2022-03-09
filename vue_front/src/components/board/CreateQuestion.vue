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
                        <div
                         class="tag-comment">
                            <p v-if="showParentTag==false&&showSelectedTagList==false&&selectedTagList==false" @click="handleShowParentTag">タグを選んでください</p>
                            <p v-if="showParentTag&&selectedTagList==false">最大３つまで選べます</p>
                            <div class="tag-group-container" v-if="selectedTagList[0]">
                                <div class="tag-group">
                                    <div>{{ selectedTagList[0].tag }}</div>
                                    <div class="circle" @click="deleteTag(selectedTagList[0])">
                                         <p>×</p>
                                    </div>
                                </div>
                                 <div class="tag-group" v-if="selectedTagList[1]">
                                    <div>{{ selectedTagList[1].tag }}</div>
                                    <div class="circle" @click="deleteTag(selectedTagList[1])">
                                         <p>×</p>
                                    </div>
                                </div>
                                 <div class="tag-group" v-if="selectedTagList[2]">
                                    <div>{{ selectedTagList[2].tag }}</div>
                                    <div class="circle" @click="deleteTag(selectedTagList[2])">
                                         <p>×</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="tag-angle"
                         @click="handleShowParentTag">
                             <i class="fas fa-angle-down"></i>
                        </div>
                    </div>
                    <div class="tag-pull-down" v-if="showParentTag">
                        <div class="tag-loop"
                        v-for="(parentTag,tagindex) in Object.keys(parentTagDict)"
                        v-bind:key="tagindex"
                        @click="getCenterTag(parentTag)">
                            <div
                             class="tag-parent">
                                <p >{{ parentTag }}</p>
                            </div>
                            <div class="angle-right">
                                <i class="fas fa-angle-right"></i>
                            </div>
                        </div>
                        <div
                            class="tag-child"
                            v-show="showChildTag">
                            <p
                             v-for="(tag,tagindex) in centerTagList"
                             v-bind:key="tagindex"
                             @click="addTags(tag.tag, tag.id)">
                                {{ tag.tag }}
                            </p> 
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
            <div v-if="alerts.title||alerts.description||alerts.tag" :class="{'notification-red':alerts.title||alerts.description||alerts.tag}">
                <div v-if="alerts.title" class="notification-text">
                    タイトルを入力してください。
                </div>
                <div v-if="alerts.description" class="notification-text">
                    文章を入力してください。
                </div>
                <div alerts.tag class="notification-text">
                    最低タグを１つ選んでください。
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
        'parentTagDict',
        // 'parentTagList'
    ],
    data(){
        return{
            title: '',
            centerTagList:[],
            selectedTagList:[],
            selectedTagDict:{},
            description:'',
            selectedFile:'',
            showParentTag: false,
            showChildTag: false,
            showSelectedTagList: false,
            alart: false,
            alerts: {
                title: false,
                description: false,
                tag:false
            },
            showCropper: false,
        }
    },
    mounted(){
        console.log("CQmounted",this.parentTagDict)
        // this.de()
    },
    watch:{
        selectedTagList: {
            handler(a){
                if (this.selectedTagList.length == 3){
                    console.log('3dayo')
                    this.showSelectedTagList = true
                    this.showParentTag = false
                    this.showChildTag = false
                }
                if(this.selectedTagList.length == 0){
                    this.showParentTag = false
                    this.showSelectedTagList = false
                    this.showChildTag = false
                }
            },deep:true          
        } 
    },
    methods:{
        confirm(){
            console.log('in confirm')
            this.formCheck()
            console.log(this.alerts.title, this.alerts.description)
            if(this.alerts.title==false&&this.alerts.description==false&&this.alerts.tag==false){
                this.$store.commit('getTitle', this.title)
                this.$store.commit('getDescription', this.description)
                console.log(this.selectedTagList)
                this.$store.commit('getTagList', this.selectedTagList)
                this.$emit('handleShowConfirm')
            }
        },
        getCenterTag(parentTag){
            this.handleShowChildTag()
            if (this.centerTagList[0]){
                this.centerTagList = []
            }
            for(let i of this.parentTagDict[parentTag]){
                this.centerTagList.push({"id":i.id, "tag":i.tag})
            }
            console.log('center.tag',this.centerTagList)
        },
        // getTagId(){
        //     const tagIdList = []
        //     for(let i of this.selectedTagList){
        //         tagIdList.push(i.id)
        //     }
        //     return tagIdList
        // },
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
        addTags(tag,id){
            console.log('tag',tag,'id',id)
            if(this.selectedTagList.length > 0){
                console.log("something")
                for(let selectedTag of this.selectedTagList){
                    if(selectedTag.tag == tag){
                        this.selectedTagList = this.selectedTagList.filter(item => item!=selectedTag)
                        return
                    }
                }
            }
            if (this.selectedTagList.length >= 3){
                this.alart = true
                return
            }
            this.selectedTagList.push({"tag":tag, "id":id})
            console.log(this.selectedTagList)
        },
        deleteTag(tag){
            this.selectedTagList = this.selectedTagList.filter(item => item!=tag)
            console.log(tag,'is deleted')
            if(this.selectedTagList.length == 0){
                console.log("0dayo")
                this.showParentTag = false
                this.showSelectedTagList = false
            }
        },
        resetNotifications(){
            this.alerts.description = false
            this.alerts.title = false
            this.alerts.tag = false
        },
        formCheck(){
            if(this.description==''){
                this.alerts.description = true
                setTimeout(this.resetNotifications, 3000)
            }
            if(this.title==''){
                this.alerts.title = true
                setTimeout(this.resetNotifications, 3000)
            }
            if(this.selectedTagList==false){
                this.alerts.tag = true
                setTimeout(this.resetNotifications, 3000)
            }
        },
        handleShowParentTag(){
            this.showParentTag = !this.showParentTag
        },
        handleShowChildTag(){
            this.showChildTag = true
            console.log('inhandle',this.showChildTag)
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
                    .tag-group-container{
                        display: flex;
                        .tag-group{
                            border: solid gray;
                            border-radius: 50vh;
                            width: auto;
                            min-width: 3rem;
                            margin-right: 0.5rem;
                            display: inline-block;
                            align-items: center;
                            padding-top:0.1rem;
                            padding-bottom: 0.1rem;
                            padding-left: 0.5rem;
                            padding-right: 0.5rem;
                            font-size:0.7rem;
                            font-weight: bold;
                            div{
                                // flex-basis:60%;
                                display: inline-block;
                            }
                            .circle{
                                // border-radius: 50vh;
                                flex-basis:40%;
                                display: inline-block;
                                align-items: center;
                                justify-content: center;
                                margin-left:0.5rem;
                                p{
                                    font-weight: bold;
                                    color: $dark-blue;
                            }
                            }
                        }
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
                position: absolute;
                background: $back-tr-white;
                border: solid $base-color;
                width: inherit;
                display: flex;
                flex-direction: column;
                padding:0.5rem;
                .tag-loop{
                    display: flex;
                    .tag-parent{
                        flex-basis:40%;
                        display: flex;
                        p{}
                    }
                    .fa-angle-right{
                        flex-basis:60%;
                    }
                }
                .tag-child{
                    position:absolute;
                    background: $back-tr-white;
                    width:60%;
                    right:0;
                    display: flex;
                    flex-direction: column;
                }
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