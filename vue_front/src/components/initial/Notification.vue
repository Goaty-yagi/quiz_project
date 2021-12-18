<template>
    <div class='notification-wrapper'>
        <div class='notice-wrapper'>
            <img class='image' src="@/assets/logo.png">
            <p class='text1'>登録すると…</p>
            <div class='block'>
                <div class='font-inline'>
                    <i id='font' class="fas fa-cog">
                        <div class='circle'/>  
                        <i class="far fa-lightbulb" id='in-font'></i>
                        <div class='text'>
                            <p>色んなクイズができる</p>
                        </div>
                    </i>       
                </div>
                <div class='font-inline'>
                    <i id='font' class="fas fa-cog">
                        <div class='circle'/>  
                        <i class="fas fa-crown" id='in-font'></i>
                        <div class='text'>
                            <p>自分のレベルを管理できる</p>
                        </div>
                    </i>       
                </div>
            </div>
            <div class='block'>
                <div class='font-inline'>
                    <i id='font' class="fas fa-cog">
                        <div class='circle'/>  
                        <i class="fas fa-award" id='in-font'></i>
                        <div class='text'>
                            <p>毎日、実力を確認できる</p>
                        </div>
                    </i>       
                </div>
                <div class='font-inline'>
                    <i id='font' class="fas fa-cog">
                        <div class='circle'/>  
                        <i class="fas fa-robot" id='in-font'></i>
                        <div class='text'>
                            <p>コミュニティに参加できる</p>
                        </div>
                    </i>       
                </div>
            </div>
            <div class='buttons'>
                <router-link @click='closeConf' to='/' class='button' id='register-button'>登録しない</router-link>
                <router-link  to='/signin' class='button' id='register-button'>登録する</router-link>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    mounted(){
    },
    methods:{
        closeConf(){
            this.$emit('close')
            this.$store.commit('reset')
        },
    }
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
    .notification-wrapper{
        top:0;
        position: fixed;
        background:rgba(0,0,0,0.5);
        width:100vw;
        height:100vh;
        flex-direction: column;
        display: flex;
        justify-content: center;
        align-items: center;
       
        
        
    }
    .notice-wrapper{
        border: solid $base-color;
        border-radius: 2vh;
        background:$back-white;
        
        // height:70%;
        text-align: center;
        
        display:inline-block;
    }
    .image{
        width:15%;
        height:15%;
        margin-left: auto;
        margin-right: auto;
    }
    .text1{
        font-size:7vw;
        font-weight: bold;
    }
    .block{
        display:flex;
        justify-content: center;
        align-items: center;
        // width:100%;
        // height:100%;
        margin-top:-3%;
    }
    .font-inline{
        flex-basis:auto;
            }.font-inner{
                color:initial;
                position:absolute;
                font-size:10vw;
                color:$back-white;
            }
    #in-font{
        font-size:initial;
        color:initial;
        font-size:10vw;
        color:$back-white;
        position:absolute;
        top: 25%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    .text{
        color:initial;
        position:absolute;
        top:55%;
        // top:25vw;
        // left:0;
        padding-left:20%;
        padding-right:20%;
        font-size:4vw;
        font-weight: bold;
        text-align: center;
    }
    #font{
        position:relative;
    // border:solid black;
        // margin-top:-15%;
        font-size:40vw;
        color: $base-color;
        // font-size:1.5rem;
        // position:absolute;
        // font-size:3rem;
        top:auto;
        bottom:auto;

    }.circle{
        position:absolute;
        border:solid $base-color;
        border-radius: 50%;
        background:$base-color;
        margin:auto;
        height: 15vw;
        width: 15vw;
        margin: 0 auto;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    .buttons{
        display:flex;
        justify-content: center;
        align-items: center;
        margin:10%;
    }
    #register-button{
        width: auto;
        font-size:5vw;
        padding:1.5%;
        
    }
@media(min-width: 660px) and (max-width: 1024px){
    .notice-wrapper{
        margin-top:10%;
        width:80%;
    }
    #font{
        font-size:35vw;
    }
    .text{
        font-size:3vw;
    }
    #register-button{
        font-size:3vw;
    }
  }
@media(min-width: 1025px){
    .text1{
        font-size:3vw;
    }
    .notice-wrapper{
        margin-top:10%;
        width:40%;
        height:50vw;
    }
    .block{
        margin:1.5vw;
    }
    #font{
        font-size:13vw;
    }
    .circle{
        height: 10vw;
        width: 10vw;
    }
    .text{
        font-size:1.1vw;
    }
    #register-button{
        font-size:3vw;
    }
    #in-font{
        font-size:3vw;
    }
    #register-button{
        font-size:1.5vw;
  }
}
// @media(min-width: 1550px){
//     .text1{
//         font-size:3vw;
//     }
//     .wrapper{
//         margin-top:10%;
//         width:40%;
//         height:70%;
//     }
//     .block{
//         margin:1.5vw;
//     }
//     #font{
//         font-size:13vw;
//     }
//     .circle{
//         height: 10vw;
//         width: 10vw;
//     }
//     .text{
//         font-size:1.1vw;
//     }
//     #register-button{
//         font-size:3vw;
//     }
//     #in-font{
//         font-size:3vw;
//     }
//     #register-button{
//         font-size:1.5vw;
//   }
// }
</style>